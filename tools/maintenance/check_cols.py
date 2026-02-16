import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
}

print("=== SEARCHING COLUMNS IN user_profiles ===\n")

res = requests.get(f"{URL}/rest/v1/user_profiles?limit=1", headers=headers)
if res.status_code == 200:
    data = res.json()
    if data:
        cols = sorted(list(data[0].keys()))
        search_terms = ["coin", "balance", "premium", "until", "pro", "subscription"]
        for c in cols:
            if any(term in c.lower() for term in search_terms):
                print(f"  FOUND: {c} = {data[0][c]}")
        
        # Check specific ones requested by code
        target_cols = ["coins", "premium_until", "balance", "is_pro", "subscription_tier"]
        print("\n--- Direct Check ---")
        for tc in target_cols:
            status = "PRESENT" if tc in cols else "MISSING"
            print(f"  {tc}: {status}")
    else:
        print("Table is empty, cannot inspect columns via data.")
else:
    print(f"Error {res.status_code}: {res.text}")
