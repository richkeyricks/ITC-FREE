import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

if not URL or not KEY:
    print("Error: Missing SUPABASE_URL or SUPABASE_KEY in .env")
    exit(1)

TABLES = ["user_profiles", "marketplace_orders", "entitlements", "user_presets", "activity_logs", "logs"]

print(f"=== STC DATABASE AUDIT DEEP-DIVE ===\n")

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
}

for table in TABLES:
    print(f"--- TABLE: {table} ---")
    try:
        # Fetch one row to inspect keys
        res = requests.get(f"{URL}/rest/v1/{table}?limit=1", headers=headers)
        if res.status_code == 200:
            data = res.json()
            if data:
                cols = sorted(list(data[0].keys()))
                print(f"  Columns found ({len(cols)}):")
                for c in cols:
                    val = data[0][c]
                    print(f"    - {c} (Example: {val} [{type(val).__name__}])")
            else:
                print("  Table is EMPTY. Trying to fetch schema via OPTIONS...")
                # Fallback: simple OPTIONS call might work on some PostgREST setups
                res_opt = requests.options(f"{URL}/rest/v1/{table}", headers=headers)
                print(f"  Status: {res_opt.status_code}")
        elif res.status_code == 404:
            print("  [MISSING] Table not found.")
        else:
            print(f"  [ERROR] {res.status_code}: {res.text}")
    except Exception as e:
        print(f"  [EXCEPTION] {e}")
    print("\n" + "="*40 + "\n")
