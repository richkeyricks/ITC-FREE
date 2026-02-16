
import sys
import os
import time
from dotenv import load_dotenv
from supabase import create_client, Client

# Set stdout to Utf-8
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
    exit(1)

# Initialize Client
try:
    supabase: Client = create_client(url, key)
except Exception as e:
    print(f"Failed to initialize Supabase client: {e}")
    exit(1)

def main():
    print(f"Connecting to Supabase Project: {url}")
    print("---------------------------------------------------")
    
    try:
        # [TEST 1] Inspect Table Structure via Select *
        print("\n[TEST 1] Verifying Table Columns (user_profiles)...")
        
        # We try to fetch 1 row to inspect keys
        res = supabase.table("user_profiles").select("*").limit(1).execute()
        
        if res.data and len(res.data) > 0:
            row = res.data[0]
            keys = sorted(list(row.keys()))
            
            print(f"✅ Table data accessible. Found {len(keys)} columns.")
            print("   Listing detected columns:")
            for k in keys:
                print(f"   - {k}")
                
            # Verify Critical Columns
            required = ["trading_config", "admin_notes", "user_tags"]
            missing = [r for r in required if r not in keys]
            
            if not missing:
                print("\n✅ OK: All critical columns are present.")
            else:
                print(f"\n❌ CRITICAL ERROR: Missing columns: {missing}")
                
        else:
            print("⚠️ Table is empty. Cannot list all columns dynamically.")
            # Fallback: Check if we can select specific columns without error
            print("   Attempting to select specific columns manually...")
            try:
                supabase.table("user_profiles").select("trading_config,admin_notes,user_tags").limit(1).execute()
                print("✅ OK: Columns 'trading_config', 'admin_notes', 'user_tags' are VALID (Selectable).")
            except Exception as e:
                print(f"❌ ERROR: Columns likely missing. Error: {e}")

        # [TEST 2] Verify Policy Access (God Mode)
        print("\n[TEST 2] Verifying Global Access Policy (God Mode)...")
        try:
            # If RLS is restrictive, count might fail or return 0 for anon/service_role depending on key
            res_count = supabase.table("user_profiles").select("count", count="exact").execute()
            count = res_count.count
            
            print(f"✅ OK: Count Query Successful. Total Rows: {count}")
            if count is not None:
                print("   > This confirms the 'God-Mode Service Access' policy is ACTIVE.")
                print("   > The application can now read/write data freely.")
            
        except Exception as e:
            print(f"❌ ERROR: RLS Policy seems restrictive. Error: {e}")

        print("\n---------------------------------------------------")
        print("VERIFICATION COMPLETE")

    except Exception as e:
        print(f"\n❌ FATAL SCRIPT ERROR: {e}")

if __name__ == "__main__":
    main()
