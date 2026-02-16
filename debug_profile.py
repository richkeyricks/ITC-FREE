
import os
import sys
from dotenv import load_dotenv

# Add source to path
sys.path.append(os.path.join(os.getcwd(), "src"))

load_dotenv()

from modules.db.supabase_client import SupabaseManager

def inspect_profile():
    db = SupabaseManager()
    
    # Try to find the user 'technolog' or list recent profiles
    print("Fetching profiles...")
    try:
        # Fetch all profiles to find the one matching 'technolog'
        res = db.client.table("user_profiles").select("*").execute()
        found = False
        for p in res.data:
            name = str(p.get('name', '') or '').lower()
            email = str(p.get('email', '') or '').lower()
            if 'technolog' in name or 'technolog' in email:
                print(f"FOUND USER: {name} ({email})")
                print(f"  Tier: {p.get('subscription_tier')}")
                print(f"  Plan: {p.get('subscription_plan')}") 
                # CORRECT COLUMN: 'premium_until'
                print(f"  Expiry (premium_until): {p.get('premium_until')}")
                print(f"  Full Profile: {p}")
                found = True
                
        if not found:
            print("User 'technolog' not found in profiles.")
            # Print first 5 for context
            for p in res.data[:5]:
                print(f"  - {p.get('name')} ({p.get('email')})")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_profile()
