import os
import json
import base64
import requests
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()

SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY", "").strip()
CLIENT_KEY = os.getenv("MIDTRANS_CLIENT_KEY", "").strip()
IS_PRODUCTION = True  # We are auditing production

def test_midtrans_connectivity():
    print("🚀 [MIDTRANS DIAGNOSTIC] Starting God-Mode Inspection...")
    
    if not SERVER_KEY:
        print("❌ ERROR: MIDTRANS_SERVER_KEY is missing in .env")
        return

    # 1. Prepare Authorization Header
    # Base64(ServerKey + ":")
    merchant_id = "G440832689" # From user screenshot
    auth_str = f"{SERVER_KEY}:"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}",
        "X-Merchant-Id": merchant_id # Some accounts REQUIRE this for Production
    }

    # 1. Test Key Health (Core API - Transaction Status)
    # Using a fake order ID just to check Auth
    core_url = f"https://api.midtrans.com/v2/FAKE-ORDER-{os.urandom(2).hex().upper()}/status"
    print(f"📡 Testing CORE API (Authentication Check)...")
    try:
        core_resp = requests.get(core_url, headers=headers, timeout=10)
        print(f"DEBUG: Core Status: {core_resp.status_code}")
        if core_resp.status_code == 401:
            print("❌ CORE API REJECTED: Server Key is invalid or not active for Production.")
            print(f"DEBUG: Response: {core_resp.text}")
        elif core_resp.status_code == 404:
            print("✅ CORE API ACCEPTED: Key is valid (Received 404 for non-existent order as expected).")
        else:
            print(f"⚠️ CORE API RESPONSE: {core_resp.status_code} - {core_resp.text}")
    except Exception as e:
        print(f"❌ CORE API CONNECTION FAILED: {str(e)}")

    # 2. Test Transaction (Snap API)
    base_url = "https://app.midtrans.com/snap/v1/transactions"
    
    payload = {
        "transaction_details": {
            "order_id": f"ITC-TEST-{os.urandom(4).hex().upper()}",
            "gross_amount": 10000 
        }
    }

    print(f"\n📡 Testing SNAP API Production...")
    try:
        response = requests.post(base_url, headers=headers, json=payload, timeout=10)
        
        print(f"DEBUG: Snap Status Code: {response.status_code}")
        print(f"DEBUG: Snap Response Body: {response.text}")

        if response.status_code == 201:
            data = response.json()
            print("✅ SUCCESS: Midtrans Snap API accepted the keys!")
            print(f"🔗 Token Generated: {data.get('token')}")
            return True
        elif response.status_code == 401:
            print(f"❌ SNAP API REJECTED (401).")
            return False
        else:
            print(f"⚠️ STATUS {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ SNAP API CONNECTION FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_midtrans_connectivity()
    if success:
        print("\n🏆 RESULT: Midtrans Configuration is VALID and LIVE.")
    else:
        print("\n💀 RESULT: Midtrans Configuration is BROKEN.")
