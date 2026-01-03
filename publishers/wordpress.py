import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def publish_to_wordpress(title, content, tags, product_link):
    """
    Publishes the blog post to a WordPress site via REST API.
    """
    url = os.getenv("WP_API_URL")
    user = os.getenv("WP_USERNAME")
    password = os.getenv("WP_APP_PASSWORD")

    if not url or not user or not password:
        return {"success": False, "error": "Missing WordPress credentials in .env"}

    # Create Basic Auth Header
    creds = f"{user}:{password}"
    token = base64.b64encode(creds.encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    # Prepare Data
    # We append the product link at the bottom as a CTA
    final_content = content + f'\n\n<p><a href="{product_link}" target="_blank" rel="nofollow">Check Current Price</a></p>'
    
    post_data = {
        "title": title,
        "content": final_content,
        "status": "publish",  # Change to 'draft' if you want to review first
        "tags": tags if tags else []
    }

    try:
        response = requests.post(f"{url}/posts", headers=headers, json=post_data)
        if response.status_code == 201:
            return {"success": True, "link": response.json().get('link')}
        else:
            return {"success": False, "error": f"Status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}