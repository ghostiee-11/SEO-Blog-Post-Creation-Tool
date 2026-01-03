import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_seo_strategy(title, details):
    prompt = f"""
    Act as an SEO Expert. Analyze:
    Product: {title}
    Context: {details[:500]}
    
    Return JSON ONLY:
    {{
        "primary_keyword": "High volume keyword",
        "secondary_keywords": ["keyword 1", "keyword 2", "keyword 3"],
        "target_audience": "Who buys this?",
        "intent": "Transactional or Informational"
    }}
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"SEO Error: {e}")
        return None