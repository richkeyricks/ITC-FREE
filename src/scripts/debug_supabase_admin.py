
import os
import sys
from supabase import create_client

# Define Config (Use Service Role Key to Bypass RLS)
URL = ""
SERVICE_KEY = ""  # From .env line 55

def check_db():
    print(f"Connecting to {URL} with SERVICE ROLE KEY...")
    client = create_client(URL, SERVICE_KEY)
    
    email = "richkeyrick@gmail.com"
    user_id = "55b7f9ce-55e3-4822-8efe-a34822f394d2"
    
    print(f"\nScanning for {email} / {user_id}...")
    
    # Check Profile
    try:
        res = client.table("user_profiles").select("name,email,hwid").eq("hwid", user_id).execute()
        print(f"Profiles Found: {len(res.data)}")
        
        if res.data:
            p = res.data[0]
            print("\n" + "="*40)
            print(f"NAME:  {p.get('name')}")
            print(f"EMAIL: {p.get('email')}")
            print(f"HWID:  {p.get('hwid')}")
            print("="*40 + "\n")
        else:
             print("NO PROFILE FOUND!")

        
    except Exception as e:
        print(f"Error checking DB: {e}")

if __name__ == "__main__":
    check_db()
