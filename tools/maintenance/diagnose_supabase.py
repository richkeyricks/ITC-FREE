import requests
import os
from dotenv import load_dotenv

def check_supabase():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use service role key for inspection
    
    if not url or not key:
        print("Missing Supabase credentials in .env")
        return

    tables = ["marketplace_orders", "entitlements", "user_profiles", "user_wallets", "affiliate_referrals"]
    
    for table in tables:
        endpoint = f"{url}/rest/v1/{table}?select=*&limit=1"
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                print(f"Table '{table}' exists. Rows: {len(response.json())}")
            else:
                print(f"Table '{table}' error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error checking table '{table}': {e}")

if __name__ == "__main__":
    check_supabase()
