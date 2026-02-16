import MetaTrader5 as mt5
import os
import sys

def test_mt5():
    print("--- MT5 DIAGNOSTIC ---")
    init_res = mt5.initialize()
    print(f"1. mt5.initialize(): {init_res}")
    
    if init_res:
        t_info = mt5.terminal_info()
        print(f"2. mt5.terminal_info(): {'FOUND' if t_info else 'NONE'}")
        if t_info:
            print(f"   - Connected to server: {t_info.connected}")
            print(f"   - Trade allowed (Algo): {t_info.trade_allowed}")
            print(f"   - Path: {t_info.path}")
        
        a_info = mt5.account_info()
        print(f"3. mt5.account_info(): {'FOUND' if a_info else 'NONE'}")
        if a_info:
            print(f"   - Login (ID): {a_info.login}")
            print(f"   - Server: {a_info.server}")
            print(f"   - Balance: {a_info.balance}")
        
        mt5.shutdown()
    else:
        print(f"!! MT5 Init Error: {mt5.last_error()}")

def test_telegram():
    print("\n--- TELEGRAM DIAGNOSTIC ---")
    session_file = "itc_copier_session.session"
    exists = os.path.exists(session_file)
    print(f"1. Session file '{session_file}': {'EXISTS' if exists else 'NOT FOUND'}")
    
    # Try check env
    from dotenv import load_dotenv
    load_dotenv()
    api_id = os.getenv("TG_API_ID")
    api_hash = os.getenv("TG_API_HASH")
    print(f"2. Env Config: API_ID={'SET' if api_id else 'MISSING'}, API_HASH={'SET' if api_hash else 'MISSING'}")

if __name__ == "__main__":
    test_mt5()
    test_telegram()
