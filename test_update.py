
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add source to path
sys.path.append(os.path.join(os.getcwd(), "src"))

load_dotenv()

from modules.db.supabase_client import SupabaseManager

def test_update():
    db = SupabaseManager()
    
    print(f"User ID: {db.user_id}")
    if db.user_id == "anonymous":
        print("Cannot test update as anonymous user.")
        return

    # Calculate expiry
    now = datetime.now()
    new_expiry = now + timedelta(days=30)
    iso_expiry = new_expiry.isoformat()
    
    print(f"Attempting update with expiry: {iso_expiry}")
    
    try:
        # Try 'premium_until' instead of 'subscription_expiry'
        data = {"premium_until": iso_expiry}
        res = db.client.table("user_profiles").update(data).eq("hwid", db.user_id).execute()
        print(f"Update Result: {res}")
        if res.data:
            print("SUCCESS! Data updated.")
        else:
            print("FAILED! No data returned (RLS blocked?).")
            
    except Exception as e:
        print(f"Update Exception: {e}")
        # Print attributes if possible
        if hasattr(e, 'code'): print(f"Error Code: {e.code}")
        if hasattr(e, 'details'): print(f"Error Details: {e.details}")
        if hasattr(e, 'message'): print(f"Error Message: {e.message}")

if __name__ == "__main__":
    test_update()
