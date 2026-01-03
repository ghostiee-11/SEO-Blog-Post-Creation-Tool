import requests
from bs4 import BeautifulSoup
from utils.headers import get_headers

def search_ebay(query=None):
    """
    Scrapes eBay.
    If query -> Search Results.
    If None -> Global Deals (Tech).
    """
    if query:
        url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
    else:
        url = "https://www.ebay.com/globaldeals/tech"
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        products = []
        
        if query:
            items = soup.find_all("div", class_="s-item__wrapper", limit=8)
        else:
            items = soup.find_all("div", class_="dne-itemtile-detail", limit=8)
        
        for item in items:
            try:
                if query:
                    title = item.find("div", class_="s-item__title").get_text(strip=True)
                    if "Shop on eBay" in title: continue
                    price = item.find("span", class_="s-item__price").get_text(strip=True)
                    img = item.find("div", class_="s-item__image-wrapper").find("img")['src']
                    link = item.find("a", class_="s-item__link")['href']
                else:
                    title = item.find("h3", class_="dne-itemtile-title").get_text(strip=True)
                    price = item.find("span", class_="first").get_text(strip=True)
                    # Image is often lazy loaded or complex on deals page, using placeholder or finding specific class
                    img_container = item.parent.find("div", class_="dne-itemtile-imagewrapper")
                    img = img_container.find("img")['src'] if img_container else "https://via.placeholder.com/150"
                    link = item.find("a", href=True)['href']

                products.append({
                    "title": title,
                    "price": price,
                    "image": img,
                    "url": link,
                    "source": "eBay"
                })
            except:
                continue
        return products
    except Exception as e:
        print(f"eBay Error: {e}")
        return []

def get_ebay_details(url):
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        desc = soup.find("div", class_="x-about-this-item")
        if not desc:
            desc = soup.find("div", class_="ux-layout-section-evo__item")
        return desc.get_text(strip=True)[:1000] if desc else "Details unavailable."
    except:
        return "Could not fetch details."