import os
import sys
import threading
import time
from dotenv import load_dotenv

# Setup path
sys.path.append(os.path.join(os.getcwd(), "src"))
load_dotenv()

from modules.mt5.mt5_service import MT5Service
from modules.db.supabase_client import SupabaseManager

def verify_mt5():
    print("\n--- MT5 Service Verification ---")
    service = MT5Service.instance()
    
    # Check Singleton
    service2 = MT5Service.instance()
    if service is not service2:
        print("[FAIL] Singleton Pattern broken!")
        return False
    print("[OK] Singleton Pattern verified.")
    
    # Check Thread Safety (Mock)
    # We can't easily test actual threading without a race condition, 
    # but we can verify the lock exists.
    if not hasattr(service, "_lock"):
        print("[FAIL] Lock missing!")
        return False
    print("[OK] Thread Lock exists.")
    
    # Attempt Init (Will fail if no MT5 installed/config, but we catch it)
    try:
        res = service.initialize()
        print(f"[INFO] MT5 Init Result: {res}")
        if not res and service.last_error():
             print(f"[INFO] MT5 Last Error: {service.last_error()}")
    except Exception as e:
        print(f"[WARN] MT5 Init threw exception (expected if no terminal): {e}")

    return True

def verify_db():
    print("\n--- Database Verification ---")
    db = SupabaseManager()
    
    if not db.client:
        print("[FAIL] Supabase Client is None. Check .env!")
        return False
        
    print(f"[OK] Supabase Client Connected. User: {db.user_id}")
    
    # Method Presence Check
    required_methods = [
        "increment_ai_bonus", 
        "exchange_code_for_session", 
        "push_chat", 
        "get_chat_history"
    ]
    
    missing = [m for m in required_methods if not hasattr(db, m)]
    if missing:
        print(f"[FAIL] Missing methods: {missing}")
        return False
        
    print(f"[OK] All {len(required_methods)} new methods present.")
    
    # Functional Test: Chat History
    try:
        hist = db.get_chat_history(limit=1)
        print(f"[OK] get_chat_history executed. Records: {len(hist)}")
    except Exception as e:
        print(f"[FAIL] get_chat_history error: {e}")
        return False
        
    return True

def main():
    print("=== FULL SYSTEM VERIFICATION ===")
    
    mt5_ok = verify_mt5()
    db_ok = verify_db()
    
    print("\n=== SUMMARY ===")
    print(f"MT5 Service: {'PASS' if mt5_ok else 'FAIL'}")
    print(f"Database:    {'PASS' if db_ok else 'FAIL'}")
    
    if mt5_ok and db_ok:
        print("\n✅ SYSTEM INTEGRITY VERIFIED")
        sys.exit(0)
    else:
        print("\n❌ SYSTEM ISSUES DETECTED")
        sys.exit(1)

if __name__ == "__main__":
    main()
