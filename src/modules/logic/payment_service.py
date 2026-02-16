# ══════════════════════════════════════════════════════════════════════════════
# 🏦 PAYMENT SERVICE (LOGIC LAYER)
# 🛡️ SECURITY: ZERO-LEAK (No API Keys in this file)
# ══════════════════════════════════════════════════════════════════════════════

import requests
import json
import uuid
import webbrowser
from index import (get_env_list)  # Using existing env loader if needed
from constants.api_endpoints import EDGE_FUNCTION_URL, SNAPSHOT_API

# --- CONSTANTS ---
# Ideally, this URL comes from src/configs or src/constants
# For now, we define it here based on the Plan, but will move to configs later.
DEFAULT_EDGE_URL = EDGE_FUNCTION_URL if 'EDGE_FUNCTION_URL' in globals() else "https://YOUR_PROJECT_ID.supabase.co/functions/v1/payment-gateway"

class PaymentService:
    """
    Handles secure communication with the Payment Gateway Edge Function.
    Ensures NO Midtrans Server Key is ever handled by the client.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.edge_url = DEFAULT_EDGE_URL

    def create_transaction(self, preset_id, preset_name, amount, currency="IDR", on_success=None):
        """
        1. Generates unique Order ID.
        2. Calls Vercel Serverless API (Secure) to generate Snap Token.
        3. Returns Snap Token & Bridge URL for Vercel.
        4. Starts Monitoring Thread with optional callback.
        """
        try:
            # 1. Unique Order ID
            order_id = f"ORDER-{uuid.uuid4().hex[:8].upper()}" 
            
            # 2. Call Haineo Vercel API (Node.js Serverless)
            # This keeps SERVER_KEY hidden from the Desktop App
            VERCEL_API = "https://telegramcopytrade.vercel.app/api/pay"
            
            payload = {
                "order_id": order_id,
                "amount": int(amount),
                "currency": currency.upper(),
                "preset_name": f"{preset_name[:40]} ({currency.upper()})",
                "customer_email": "trader@haineo.ai" # In production, fetch from user state
            }

            # 3. Request Token from Vercel
            response = requests.post(VERCEL_API, json=payload, timeout=15)
            data = response.json()

            if response.status_code not in [200, 201]:
                error_msg = data.get('error', 'Unknown Vercel API Error')
                print(f"// Vercel API Error ({response.status_code}): {data}")
                return False, f"API Error ({response.status_code}): {error_msg}"

            # 4. Success -> Sync Initial State to DB (Enterprise Bridge)
            db_order = {
                "order_id": order_id,
                "preset_id": str(preset_id),
                "preset_name": preset_name,
                "amount": float(amount),
                "status": "PENDING"
            }
            if hasattr(self.db_manager, 'create_order'):
                self.db_manager.create_order(db_order)

            # 5. Start Realtime Monitoring
            self.start_monitoring(order_id, on_success)

            # 6. Return Bridge URL
            bridge_url = f"https://telegramcopytrade.vercel.app/pay?token={data.get('token')}&id={order_id}"
            
            return True, {
                "token": data.get("token"),
                "redirect_url": bridge_url,
                "order_id": order_id
            }

        except Exception as e:
            return False, f"Connection Failed: {str(e)}"

    def start_monitoring(self, order_id, on_success=None):
        """Spawns a background thread to listen for Supabase/Midtrans updates"""
        import threading
        import time
        
        def _listen():
            print(f"// STARTED Monitoring Order: {order_id} (Duration: 3m)")
            for _ in range(60): # Monitor for 3 minutes (60 * 3s)
                time.sleep(3)
                
                # A. Check Supabase (Priority: Enterprise Bridge)
                status = "UNKNOWN"
                if hasattr(self.db_manager, 'get_order_status'):
                    status = self.db_manager.get_order_status(order_id)
                
                # B. Fallback to Direct Poll if Supabase is still PENDING (Double Check)
                if status == "PENDING" or status == "UNKNOWN":
                   status = self.check_payment_status(order_id) # The direct poll method
                   
                if status == "SUCCESS":
                    print(f"✅ PAYMENT SUCCESS DETECTED FOR {order_id}")
                    # Callback Trigger
                    if on_success:
                        try:
                            # Run on main thread if possible, or straight execution
                            # Logic layer is thread-agnostic, caller handles dispatch
                            on_success()
                        except Exception as cb_err:
                            print(f"Callback Error: {cb_err}")
                    break
                elif status == "FAILED":
                    print(f"❌ Payment Failed for {order_id}")
                    break
                    
        threading.Thread(target=_listen, daemon=True).start()

    def open_payment_browser(self, redirect_url):
        """
        Opens the Snap Payment Page in the default system browser.
        Fallback if WebView is not available.
        """
        try:
            webbrowser.open(redirect_url)
            return True, "Browser Opened"
        except Exception as e:
            return False, str(e)

    def check_payment_status(self, order_id):
        """
        Polls the database OR calls Midtrans directly (Hybrid Mode).
        For Desktop Sandbox, we call Midtrans API directly to bypass Webhook requirement.
        """
        try:
            # 1. Direct API Check (Sandbox/Trial Mode)
            import base64
            from configs.payment_config import STATUS_BASE_URL, SERVER_KEY
            
            # Construct Status URL
            status_url = f"{STATUS_BASE_URL}/{order_id}/status"
            
            auth_string = f"{SERVER_KEY}:"
            auth_bytes = auth_string.encode('ascii')
            base64_auth = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Basic {base64_auth}"
            }
            
            response = requests.get(status_url, headers=headers, timeout=10)
            
            # Defensive JSON parsing
            if response.status_code != 200:
                print(f"// Status Check Warning ({response.status_code}): {response.text[:100]}")
                return "PENDING"
                
            data = response.json()
            
            if response.status_code == 404:
                return "PENDING" # Not found usually means not paid yet or just created
            
            # Map Midtrans Status to App Status
            transaction_status = data.get("transaction_status")
            fraud_status = data.get("fraud_status")
            
            if transaction_status == "capture":
                if fraud_status == "challenge":
                    return "CHALLENGE"
                return "SUCCESS"
            elif transaction_status == "settlement":
                return "SUCCESS"
            elif transaction_status in ["deny", "cancel", "expire"]:
                return "FAILED"
            elif transaction_status == "pending":
                return "PENDING"
            
            return "UNKNOWN"

        except Exception as e:
            print(f"Status Check Error: {e}")
            return "UNKNOWN"
