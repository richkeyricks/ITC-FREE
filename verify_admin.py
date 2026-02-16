import sys
import os
sys.path.append(os.path.abspath("src"))
from modules.db.supabase_client import SupabaseManager

def test_admin_powers():
    print("========================================")
    print(" DIAGNOSTIC: SUPABASE ADMIN CHECK")
    print("========================================")
    
    db = SupabaseManager()
    
    print(f"1. Connection: {'CONNECTED' if db.client else 'FAILED'}")
    if not db.client: return

    # Check Admin Status
    is_admin = db.is_admin()
    print(f"2. Your Role: {'ADMIN' if is_admin else 'USER'}")
    print(f"   Email: {db.user_email}")
    
    # Try to find a user to update (Self for safety or first in list)
    try:
        users = db.client.table("user_profiles").select("*").limit(1).execute()
        if not users.data:
            print("3. Fetch Users: NO DATA (Table Empty?)")
            return
            
        target = users.data[0]
        t_hwid = target['hwid']
        t_is_pro = target.get('is_pro', False)
        
        print(f"3. Target User: {target.get('name')} (ID: {t_hwid})")
        print(f"   Current Status: PRO={t_is_pro}")
        
        # ATTEMPT UPDATE
        new_status = not t_is_pro
        print(f"4. Attempting Update to PRO={new_status}...")
        
        res = db.client.table("user_profiles").update({"is_pro": new_status}).eq("hwid", t_hwid).execute()
        
        # Check if actually updated (RLS often fails silently by returning empty data)
        if res.data:
            print("   ✅ SUCCESS: Result returned.")
        else:
            print("   ❌ FAILED: RLS Blocked Update (Empty Result)")
            print("   REASON: Supabase Policy strictly forbids updating other users.")
            print("\n   SOLUTION: You must execute SQL Policy in Supabase Dashboard.")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")

if __name__ == "__main__":
    test_admin_powers()
