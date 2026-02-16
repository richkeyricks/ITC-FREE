import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_serper():
    api_key = os.getenv("SERPER_API_KEY")
    print(f"API Key found: {bool(api_key)}")
    
    # Simulate user input
    raw_query = "berita ekonomi hari ini"
    symbol = "BTCUSDm"

    # 1. Sanitize Symbol (Matches smart_fill.py logic)
    import re
    clean_symbol = re.sub(r'[^a-zA-Z0-9]', '', symbol).upper()
    if clean_symbol.endswith('M') and len(clean_symbol) > 3:
        clean_symbol = clean_symbol[:-1]

    # 2. Build Query (Matches smart_fill.py logic)
    if raw_query and any(k in raw_query.lower() for k in ["berita viral", "kejadian", "terbaru", "hari ini"]):
        query = f"{raw_query} forex trading indonesia"
    else:
        query = f"berita terbaru {clean_symbol} forex trading"

    print(f"Original Symbol: {symbol}")
    print(f"Clean Symbol: {clean_symbol}")
    print(f"Final Query: {query}")

    url = "https://google.serper.dev/news"
    payload = json.dumps({
        "q": query,
        "num": 5,
        "gl": "id",
        "hl": "id",
        "tbs": "qdr:d"
    })
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    try:
        print("Sending request to Serper...")
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("News found:")
            print(json.dumps(data.get("news", []), indent=2))
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_serper()
