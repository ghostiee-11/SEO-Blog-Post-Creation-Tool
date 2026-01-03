import requests
from bs4 import BeautifulSoup
from utils.headers import get_headers

def search_amazon(query=None):
    """
    Scrapes Amazon. 
    If query is provided -> Search Results.
    If query is None -> Best Sellers (Electronics).
    """
    if query:
        url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
    else:
        # Bestsellers in Electronics
        url = "https://www.amazon.com/gp/bestsellers/electronics/"
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        
        if response.status_code == 503:
            # Fallback data if blocked
            return [{"title": "Amazon Bot Blocked (Try Again)", "price": "$0.00", "image": "", "url": "#", "source": "Amazon"}]
            
        soup = BeautifulSoup(response.text, "lxml")
        products = []
        
        # Selectors differ for Search vs Bestsellers
        if query:
            items = soup.find_all("div", {"data-component-type": "s-search-result"}, limit=8)
        else:
            # Amazon Bestsellers Grid ID
            grid = soup.find("div", class_="p13n-gridRow")
            items = grid.find_all("div", id="gridItemRoot") if grid else []

        for item in items[:8]:
            try:
                # Logic to extract data (handles both layouts)
                if query:
                    title = item.find("h2").get_text(strip=True)
                    price_tag = item.find("span", class_="a-price-whole")
                    price = f"${price_tag.get_text(strip=True)}" if price_tag else "Check Price"
                    img = item.find("img", class_="s-image")['src']
                    link = "https://www.amazon.com" + item.find("a", class_="a-link-normal")['href']
                else:
                    # Bestseller Layout
                    title = item.find("div", class_="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1").get_text(strip=True)
                    price_tag = item.find("span", class_="_cDEzb_p13n-sc-price_3mJ9Z")
                    price = price_tag.get_text(strip=True) if price_tag else "Check Price"
                    img = item.find("img")['src']
                    link = "https://www.amazon.com" + item.find("a")['href']

                products.append({
                    "title": title,
                    "price": price,
                    "image": img,
                    "url": link,
                    "source": "Amazon"
                })
            except:
                continue
        return products
    except Exception as e:
        print(f"Amazon Error: {e}")
        return []