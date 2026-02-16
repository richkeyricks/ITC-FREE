import os 
import sys
sys.path.insert(0, "src")
from modules.db.supabase_client import SupabaseManager

try:
    db = SupabaseManager()
    donations = db.get_donations()
    print(f"DEBUG: Found {len(donations)} donations in DB")
    for d in donations:
        print(f"Donor: {d.get('name')} | Amount: {d.get('amount')} | Message: {d.get('message')}")
except Exception as e:
    print(f"Error: {e}")
