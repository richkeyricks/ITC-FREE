import requests
import os
from dotenv import load_dotenv
import json

def inspect():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
    }
    
    tables = ["marketplace_presets", "marketplace_orders", "entitlements", "user_profiles"]
    
    for table in tables:
        print(f"\n--- Table: {table} ---")
        res = requests.get(f"{url}/rest/v1/{table}?select=*", headers=headers)
        if res.status_code == 200:
            data = res.json()
            if data:
                print(json.dumps(data[0], indent=2))
                print(f"Total rows: {len(data)}")
            else:
                print("Table is empty.")
        else:
            print(f"Error: {res.status_code} - {res.text}")

if __name__ == "__main__":
    inspect()
