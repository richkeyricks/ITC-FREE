import os
import requests
import json
from dotenv import load_dotenv

# Load credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use Service Key for full access

def query_supabase_sql(query):
    endpoint = f"{SUPABASE_URL}/rest/v1/"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "params=single-objective"
    }
    
    # Using the /rpc/api_sql (if it exists) or just generic REST for schema
    # Actually, standard REST can't do arbitrary SQL. 
    # We need to use the PostgREST features to list tables.
    
    print(f"// Auditing Supabase: {SUPABASE_URL}")
    
    # 1. List Tables via PostgREST
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers=headers)
        if response.status_code == 200:
            print("// Live Tables & Column Audit:")
            specs = response.json()
            definitions = specs.get('definitions', {})
            
            target_tables = ['marketplace_orders']
            for table in target_tables:
                if table in definitions:
                    print(f"\n--- TABLE: {table} ---")
                    props = definitions[table].get('properties', {})
                    for col, detail in props.items():
                        col_type = detail.get('type')
                        col_format = detail.get('format', '')
                        print(f"  - {col}: {col_type} ({col_format})")
                else:
                    print(f"\n!! MISSING TABLE: {table}")
        else:
            print(f"!! Error listing tables: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"!! Request error: {e}")

if __name__ == "__main__":
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("!! Missing Supabase credentials in .env")
    else:
        query_supabase_sql("")
