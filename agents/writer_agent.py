import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def write_blog_post(product, seo_data, details):
    kw_str = ", ".join(seo_data['secondary_keywords'])
    
    prompt = f"""
    Write a high-converting Blog Review (Markdown format).
    
    Product: {product['title']}
    Price: {product['price']}
    Details: {details[:800]}
    
    SEO DATA:
    - Focus Keyword: {seo_data['primary_keyword']}
    - Keywords to include: {kw_str}
    - Audience: {seo_data['target_audience']}
    
    Structure:
    1. H1 Title (Catchy)
    2. Introduction (The Hook)
    3. Key Features (Use bullet points)
    4. Pros & Cons
    5. Conclusion
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content