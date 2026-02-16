import os
import sys
from dotenv import load_dotenv

# Setup path to src
sys.path.append(os.path.join(os.getcwd(), "src"))

# Load Env
load_dotenv()

from modules.db.supabase_client import SupabaseManager

def test_supabase_methods():
    print("--- Testing Supabase Connection & Methods ---")
    db = SupabaseManager()
    
    if not db.client:
        print("[FAIL] Client not initialized. Check .env")
        return

    # 1. Mock Login (We need a user_id to test user methods)
    # We'll use a known test ID if available, or just skip if anonymous
    if db.user_id == "anonymous":
        print("[WARN] User is anonymous. Some tests will be skipped.")
        # Try to use a dummy ID for testing IF it's safe (e.g., self-test)
        # db.user_id = "test_user_hwid" 

    # 2. Test get_chat_history (Should return empty list or data, but not crash)
    print("\n[TEST] get_chat_history...")
    try:
        hist = db.get_chat_history(limit=2)
        print(f"   Success. Records found: {len(hist)}")
    except Exception as e:
        print(f"   [FAIL] {e}")

    # 3. Test push_chat (Only if we have a user)
    if db.user_id != "anonymous":
        print("\n[TEST] push_chat...")
        try:
            db.push_chat("user", "Test message from verification script")
            print("   Success. Message pushed.")
        except Exception as e:
            print(f"   [FAIL] {e}")

    # 4. Test increment_ai_bonus (RPC)
    if db.user_id != "anonymous":
        print("\n[TEST] increment_ai_bonus...")
        try:
            res = db.increment_ai_bonus(1)
            print(f"   Result: {res}")
        except Exception as e:
            print(f"   [FAIL] {e}")
            
    # 5. Test exchange_code_for_session (Dry run only)
    print("\n[TEST] exchange_code_for_session (Signature Check)...")
    if hasattr(db, "exchange_code_for_session"):
        print("   [OK] Method exists.")
    else:
        print("   [FAIL] Method MISSING.")

if __name__ == "__main__":
    test_supabase_methods()
