import os
from supabase import create_client, Client
from dotenv import load_dotenv

def verify_data():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use service role key to see everything
    
    if not url or not key:
        print("Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")
        return

    print(f"Connecting to: {url}")
    supabase: Client = create_client(url, key)
    
    try:
        # Check user_profiles with *
        res = supabase.table("user_profiles").select("*").limit(1).execute()
        
        if res.data:
            print("\n--- User Profiles Schema ---")
            print(f"Columns found: {list(res.data[0].keys())}")
            
            # Fetch samples now that we know columns (limit 5)
            # Fetch samples now that we know columns (limit 5)
            res_all = supabase.table("user_profiles").select("*").limit(5).execute()
            print("\n--- User Profiles Data (Sample) ---")
            for row in res_all.data:
                print(row)
        else:
            print("No data found in user_profiles.")
            
        # Check entitlements if table exists
        try:
            res_e = supabase.table("entitlements").select("*").limit(5).execute()
            if res_e.data:
                print("\n--- Entitlements Data (Sample) ---")
                print(res_e.data)
        except:
            print("\nEntitlements table might not exist or is inaccessible.")

    except Exception as e:
        print(f"Error querying Supabase: {e}")

if __name__ == "__main__":
    verify_data()
