import requests
import os
from dotenv import load_dotenv
import json

def get_schema():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
    }
    
    res = requests.get(f"{url}/rest/v1/", headers=headers)
    if res.status_code == 200:
        schema = res.json()
        with open("supabase_schema.json", "w") as f:
            json.dump(schema, f, indent=2)
        print("Schema saved to supabase_schema.json")
        
        # Extract marketplace_orders columns
        tables = schema.get("definitions", {})
        if "marketplace_orders" in tables:
            cols = tables["marketplace_orders"].get("properties", {}).keys()
            print(f"marketplace_orders columns: {list(cols)}")
        else:
            print("marketplace_orders not found in schema definitions.")
    else:
        print(f"Error: {res.status_code} - {res.text}")

if __name__ == "__main__":
    get_schema()
