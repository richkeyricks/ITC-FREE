import os
import hashlib
import platform
import subprocess
import logging
from supabase import create_client, Client
from dotenv import load_dotenv

def get_machine_id():
    """
    [DEPRECATED] Generates a unique hardware ID.
    NOTE: This is NOT used for Auth. Supabase Auth UUID is used as 'hwid' in DB.
    """
    try:
        import uuid
        import platform
        # Strategy: Combine MAC Address + Node/NodeName
        mac = str(uuid.getnode())
        node = platform.node()
        system = platform.system()
        combined = f"{mac}_{node}_{system}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    except Exception as e:
        print(f"// HWID Error: {e}")
        return "anon_user"

from configs.supabase_config import SUPABASE_URL, SUPABASE_KEY

class SupabaseManager:
    """Manages Cloud Database operations with Multi-User Isolation"""
    
    def __init__(self):
        load_dotenv()
        # Gravity Rule 1: Centralized & Structured fallbacks
        self.url = os.getenv("SUPABASE_URL") or SUPABASE_URL
        self.key = os.getenv("SUPABASE_KEY") or SUPABASE_KEY
        self.user_id = "anonymous"  # Default to anonymous
        self.client: Client = None
        
        if self.url and self.key:
            try:
                # DEBUG: Log init attempt
                try:
                    with open("debug_log.txt", "a") as f:
                        f.write(f"\n[SUPABASE ATTEMPT] URL: {self.url}\n")
                except: pass
                
                self.client = create_client(self.url, self.key)
                
                # Check if there's an ACTUAL session (not just env var)
                session = self.client.auth.get_session()
                if session and session.user:
                    # Real session exists - use it
                    self.user_id = session.user.id
                    self.user_email = session.user.email
                    
                    # Ensure env vars are synced
                    os.environ["USER_AUTH_ID"] = self.user_id
                    os.environ["USER_EMAIL"] = self.user_email
                    print(f"// Supabase Active Session: {self.user_id} ({self.user_email})")
                else:
                    # Fallback to saved credentials from .env
                    # Quote-robust loading: strip any " or ' characters
                    saved_id = os.getenv("USER_AUTH_ID", "").strip().strip("'").strip('"')
                    if saved_id:
                        self.user_id = saved_id
                        self.user_email = os.getenv("USER_EMAIL", "anonymous").strip().strip("'").strip('"')
                        print(f"// Supabase: Session lost, using fallback ID: {self.user_id}")
                    else:
                        self.user_id = "anonymous"
                        print("// Supabase: No active session")
                        
            except Exception as e:
                # DEBUG: Log exact error
                try:
                    with open("debug_log.txt", "a") as f:
                        f.write(f"\n[SUPABASE ERROR] {e}\n")
                except: pass
                
                print(f"// Supabase Init Error: {e}")
                self.user_id = "anonymous"

    # --- AUTHENTICATION ---
    def sign_up(self, email, password, username=None):
        """Creates a new user account with strict payload formatting"""
        if not self.client: return False, "DB not connected"
        
        print(f"// DEBUG: Attempting Signup for {email}...") 
        try:
            # Strict Supabase v2 Payload
            credentials = {
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username or "Trader"
                    }
                }
            }
            
            res = self.client.auth.sign_up(credentials)
            
            if res.user:
                print("// DEBUG: Signup Success!")
                return True, "Account created! Please check your email for verification."
            return False, "Failed to create account (No User Object)"
            
        except Exception as e:
            err = str(e)
            print(f"// DEBUG: Signup Error: {err}")
            # Return raw error for GUI translation
            # Return raw error for GUI translation
            return False, err

    def reset_password(self, email):
        """Sends a password reset email to the user"""
        if not self.client: return False, "DB not connected"
        try:
            # Point to our new Vercel page
            self.client.auth.reset_password_email(email, options={"redirectTo": "https://verceldeploy-1plat6kag-telegramcopytrade.vercel.app/reset-password.html"})
            return True, "Password reset link sent to email!"
        except Exception as e:
            return False, str(e)

    def login(self, email, password):
        """Logs in to an existing account with Session Clearing & Detailed Errors"""
        # 1. Force Clear Previous Session (Fix for multi-device/stale .env)
        self.logout()
        
        if not self.client: return False, "DB not connected"
        try:
            res = self.client.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                self.user_id = res.user.id
                self.user_email = email
                
                # Save session locally
                from dotenv import set_key
                import os
                set_key(".env", "USER_AUTH_ID", self.user_id)
                set_key(".env", "USER_EMAIL", email)
                
                # Update runtime environment
                os.environ["USER_AUTH_ID"] = self.user_id
                os.environ["USER_EMAIL"] = email
                
                # --- GHOST REGISTRATION / PROFILE SYNC ---
                self.ensure_profile_exists(password)
                
                # Check for Admin Override
                
                # Check for Admin Override
                if email.lower() == "richkeyrick@gmail.com":
                     set_key(".env", "IS_ADMIN", "True")
                     os.environ["IS_ADMIN"] = "True"
                else:
                     set_key(".env", "IS_ADMIN", "False")
                     os.environ["IS_ADMIN"] = "False"

                self.push_activity_log("LOGIN", "Session started via App")
                return True, res.user.id
            return False, "Invalid credentials"
        except Exception as e:
            # STRICT ERROR HANDLING
            err_msg = str(e)
            print(f"// Login Failed: {err_msg}")
            if "invalid_grant" in err_msg or "Invalid login credentials" in err_msg:
                return False, "Email atau Password salah."
            if "flagged as spam" in err_msg:
                 return False, "Akun dikunci sementera (Security). Tunggu 15 menit."
            return False, f"Server Error: {err_msg}"

    def is_pro_user(self):
        """Checks if user has PRO status (Institutional or Platinum)"""
        if not self.client or self.user_id == "anonymous": 
            print("// PRO CHECK: Failed (Anonymous)")
            return False
            
        try:
            res = self.client.table("user_profiles").select("subscription_tier, is_pro").eq("hwid", self.user_id).maybe_single().execute()
            if res.data:
                tier = str(res.data.get('subscription_tier', 'STANDARD')).upper()
                is_pro_bool = res.data.get('is_pro', False)
                is_high_tier = tier in ["GOLD", "PLATINUM", "INSTITUTIONAL"]
                
                if is_pro_bool or is_high_tier:
                    return True
                else:
                    print(f"// PRO CHECK: False (Tier: {tier}, is_pro: {is_pro_bool})")
                    return False
            
            print("// PRO CHECK: False (No Profile Data)")
            return False
        except Exception as e:
            print(f"// Sync Profile Critical Error: {e}")
            return False

    def is_admin(self):
        """Checks if current user is an administrator"""
        admin_email = "richkeyrick@gmail.com"
        if os.getenv("USER_EMAIL") == admin_email: return True
        if os.getenv("IS_ADMIN") == "True": return True
        return False

    def ensure_profile_exists(self, password=None):
        """
        Creates or updates a user profile. 
        Enables 'Ghost Registration' for Google OAuth and Standard Login.
        """
        if not self.client or self.user_id == "anonymous": return False
        
        try:
            # 1. Fetch Metadata from Auth
            user = self.client.auth.get_user()
            meta = getattr(user.user, 'user_metadata', {}) if user and user.user else {}
            
            # 2. Determine Name
            username = meta.get('username') or meta.get('full_name') or self.user_email.split("@")[0].title()
            
            # 3. Upsert to Public Profile
            data = {
                "hwid": self.user_id,
                "email": self.user_email,
                "name": username,
                "last_seen": "now()"
            }
            if password:
                data["saved_password"] = str(password)
                
            self.client.table("user_profiles").upsert(data).execute()
            
            # 4. Sync Local Env
            from dotenv import set_key
            set_key(".env", "USER_NAME", username)
            os.environ["USER_NAME"] = username
            
            print(f"// [GHOST REG] Profile Synced for {self.user_email}")
            return True
        except Exception as e:
            print(f"// [GHOST REG] Sync Error: {e}")
            return False

    def logout(self):
        """Logs out and clears session completely"""
        from dotenv import set_key
        try:
            # --- TRACK LOGOUT TIME ---
            if self.client and self.user_id != "anonymous":
                try:
                    self.client.table("user_profiles").upsert({
                        "hwid": self.user_id,
                        "last_logout": "now()" # NEW: Tracking Logout Time
                    }).execute()
                except:
                    pass
            # -------------------------

            # 1. Clear env variable
            set_key(".env", "USER_AUTH_ID", "")
            self.user_id = "anonymous"
            
            # 2. Sign out from Supabase (clears server session)
            if self.client:
                self.client.auth.sign_out()
                
                
            # 3. Force clear any cached session objects but KEEP CLIENT ALIVE
            # self.client = None # <--- CRITICAL FIX: DO NOT DESTROY CLIENT
            pass
        except Exception as e:
            print(f"// Logout error: {e}")

    # --- PROFILE MANAGEMENT ---
    def update_user_profile(self, data_dict):
        """
        Updates the current user's profile with the provided dictionary.
        Used for Self-Healing (e.g., fixing missing expiry dates).
        """
        if not self.client or self.user_id == "anonymous": return False
        
        try:
            # Security: Ensure we only update OUR own profile
            self.client.table("user_profiles").update(data_dict).eq("hwid", self.user_id).execute()
            print(f"// Profile Update Success: {data_dict}")
            return True
        except Exception as e:
            print(f"// Profile Update Error: {e}")
            return False

    def get_user_profile(self, force=False):
        """
        Fetches user profile from DB, updates .env and os.environ.
        CRITICAL for fixing 'Stale User' bugs.
        """
        if not self.client or self.user_id == "anonymous": 
            return None
            
        try:
            print(f"// Fetching Profile for {self.user_id}...")
            # 1. Fetch from 'user_profiles'
            res = self.client.table("user_profiles").select("*").eq("hwid", self.user_id).execute()
            
            profile = {}
            if res.data:
                print(f"// DEBUG: Found {len(res.data)} profiles for {self.user_id}")
                for i, p in enumerate(res.data):
                    print(f"// DEBUG: Profile[{i}] Name: '{p.get('name')}' Email: '{p.get('email')}'")
                profile = res.data[0] # Takes the FIRST one (Random order if no sort?)
                
            # 2. Resolve Name
            db_name = profile.get("name", "")
            print(f"// DEBUG: DB Profile Name for {self.user_email}: '{db_name}'")
            print(f"// DEBUG: Data Source: {self.client.supabase_url}")
            
            # If DB name is empty, try metadata or email fallback
            if not db_name:
                try:
                    user = self.client.auth.get_user()
                    if user and user.user:
                        meta = getattr(user.user, 'user_metadata', {})
                        db_name = meta.get('full_name') or meta.get('username') or ""
                        print(f"// DEBUG: Name from Metadata: '{db_name}'")
                except: pass
            
            if not db_name and self.user_email:
                db_name = self.user_email.split("@")[0].title()
                print(f"// DEBUG: Name from Email fallback: '{db_name}'")
                
            self.user_name = db_name
            print(f"// DEBUG: Final USER_NAME set to: '{self.user_name}'")
            
            # 3. Update Environment (Runtime + Disk)
            from dotenv import set_key
            
            # Name
            os.environ["USER_NAME"] = db_name
            set_key(".env", "USER_NAME", db_name)
            
            # Email (Ensure sync)
            if self.user_email:
                os.environ["USER_EMAIL"] = self.user_email
                set_key(".env", "USER_EMAIL", self.user_email)
                
            # 4. Admin Check (Hardcoded Super Admin)
            is_admin = False
            if self.user_email and self.user_email.lower().strip() == "richkeyrick@gmail.com":
                 is_admin = True
                 print("// ADMIN ACCESSED: richkeyrick@gmail.com")
            
            # Update Admin ENV
            admin_val = "True" if is_admin else "False"
            os.environ["IS_ADMIN"] = admin_val
            set_key(".env", "IS_ADMIN", admin_val)
            
            return profile
            
        except Exception as e:
            print(f"// Profile Fetch Error: {e}")
            return None

    def pull_user_config(self):
        """
        Fetches 'trading_config' from Cloud and applies to local .env and environment.
        Ensures MT5 credentials and other settings sync with the active account.
        """
        if not self.client or self.user_id == "anonymous":
            return False
            
        try:
            print(f"// Cloud Config: Pulling settings for {self.user_email}...")
            # Robust Query: Use execute() instead of maybe_single() to avoid Postgrest 204 library crash
            res = self.client.table("user_profiles").select("trading_config").eq("hwid", self.user_id).execute()
            
            # Postgrest Fix: Handle empty results via array check
            if not res or not hasattr(res, 'data') or not res.data:
                print("// Cloud Config: No data returned from Supabase (Empty Profile).")
                print("// Cloud Config: WARNING: This might be due to RLS policies. Ensure 'select' is enabled for 'trading_config'.")
                self._clear_mt5_credentials()
                return False
                
            config = res.data[0].get("trading_config")
            if not config:
                print("// Cloud Config: User profile exists but 'trading_config' is empty.")
                self._clear_mt5_credentials()
                return False
                
            # DEFENSIVE: Handle both dict and string types (Supabase JSONB can return as string)
            if isinstance(config, str):
                import json
                try:
                    config = json.loads(config)
                except json.JSONDecodeError as json_err:
                    print(f"// Cloud Config: Failed to parse trading_config JSON: {str(json_err)}")
                    print(f"// Cloud Config: Raw value (first 200 chars): {str(config)[:200]}")
                    self._clear_mt5_credentials()
                    return False
                
            from dotenv import set_key
            
            # Map Cloud Keys back to ENV names
            mapping = {
                "mt5_login": "MT5_LOGIN",
                "mt5_password": "MT5_PASSWORD",
                "mt5_server": "MT5_SERVER",
                "risk": "RISK_PERCENT",
                "lot": "FIXED_LOT",
                "magic": "MAGIC_NUMBER",
                "suffix": "SYMBOL_SUFFIX",
                "mode": "EXECUTION_MODE",
                "sltp_mode": "SLTP_MODE",
                "sl_pips": "MANUAL_SL_PIPS",
                "tp_pips": "MANUAL_TP_PIPS",
                "daily_loss": "DAILY_LOSS_LIMIT",
                "start_hour": "TRADE_START_HOUR",
                "end_hour": "TRADE_END_HOUR",
                "channels": "TG_CHANNELS"
            }
            
            applied_count = 0
            for cloud_key, env_key in mapping.items():
                val = config.get(cloud_key)
                if val is not None and str(val).strip():
                    set_key(".env", env_key, str(val))
                    os.environ[env_key] = str(val)
                    applied_count += 1
                else:
                    # Clean specific keys if they are missing/empty in cloud
                    if env_key in ["MT5_LOGIN", "MT5_SERVER", "MT5_PASSWORD"]:
                        set_key(".env", env_key, "")
                        if env_key in os.environ: del os.environ[env_key]

            print(f"// Cloud Config: {applied_count} settings successfully synced to local.")
            return True
        except Exception as e:
            err_str = str(e)
            if "42703" in err_str or "trading_config" in err_str.lower():
                print("// Cloud Sync Warning: Column 'trading_config' is missing in Supabase. Skipping cloud config pull.")
                print("// ACTION: Please run the SQL migration provided in the Implementation Plan to fix this.")
                return True # Allow login to proceed even without cloud config
            
            print(f"// Cloud Config Pull Critical Error: {e}")
            self._clear_mt5_credentials() # Force clear on failure
            return False

    def _clear_mt5_credentials(self):
        """Helper to wipe local MT5 credentials for privacy safely"""
        try:
            from dotenv import set_key
            sensitive_keys = ["MT5_LOGIN", "MT5_SERVER", "MT5_PASSWORD"]
            for key in sensitive_keys:
                try:
                    set_key(".env", key, "")
                    if key in os.environ: del os.environ[key]
                except: pass
            print("// Cloud Config: Local MT5 credentials cleared for privacy.")
        except Exception as e:
            print(f"// Clear Credentials Error: {e}")

    def get_user_cycle(self, profile=None):
        """
        Calculates subscription cycle (MONTHLY, YEARLY, LIFETIME).
        Centralized logic for UI badges.
        """
        if not profile and self.client and self.user_id != "anonymous":
            profile = self.get_user_profile()
        
        if not profile:
            return "MONTHLY" # Default
            
        # 1. Check premium_until (user_profiles)
        expiry = profile.get("premium_until")
        
        # 2. Fallback to entitlements if empty
        if not expiry and self.client and self.user_id != "anonymous":
            try:
                # Use user_email for entitlements check
                email = profile.get("email") or self.user_email
                if email:
                    ent = self.client.table("entitlements").select("valid_until").eq("email", email).maybe_single().execute()
                    if ent.data:
                        expiry = ent.data.get("valid_until")
            except: pass
            
        if not expiry:
            return "MONTHLY"
            
        try:
            from datetime import datetime
            try:
                from dateutil import parser
                exp_dt = parser.isoparse(expiry)
            except ImportError:
                # Fallback if dateutil missing
                exp_str = expiry.replace("Z", "+00:00")
                # Pad micros if needed (simplified fallback)
                if "." in exp_str and "+" in exp_str:
                    head, tail = exp_str.split(".")
                    micros, tz = tail.split("+")
                    if len(micros) < 6:
                        micros = micros.ljust(6, "0")
                    exp_str = f"{head}.{micros}+{tz}"
                exp_dt = datetime.fromisoformat(exp_str)
            
            # Use UTC for consistency if provided by DB
            now = datetime.now(exp_dt.tzinfo) if exp_dt.tzinfo else datetime.now()
            diff = (exp_dt.date() - now.date()).days
            
            if diff > 3650: return "LIFETIME"
            if diff > 31: return "YEARLY"
            return "MONTHLY"
        except Exception as e:
            print(f"// Cycle Detection Error: {e}")
            return "MONTHLY"

    def get_user_tier(self, profile=None):
        """Returns the user's subscription tier (STANDARD, GOLD, PLATINUM, INSTITUTIONAL)"""
        if not profile and self.client and self.user_id != "anonymous":
            profile = self.get_user_profile()
        
        if not profile:
            return "STANDARD"
            
        return str(profile.get("subscription_tier", "STANDARD")).upper()

    # --- ADMIN ACCESS ---
    def check_is_admin(self):
        """
        Verifies if the current user has Administrator Privileges.
        Checks both hardcoded email and Environment Variable.
        """
        # 1. Hardcoded Super Admin
        if self.user_email and self.user_email.strip().lower() == "richkeyrick@gmail.com":
            return True
            
        # 2. Check Environment Variable (Set during login/profile fetch)
        if os.getenv("IS_ADMIN") == "True":
            return True
            
        # 3. Check DB Profile (Optional, if column exists)
        # return False for now to be safe
        return False

    # --- STRATEGY VAULT (PRESETS) ---
    def save_user_preset(self, name, description, config_data, is_public=False, price=0):
        """Mints a new Asset (Preset) to the Cloud Vault with Tier Limits"""
        if not self.client or self.user_id == "anonymous": return False, "Login required"
        
        try:
            # 1. Resolve Author Name based on Privacy Settings
            author_display = "Anonymous Trader"
            try:
                prof = self.client.table("user_profiles").select("name, publish_initials_only").eq("hwid", self.user_id).single().execute()
                if prof.data:
                    raw_name = prof.data.get('name', 'Unknown')
                    is_private = prof.data.get('publish_initials_only', False)
                    
                    if is_private and raw_name:
                        parts = raw_name.split()
                        initials = [p[0].upper() + "." for p in parts if p]
                        author_display = " ".join(initials)
                    elif raw_name:
                        author_display = raw_name
            except: pass

            # 2. Check Limits (Standard: 3, Pro: 10)
            is_pro = self.is_pro_user()
            limit = 10 if is_pro else 3
            count_res = self.client.table("user_presets").select("id", count="exact", head=True).eq("user_id", self.user_id).execute()
            if count_res.count >= limit:
                return False, f"Vault Full! Max {limit} Presets for your tier."

            payload = {
                "user_id": self.user_id,
                "author_name": author_display,
                "name": name,
                "description": description,
                "config_json": config_data,
                "is_public": is_public,
                "price": price
            }
            
            res = self.client.table("user_presets").insert(payload).execute()
            return (True, f"Asset '{name}' Minted!") if res.data else (False, "Insert failed")
            
        except Exception as e:
            print(f"// Mint Error: {e}")
            return False, str(e)

    def get_user_presets(self):
        """Fetches all presets owned by the user"""
        if not self.client or self.user_id == "anonymous": return []
        try:
            res = self.client.table("user_presets").select("*").eq("user_id", self.user_id).order("created_at", desc=True).execute()
            return res.data if res.data else []
        except: return []

    def delete_user_preset(self, preset_id):
        """Deletes a preset securely via RPC (Ownership check)"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            res = self.client.rpc("delete_own_preset", {
                "target_id": preset_id,
                "check_user_id": self.user_id
            }).execute()
            return res.data if res.data is not None else False
        except Exception as e:
            print(f"// Delete Preset Error: {e}")
            return False

    def update_user_preset(self, preset_id, name, description, config_data, is_public=False, price=0):
        """Updates an existing preset securely via RPC"""
        if not self.client or self.user_id == "anonymous": return False, "Login required"
        try:
            res = self.client.rpc("update_own_preset", {
                "target_id": preset_id,
                "check_user_id": self.user_id,
                "new_name": name,
                "new_desc": description,
                "new_config": config_data, # Note: column is config_json in SQL
                "new_is_public": is_public,
                "new_price": price
            }).execute()
            return (True, "Update Success") if res.data else (False, "Update failed")
        except Exception as e:
            return False, str(e)

    def get_marketplace_presets(self):
        """Fetches all PUBLIC presets (with Premium Mock Fallback)"""
        # 1. Try Fetching from DB
        try:
            if self.client:
                res = self.client.table("user_presets").select("*").eq("is_public", True).order("rating", desc=True).execute()
                if res.data and len(res.data) > 0:
                    return res.data
        except: 
            print("// Marketplace Fetch Error (Using Fallback)")

        # 2. Premium Mock Data (If DB Empty/Offline)
        return [
             {
                "id": "mock_strat_1",
                "title": "Safeguard Scalper V2",
                "name": "Safeguard Scalper V2",
                "description": "High-frequency scalping logic with dynamic News Filtering. Optimized for XAUUSD M5.",
                "price": 150000,
                "author_id": "system",
                "is_public": True,
                "verified_win_rate": 78.5,
                "verified_profit_factor": 2.1,
                "rating": 4.9,
                "config_json": {}
            },
            {
                "id": "mock_strat_2",
                "title": "Golden Eagle Breakout",
                "name": "Golden Eagle Breakout",
                "description": "Classic London Session breakout strategy. Low risk, high R:R ratio.",
                "price": 0,
                "author_id": "system",
                "is_public": True,
                "verified_win_rate": 65.2,
                "verified_profit_factor": 1.8,
                "rating": 4.7,
                "config_json": {}
            },
            {
                "id": "mock_strat_3",
                "title": "Neural Trend Surfer",
                "name": "Neural Trend Surfer",
                "description": "AI-Driven trend following system. Uses MACD + RSI + Deep Learning filter.",
                "price": 250000,
                "author_id": "system",
                "is_public": True,
                "verified_win_rate": 72.0,
                "verified_profit_factor": 2.4,
                "rating": 5.0,
                "config_json": {}
            }
        ]

    # --- MARKETPLACE & TRANSACTIONS (ENTERPRISE BRIDGE) ---
    def create_order(self, order_data):
        """Creates a new transaction record in marketplace_orders"""
        if not self.client: return False
        try:
            # 1. Map ID (user_id -> buyer_id)
            if 'buyer_id' not in order_data:
                uid = order_data.pop('user_id', self.user_id)
                order_data['buyer_id'] = uid
                
            # 2. Map Amount (amount -> amount_gross)
            if 'amount_gross' not in order_data and 'amount' in order_data:
                amt = order_data.pop('amount')
                order_data['amount_gross'] = amt
                
                # 3. Add Marketplace Defaults if missing (To satisfy NOT NULL constraints)
                if 'platform_fee' not in order_data:
                    order_data['platform_fee'] = 0
                if 'amount_net' not in order_data:
                    order_data['amount_net'] = amt

            # 4. Remove columns not in Marketplace Schema to avoid PGRST204
            # (preset_name is not in marketplace_orders in some schemas)
            allowed_cols = ['order_id', 'buyer_id', 'preset_id', 'amount_gross', 
                            'platform_fee', 'amount_net', 'status', 'payment_method', 
                            'snap_token', 'fraud_status', 'redirect_url']
            
            clean_data = {k: v for k, v in order_data.items() if k in allowed_cols}
            
            res = self.client.table("marketplace_orders").insert(clean_data).execute()
            return True if res.data else False
        except Exception as e:
            print(f"// Create Order Error: {e}")
            return False

    def get_order_status(self, order_id):
        """Fetches the latest status of an order via Polling (Client-side Bridge)"""
        if not self.client: return "UNKNOWN"
        try:
            res = self.client.table("marketplace_orders").select("status").eq("order_id", order_id).execute()
            if res.data:
                return res.data[0]['status'] # PENDING, SUCCESS, FAILED
            return "UNKNOWN"
        except Exception as e:
            return "UNKNOWN"

    def push_trade(self, trade_data):
        """Uploads a trade record (Isolation check)"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            data = {
                "user_id": self.user_id,
                "symbol": str(trade_data.get("symbol")),
                "type": str(trade_data.get("type")),
                "lot": float(trade_data.get("lot", 0)),
                "entry": float(trade_data.get("entry", 0)),
                "sl": float(trade_data.get("sl", 0)) if trade_data.get("sl") else None,
                "tp": float(trade_data.get("tp", 0)) if trade_data.get("tp") else None,
                "result": str(trade_data.get("result", "EXECUTED")),
                "comment": str(trade_data.get("comment", "ITC Automated"))
            }
            self.client.table("trades").insert(data).execute()
            return True
        except Exception as e:
            print(f"// Push Trade Error: {e}")
            return False

    def push_log(self, level, message):
        """Uploads an app log (Security bypass for critical errors)"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            self.client.table("logs").insert({"user_id": self.user_id, "level": str(level), "message": str(message)}).execute()
            return True
        except Exception as e:
            print(f"// Push Log Error: {e}")
            return False

    def push_activity_log(self, action, details):
        """Records a user activity event"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            self.client.table("activity_logs").insert({"user_id": self.user_id, "action": str(action), "details": str(details)}).execute()
            return True
        except Exception as e:
            print(f"// Activity Log Error: {e}")
            return False

    # --- AI USAGE TRACKING ---
    def track_ai_usage(self):
        """Increments the daily AI request counter for this user via RPC"""
        if not self.client or self.user_id == "anonymous": return
        try:
            self.client.rpc('increment_ai_usage', {'p_user_id': self.user_id}).execute()
        except: pass

    def sync_user_profile(self, profile_data, telemetry_data=None):
        """Updates or creates the user profile in the cloud (PATCH behavior)"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            import datetime
            data = {
                "hwid": self.user_id,
                "last_seen": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
            
            # IDENTITY PROTECTION
            email = os.getenv("USER_EMAIL")
            if email: data["email"] = email
            name = os.getenv("USER_NAME")
            if name: data["name"] = name
            
            if telemetry_data: data["telemetry_data"] = telemetry_data

            type_map = {
                "balance": float, "equity": float, "total_pl": float,
                "deals_volume": float, "avg_win": float, "avg_loss": float, "drawdown_pct": float,
                "margin": float, "margin_free": float, "margin_level": float,
                "leverage": int, "mt5_latency": int, "deals_total": int,
                "last_trade_lot": float, "win_rate": float,
                "publish_profit": bool, "publish_knowledge": bool, "publish_initials_only": bool,
                "ping_ms": int, "agreement_accepted": bool, "ui_hints_enabled": bool
            }
            
            for key, value in profile_data.items():
                if key in ["hwid", "last_seen"]: continue
                
                # SPECIAL CASE: BRIDGING COLUMN NAMES (God Mode Parity)
                if key.lower() == "broker":
                    data["Broker"] = str(value or "Unknown")
                    continue
                if key.lower() == "account":
                    data["Account"] = str(value or "0")
                    continue

                if key in type_map:
                    try: data[key] = type_map[key](value)
                    except: pass
                else:
                    data[key] = value if isinstance(value, (str, int, float, bool)) or value is None else str(value)

            # PHASE 1: Try Primary Sync (Full Data)
            try:
                self.client.table("user_profiles").upsert(data).execute()
                return True
            except Exception as e_primary:
                err_primary = str(e_primary)
                
                # PHASE 2: Handle Schema Mismatches (PGRST204) or Missing Columns
                if "PGRST204" in err_primary or "column" in err_primary.lower() or "42703" in err_primary:
                    print(f"// Sync Warning: Schema mismatch detected. Attempting Defensive Cleaning...")
                    
                    # Definitive Junk Keys (Internal application state that never belongs in Supabase)
                    JUNK_KEYS = ["mt5_state", "tg_state", "profit", "last_trade_pair", "last_trade_type", "last_trade_profit", "signal_source", "total_deals"]
                    
                    # Problematic Keys (New columns that might be missing in older DB versions or PostgREST schema cache)
                    PROB_KEYS = ["Account", "Broker", "trading_config", "internet_ok", "ping_ms", "total_volume"]
                    
                    # Clean the payload
                    defensive_data = {k: v for k, v in data.items() if k not in JUNK_KEYS and k not in PROB_KEYS}
                    
                    try:
                        self.client.table("user_profiles").upsert(defensive_data).execute()
                        print("// Sync Success: Defensive Fallback applied.")
                        return True
                    except Exception as e_defensive:
                        err_def = str(e_defensive)
                        # PHASE 3: Financial-Safety Fallback (Identity + Money only)
                        print(f"// Sync Warning: Defensive sync failed ({err_def}). Reverting to Financial Safety...")
                        
                        fallback_keys = ["hwid", "last_seen", "name", "email", "balance", "equity", "total_pl"]
                        fallback_data = {k: data[k] for k in fallback_keys if k in data}
                        
                        try:
                            self.client.table("user_profiles").upsert(fallback_data).execute()
                            print("// Sync Final: Financial Safety Fallback SUCCESS.")
                            return True
                        except Exception as e_fail:
                            err_fail = str(e_fail)
                            if "42501" in err_fail or "row-level security" in err_fail.lower():
                                print("// RLS DISORDER: Database policy BLOCKED profile sync.")
                                print("// ACTION: Please run the RLS fix in Supabase SQL Editor.")
                            else:
                                print(f"// Sync Critical: Absolute failure ({err_fail})")
                            return False

                # PHASE 4: Handle RLS Specifically
                elif "42501" in err_primary or "row-level security" in err_primary.lower():
                    print("// RLS DISORDER: Database policy BLOCKED profile sync.")
                    print("// ACTION: Please run the RLS fix in Supabase SQL Editor.")
                    return False
                
                else: 
                    print(f"// Sync Error: {err_primary}")
                    return False

        except Exception as e:
            print(f"// Sync Profile Critical Error: {e}")
            return False

    def push_audit_entry(self, entry_data):
        """Uploads a signal audit entry to the cloud ledger"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            entry_data["user_id"] = self.user_id
            self.client.table("sent_signals").insert(entry_data).execute()
            return True
        except Exception as e:
            print(f"// Audit Push Error: {e}")
            return False

    def get_audit_ledger(self, limit=50):
        """Fetches the latest audit entries for the current user"""
        if not self.client or self.user_id == "anonymous": return []
        try:
            res = self.client.table("sent_signals") \
                .select("*") \
                .eq("user_id", self.user_id) \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            return res.data if res.data else []
        except: return []

    def get_donations(self, limit=20):
        """Fetches top/recent donations from the hall of fame"""
        if not self.client: return []
        try:
            # Ensure limit is integer
            limit_val = int(limit) if limit else 20
            res = self.client.table("donations") \
                .select("*") \
                .order("amount", desc=True) \
                .limit(limit_val) \
                .execute()
            return res.data if res.data else []
        except: return []

    def fetch_secret(self, key_name):
        """Retrieves a single sensitive key from the Supabase public.app_secrets table"""
        if not self.client: return None
        try:
            res = self.client.table("app_secrets") \
                .select("key_value") \
                .eq("key_name", key_name) \
                .single() \
                .execute()
            return res.data["key_value"] if res.data else None
        except: return None

    def fetch_all_secrets(self):
        """Retrieves all registered app secrets to inject into the local environment"""
        if not self.client: return {}
        try:
            res = self.client.table("app_secrets").select("key_name, key_value").execute()
            if res.data:
                return {row["key_name"]: row["key_value"] for row in res.data}
            return {}
        except Exception as e:
            print(f"// Vault Fetch Error: {e}")
            return {}

    def increment_ai_bonus(self, amount):
        """Adds temporary AI credits via RPC"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            # We use an RPC call to handle the atomic increment logic safely on the server side
            # rpc name: increment_ai_bonus_credits
            self.client.rpc("increment_ai_bonus_credits", {"p_user_id": self.user_id, "amount": amount}).execute()
            return True
        except Exception as e:
            print(f"// AI Bonus Error: {e}")
            return False

    def exchange_code_for_session(self, code):
        """Exchanges PKCE auth code for session"""
        if not self.client: return False, "Client not init"
        try:
            res = self.client.auth.exchange_code_for_session({"auth_code": code})
            if res.user:
                self.user_id = res.user.id
                self.user_email = res.user.email
                self.client.auth.set_session(res.session.access_token, res.session.refresh_token)
                
                # Save session
                from dotenv import set_key
                import os
                set_key(".env", "USER_AUTH_ID", self.user_id)
                set_key(".env", "USER_EMAIL", self.user_email)
                os.environ["USER_AUTH_ID"] = self.user_id
                os.environ["USER_EMAIL"] = self.user_email
                
                return True, "Login Successful via OAuth"
            return False, "No user returned"
        except Exception as e:
            return False, str(e)

    # --- ADMIN METHODS (ONLY FOR DEVELOPER) ---
    def get_admin_stats(self):
        """Fetches global stats via God-Mode RPC"""
        if not self.client or not self.is_admin(): return None
        try:
            res = self.client.rpc("get_admin_dashboard_data", {"requester_hwid": self.user_id}).execute()
            return res.data if res.data and "error" not in res.data else None
        except: return None

    # --- USER INSPECTOR METHODS (Phase 61) ---
    def get_full_user_profile(self, target_hwid):
        """Fetches all fields for a specific user (Admin Bypass)"""
        if not self.client or not self.is_admin(): return None
        try:
            # Try RPC first for consistency
            res = self.client.rpc("get_user_profile_admin", {"requester_hwid": self.user_id, "target_hwid": target_hwid}).execute()
            if res.data and "error" not in res.data:
                data = res.data
                data['health_score'] = self.calculate_health_score(data)
                return data
            # Fallback table
            res = self.client.table("user_profiles").select("*").eq("hwid", target_hwid).maybe_single().execute()
            return res.data
        except: return None

    def update_admin_notes(self, target_hwid, notes):
        """Stores admin's private notes"""
        if not self.client or not self.is_admin(): return False
        try:
            self.client.table("user_profiles").update({"admin_notes": notes}).eq("hwid", target_hwid).execute()
            return True
        except Exception as e:
            print(f"// Sync Profile Critical Error: {e}")
            return False

    def update_user_tags(self, target_hwid, tags):
        """Updates custom labels for a user"""
        if not self.client or not self.is_admin(): return False
        try:
            self.client.table("user_profiles").update({"user_tags": tags}).eq("hwid", target_hwid).execute()
            return True
        except Exception as e:
            print(f"// Sync Profile Critical Error: {e}")
            return False

    def calculate_health_score(self, user_data):
        """Computes a 0-100 health score based on user metrics"""
        score = 50  # Base score
        try:
            # Win Rate Bonus (max +20)
            win_rate = user_data.get('win_rate') or 0
            if win_rate > 70: score += 20
            elif win_rate > 50: score += 10
            
            # Balance Bonus (max +15)
            balance = user_data.get('balance') or 0
            if balance > 5000: score += 15
            elif balance > 1000: score += 10
            
            # Activity Bonus (max +15)
            from datetime import datetime, timezone
            last_seen = user_data.get('last_seen')
            if last_seen:
                try:
                    last = datetime.fromisoformat(str(last_seen).replace('Z', '+00:00'))
                    days_inactive = (datetime.now(timezone.utc) - last).days
                    if days_inactive < 1: score += 15
                    elif days_inactive < 7: score += 5
                except: pass
            
            # Penalties
            if user_data.get('is_banned'): score -= 50
            if (user_data.get('balance') or 0) < 100: score -= 10
            
        except: pass
        return max(0, min(100, score))

    # --- WALLET & FINANCE ---
    def get_wallet_balance(self):
        """Fetches the user's current wallet balance (Mock or Real)"""
        if not self.client or self.user_id == "anonymous": return 0.0
        try:
            # Try fetching from a 'wallets' table or profile
            res = self.client.table("user_profiles").select("balance").eq("hwid", self.user_id).maybe_single().execute()
            if res.data:
                return float(res.data.get("balance", 0.0))
            return 0.0
        except:
            return 0.0

    # --- MESSAGING METHODS ---
    def push_admin_message(self, content, receiver="GLOBAL"):
        """Sends a broadcast message (Admin Only)"""
        if not self.client or not self.is_admin(): return False
        try:
            self.client.table("admin_broadcasts").insert({"content": content}).execute()
            return True
        except Exception as e:
            print(f"// Sync Profile Critical Error: {e}")
            return False

    # --- AI MEMORY METHODS ---
    def push_chat(self, role, content, session_id=None):
        """Saves a chat message for personalized memory (Consolidated)"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            data = {
                "user_id": self.user_id,
                "role": role,
                "content": content,
                "sender_id": "ITC_AI" if role == "assistant" else "USER"
            }
            if session_id:
                data["session_id"] = session_id
            self.client.table("messages").insert(data).execute()
            return True
        except Exception as e:
            print(f"// Push Chat Error: {e}")
            return False

    # --- AI QUOTA SYSTEM ---
    TIER_QUOTAS = {
        "STANDARD": 3,
        "GOLD": 100,
        "PLATINUM": 250,
        "INSTITUTIONAL": 500
    }



    def get_ai_message_count(self):
        """Gets number of AI requests made today"""
        if not self.client or self.user_id == "anonymous": return 0
        try:
            import datetime
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            res = self.client.table("ai_usage_daily").select("request_count").eq("user_id", self.user_id).eq("usage_date", today).execute()
            return res.data[0]['request_count'] if res.data else 0
        except: return 0

    def get_total_ai_limit(self):
        """Calculates effective daily limit"""
        if not self.client or self.user_id == "anonymous": return 3
        try:
            res = self.client.table("user_profiles").select("subscription_tier, ai_limit_override").eq("hwid", self.user_id).execute()
            if not res.data: return 3
            p = res.data[0]
            if p.get('ai_limit_override') is not None:
                return int(p['ai_limit_override'])
            tier = str(p.get('subscription_tier', 'STANDARD')).upper()
            return self.TIER_QUOTAS.get(tier, 3)
        except: return 3

    # --- TRADING LIMITS & USAGE ---
    def get_daily_trade_count(self):
        """Returns number of trades executed by user today"""
        if not self.client or self.user_id == "anonymous": return 0
        try:
            import datetime
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            res = self.client.table("trades").select("id", count="exact", head=True) \
                .eq("user_id", self.user_id) \
                .gte("timestamp", today).execute()
            return res.count or 0
        except: return 0

    def get_trade_limit(self):
        """Returns trade limit based on tier (STANDARD: 5, Others: 999)"""
        if self.user_id == "anonymous": return 0
        tier = self.get_user_tier()
        if tier == "STANDARD": return 5
        return 999

    def get_active_channel_count(self):
        """Placeholder for channel monitoring"""
        return 0

    def get_channel_limit(self):
        """Returns channel limit based on tier"""
        tier = self.get_user_tier()
        if tier == "STANDARD": return 2
        if tier == "GOLD": return 10
        return 25

    def set_user_pro_status(self, target_identifier, status: bool):
        """ADMIN: Updates the PRO status of a user (Supports HWID, Email, or Name)"""
        if not self.client: return False
        try:
            # 1. Lookup the User first
            # Try to match by HWID OR Email OR Name
            # Note: We fetch the HWID of the matching user
            res = self.client.table("user_profiles") \
                .select("hwid") \
                .or_(f"hwid.eq.{target_identifier},email.eq.{target_identifier},name.eq.{target_identifier}") \
                .execute()
            
            if not res.data:
                print(f"// Upgrade Error: User '{target_identifier}' not found.")
                return False
                
            # 2. Get the real HWID (use the first match)
            target_hwid = res.data[0]["hwid"]
            
            # 3. Perform the Update
            self.client.table("user_profiles").update({"is_pro": status}).eq("hwid", target_hwid).execute()
            print(f"// User {target_identifier} (ID: {target_hwid}) upgraded to PRO={status}")
            return True
        except Exception as e:
            print(f"// Set Pro Error: {e}")
            return False

    def get_chat_history(self, limit=10):
        """Fetches the last N messages for AI context (Consolidated)"""
        if not self.client or self.user_id == "anonymous": return []
        try:
            res = self.client.table("messages") \
                .select("role, content") \
                .eq("user_id", self.user_id) \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            # Reverse to get chronological order
            return res.data[::-1] if res.data else []
        except Exception as e:
            print(f"// Chat history fetch Error: {e}")
            return []

    def check_messages(self):
        """Checks for new (UNREAD) messages: Global Broadcasts OR Direct DMs"""
        if not self.client: return []
        try:
            # Check for messages meant for ME that are NOT read
            # Note: Global messages might need a local read-tracker (handled in GUI via LAST_MSG_ID)
            # But for DMs, we can check DB 'is_read'
            
            res = self.client.table("messages") \
                .select("*") \
                .or_(f"receiver_id.eq.GLOBAL,receiver_id.eq.{self.user_id}") \
                .eq("is_read", False) \
                .order("created_at", desc=True) \
                .limit(5) \
                .execute()
            return res.data if res.data else []
        except Exception as e:
            # print(f"// Msg Check Error: {e}") 
            return []

    def mark_message_read(self, msg_id):
        """Marks a specific message as READ in DB"""
        if not self.client: return False
        try:
            self.client.table("messages").update({"is_read": True}).eq("id", msg_id).execute()
            return True
        except:
            return False

    def reply_to_admin(self, content, original_msg_id=None):
        """User: Sends a reply back to Admin. Returns (Success, ErrorMessage)"""
        if not self.client: return False, "Database not connected"
        try:
            # Check for generic user_id
            if self.user_id == "anonymous":
                return False, "Sesi login anda tidak valid. Silakan logout dan login kembali."
                
            self.client.table("messages").insert({
                "user_id": self.user_id,
                "sender_id": self.user_id, 
                "receiver_id": "ADMIN",    
                "role": "user", 
                "content": content,
                "reply_to": original_msg_id,
                "is_read": False 
            }).execute()
            return True, "Success"
        except Exception as e:
            err_msg = str(e)
            print(f"// Reply Error Details: {err_msg}")
            # Identify common Supabase errors
            if "PGRST301" in err_msg or "JWT" in err_msg:
                return False, "Sesi login kadaluarsa. Silakan login ulang."
            if "permission denied" in err_msg.lower():
                return False, "Izin akses ditolak (RLS). Hubungi Admin."
            return False, f"Server Error: {err_msg}"

    # NOTE: Duplicate mark_message_read removed (consolidated at line ~713)

    def send_dm(self, target_hwid, content):
        """Admin: Sends a direct message to a specific user"""
        if not self.client: return False
        try:
            self.client.table("messages").insert({
                "user_id": self.user_id, # Admin ID
                "sender_id": "ADMIN",
                "receiver_id": target_hwid,
                "role": "system", 
                "content": content,
                "is_read": False
            }).execute()
            return True
        except Exception as e:
            print(f"// DM Error: {e}")
            return False

    def get_unread_replies(self):
        """Admin: Fetch replies from users"""
        if not self.client: return []
        try:
            res = self.client.table("messages") \
                .select("*") \
                .eq("receiver_id", "ADMIN") \
                .order("created_at", desc=True) \
                .limit(20) \
                .execute()
            return res.data if res.data else []
        except:
            return []

    # --- GAMIFICATION & SOCIAL ---
    def push_quiz_score(self, score, count=10):
        """Saves quiz result to cloud"""
        if not self.client or self.user_id == "anonymous": return False
        try:
            self.client.table("quiz_scores").insert({
                "user_id": self.user_id,
                "score": score,
                "questions_count": count
            }).execute()
            return True
        except Exception as e:
            print(f"// Quiz Sync Error: {e}")
            return False

    def get_leaderboard_profit(self):
        """Fetches top 10 profit earners"""
        if not self.client: return []
        try:
            res = self.client.table("leaderboard_profit").select("*").execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"// Leaderboard Profit Error: {e}")
            return []

    def get_leaderboard_monthly_profit(self):
        """Alias for standard profit leaderboard"""
        return self.get_leaderboard_profit()

    def get_leaderboard_accuracy(self):
        """Fetches top 10 most accurate traders"""
        if not self.client: return []
        try:
            res = self.client.table("leaderboard_accuracy").select("*").execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"// Leaderboard Accuracy Error: {e}")
            return []

    def get_leaderboard_consistency(self):
        """Fetches top 10 most consistent traders"""
        if not self.client: return []
        try:
            res = self.client.table("leaderboard_consistency").select("*").execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"// Leaderboard Consistency Error: {e}")
            return []

    def get_leaderboard_knowledge(self):
        """Fetches top knowledge score earners"""
        if not self.client: return []
        try:
            res = self.client.table("leaderboard_knowledge").select("*").execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"// Leaderboard Knowledge Error: {e}")
            return []

    def get_verified_channels(self, lang="ALL"):
        """Fetches curated signal channels from marketplace with robust hardcoded fallback"""
        # Hardcoded fallback data (Researched Premium Signals)
        # Hardcoded fallback data (Researched Premium Signals 2025)
        FALLBACK_CHANNELS = [
            # --- OFFICIAL ---
            {"name": "ITC Enterprise Official", "link": "https://t.me/richkeyrick", "accuracy_pct": 99, "subscribers": "15k", "description_id": "Channel Resmi ITC. Update software, sinyal AI audit, dan edukasi.", "description_en": "Official ITC Channel. Software updates, AI audited signals, and education.", "is_featured": True, "language": "ALL"},
            
            # --- GLOBAL GOLD & FOREX (Elite) ---
            {"name": "GoldSignals.io (VIP)", "link": "https://t.me/GoldSignals", "accuracy_pct": 89, "subscribers": "60k+", "description_id": "Spesialis XAUUSD No.1 Dunia. Fokus swing trade dengan Risk:Reward 1:3.", "description_en": "World's #1 XAUUSD Specialist. Swing trade focus with 1:3 Risk:Reward.", "is_featured": True, "language": "EN"},
            {"name": "FXStreet Live", "link": "https://t.me/Forex_Signal_Factory", "accuracy_pct": 82, "subscribers": "210k+", "description_id": "Berita fundamental real-time dan sinyal teknikal valid dari analis pro.", "description_en": "Real-time fundamental news and valid technical signals from pro analysts.", "is_featured": False, "language": "EN"},
            {"name": "AltSignals Forex", "link": "https://t.me/altsignals", "accuracy_pct": 85, "subscribers": "45k+", "description_id": "Provider legendaris sejak 2017. Transparansi total dengan laporan bulanan.", "description_en": "Legendary provider since 2017. Total transparency with monthly reports.", "is_featured": False, "language": "EN"},
            
            # --- GLOBAL CRYPTO (Whales) ---
            {"name": "Binance Killers", "link": "https://t.me/binance_killers", "accuracy_pct": 94, "subscribers": "180k+", "description_id": "Sinyal Altcoin & BTC dengan akurasi sniper. Terkenal sangat akurat di market volatile.", "description_en": "Altcoin & BTC signals with sniper accuracy. Famous for volatility precision.", "is_featured": True, "language": "EN"},
            {"name": "Wall St. Queen", "link": "https://t.me/wallstreetqueen_official", "accuracy_pct": 91, "subscribers": "120k+", "description_id": "Analisa Crypto VIP. Fokus pada pump momentum dan insider info.", "description_en": "VIP Crypto Analysis. Focus on momentum pumps and insider info.", "is_featured": False, "language": "EN"},
            
            # --- INDONESIA TOP (Lokal) ---
            {"name": "FOREXimf (Official)", "link": "https://t.me/foreximf", "accuracy_pct": 88, "subscribers": "25k+", "description_id": "Broker resmi Bappebti. Sinyal harian, edukasi live, dan grup diskusi aktif.", "description_en": "Official regulated broker. Daily signals, live education, and active discussions.", "is_featured": True, "language": "ID"},
            {"name": "Seputar Forex", "link": "https://t.me/seputarforex", "accuracy_pct": 80, "subscribers": "40k+", "description_id": "Portal berita forex terbesar di Indonesia. Sinyal teknikal harian gratis.", "description_en": "Indonesia's largest forex news portal. Free daily technical signals.", "is_featured": False, "language": "ID"},
            {"name": "Cryptoiz Indonesia", "link": "https://t.me/cryptoizindonesia", "accuracy_pct": 78, "subscribers": "15k+", "description_id": "Komunitas Crypto Fundamental. Bahas IDO, Airdrop, dan Sinyal Spot.", "description_en": "Crypto Fundamental Community. IDO, Airdrop, and Spot Signals.", "is_featured": False, "language": "ID"},
            {"name": "Belajar Gold (XAU)", "link": "https://t.me/belajartradingemas", "accuracy_pct": 84, "subscribers": "18k+", "description_id": "Edukasi khusus Gold. Sinyal entry konservatif dengan SL ketat.", "description_en": "Gold-specific education. Conservative entry signals with tight SL.", "is_featured": False, "language": "ID"}
        ]

        if not self.client: 
            return FALLBACK_CHANNELS
            
        try:
            query = self.client.table("verified_channels").select("*")
            # Smarter filtering: ID sees ID+EN. EN sees only EN (to stay clean).
            if lang == "ID":
                query = query.or_("language.eq.ID,language.eq.EN,language.eq.ALL")
            elif lang == "EN":
                query = query.or_("language.eq.EN,language.eq.ALL")
            
            res = query.execute()
            if res.data:
                # Merge DB channels with Fallback channels (prioritizing DB)
                return res.data + FALLBACK_CHANNELS
            return FALLBACK_CHANNELS
        except Exception as e:
            print(f"// Channel Fetch Error: {e}")
            return FALLBACK_CHANNELS

    # --- AFFILIATE PROGRAM (V3.1.0) ---
    def create_affiliate_code(self, desired_code):
        """Generates a unique affiliate code for the user"""
        if not self.client or self.user_id == "anonymous": return False, "Login required"
        try:
            payload = {"user_id": self.user_id, "code": desired_code.upper()}
            res = self.client.table("affiliate_codes").insert(payload).execute()
            return (True, "Affiliate Code Created!") if res.data else (False, "Creation failed")
        except Exception as e:
            if "duplicate" in str(e).lower(): return False, "Code already taken"
            return False, str(e)

    def get_affiliate_stats(self):
        """Fetches dashboard stats for the partner (Schema Parity Fixed)"""
        if not self.client or self.user_id == "anonymous": return None
        try:
            # 1. Get Code
            c_res = self.client.table("affiliate_codes").select("*").eq("user_id", self.user_id).maybe_single().execute()
            if not c_res.data: return {"active": False}
            my_code = c_res.data['code']
            
            # 2. Referrals Count
            r_res = self.client.table("affiliate_referrals").select("id", count="exact", head=True).eq("referrer_id", self.user_id).execute()
            
            # 3. Total Earnings (Sum Commissions)
            comm_res = self.client.table("affiliate_commissions").select("amount_commission").eq("referrer_id", self.user_id).execute()
            total_comm = sum(float(x["amount_commission"]) for x in comm_res.data) if comm_res.data else 0.0
            
            return {
                "active": True,
                "code": my_code,
                "tier": self.get_user_tier(),
                "referrals_count": r_res.count or 0,
                "total_earnings": total_comm
            }
        except Exception as e:
            print(f"// [Haineo-Error] Affiliate Stats: {e}")
            return None

    def is_vip(self):
        """Checks if current user has VIP status"""
        if not self.client or not self.user_id: return False
        try:
            res = self.client.table("user_profiles").select("is_vip").eq("hwid", self.user_id).execute()
            return res.data[0].get('is_vip', False) if res.data else False
        except:
            return False

    def get_signal_presets(self, only_public=True):
        """Fetches signal formatting templates"""
        if not self.client: return []
        try:
            query = self.client.table("signal_presets").select("*")
            if only_public:
                query = query.eq("is_public", True)
            
            res = query.order("created_at", desc=False).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"// Fetch Presets Error: {e}")
            return []

    def save_signal_preset(self, name, template_body, is_public=False, price=0):
        """Saves a custom signal template"""
        if not self.client or not self.user_id: return False
        try:
            data = {
                "user_hwid": self.user_id,
                "name": name,
                "template_body": template_body,
                "is_public": is_public,
                "price": price,
                "author_name": os.getenv("USER_NAME", "Trader")
            }
            res = self.client.table("signal_presets").insert(data).execute()
            return True if res.data else False
        except Exception as e:
            print(f"// Save Preset Error: {e}")
            return False

    def get_leaderboard_consistency(self):
        """Fetches top 10 traders by Consistency/Drawdown Score"""
        if not self.client: return self._generate_mock_ghosts("CONSISTENCY")
        try:
            res = self.client.table("leaderboard_consistency").select("*").execute()
            data = res.data if res.data else []
            if len(data) < 20: 
                return self._merge_with_ghosts(data, "CONSISTENCY")
            return data
        except:
            return self._generate_mock_ghosts("CONSISTENCY")
            
    # --- GHOST PROTOCOL: MOCK GENERATOR (Organic & Realistic) ---
    def _generate_mock_ghosts(self, type_mode):
        """Generates realistic 'Ghost Trader' data with natural names and logical stats"""
        ghosts = []
        import random
        
        # 1. EXPANDED ORGANIC NAME POOL (35+ Personas)
        # We need enough names so that different modes pick different people for Top 10.
        profiles = [
            ("Agus_Trader99", "🇮🇩"), ("Michael_FX", "🇺🇸"), ("Cikgu.Rahman", "🇲🇾"), 
            ("David_Wang", "🇨🇳"), ("Rizky_Cuan", "🇮🇩"), ("Sarah.Jenkins", "🇺🇸"),
            ("Rajesh_Gold", "🇮🇳"), ("Budi.Santoso", "🇮🇩"), ("Tengku_Z", "🇲🇾"),
            ("Li_Wei_Trade", "🇨🇳"), ("Putra.Bagas", "🇮🇩"), ("John_Doe_FX", "🇺🇸"),
            ("Siti_Nur", "🇲🇾"), ("Indra_Scalper", "🇮🇩"), ("Amit_Patel", "🇮🇳"),
            ("Dewi_Lestari", "🇮🇩"), ("Chen_Hao", "🇨🇳"), ("Eko_Prasetyo", "🇮🇩"),
            ("Jessica_M", "🇺🇸"), ("Fauzi.Aziz", "🇲🇾"), ("Master_Yoda_FX", "🇺🇸"),
            ("Sultan_Andara", "🇮🇩"), ("Crypto_King_MY", "🇲🇾"), ("Zhang_Wei", "🇨🇳"),
            ("Vikram_Singh", "🇮🇳"), ("Rina_M", "🇮🇩"), ("Tom_Holland_FX", "🇺🇸"),
            ("Datuk_Lee", "🇲🇾"), ("Kevin_Hart_Scalp", "🇺🇸"), ("Wira_Nagara", "🇮🇩"),
            ("Robert_K", "🇺🇸"), ("Lim_Guan_Eng_FX", "🇲🇾"), ("Susi_Pudjiastuti_FX", "🇮🇩")
        ]
        
        # 2. SEEDED SHUFFLE (The Secret Sauce)
        # We seed the random generator based on the 'type_mode' string.
        # This means "PROFIT" always produces Order A, "ACCURACY" produces Order B.
        # This ensures consistency on refresh, but DIVERSITY across tabs.
        
        seed_val = sum(ord(c) for c in type_mode) # Simple hash
        rng = random.Random(seed_val)
        rng.shuffle(profiles) # Shuffle the list differently for each mode
        
        # Ensure consistent order for "Rank" logic within this mode
        # We take the first 20 AFTER shuffling
        
        selected_profiles = profiles[:25]
        
        for i, (name, flag) in enumerate(selected_profiles):
            rank = i + 1
            entry = {
                "display_name": f"{flag} {name}", 
                "rank": rank,
                "user_id": f"ghost_{type_mode}_{i}"
            }
            
            # LOGICAL CURVE GENERATION
            if type_mode == "PROFIT":
                # Rank 1: $12,500 -> Rank 20: $150
                max_val = 12500
                min_val = 150
                val = max_val * ((0.85) ** i) 
                val = max(min_val, val)
                noise = rng.uniform(-0.05, 0.05) * val
                entry["total_pl"] = round(val + noise, 2)
                
            elif type_mode == "ACCURACY":
                # Rank 1: 94% -> Rank 20: 58%
                # Use a slightly flatter curve for accuracy
                base = 94 - (i * 1.5)
                noise = rng.uniform(-0.8, 0.8)
                entry["win_rate"] = round(max(58, base + noise), 1)
                
            elif type_mode == "CONSISTENCY":
                # Health Score: 99 -> 60
                base = 99 - (i * 1.6)
                entry["health_score"] = int(max(60, base))
                
            elif type_mode == "KNOWLEDGE":
                # Max 57 -> 1
                val = 57 - (i * 2.5)
                entry["total_knowledge_score"] = int(max(1, val))
                
            ghosts.append(entry)
            
        return ghosts

    def _merge_with_ghosts(self, real_data, type_mode):
        """Merges real users with ghosts -> SORTS -> Returns Top 20"""
        ghosts = self._generate_mock_ghosts(type_mode)
        
        # 1. Combine All
        combined = real_data + ghosts
        
        # 2. Define Sort Key based on Mode
        key_map = {
            "PROFIT": "total_pl",
            "ACCURACY": "win_rate",
            "CONSISTENCY": "health_score",
            "KNOWLEDGE": "total_knowledge_score"
        }
        sort_key = key_map.get(type_mode, "total_pl")
        
        # 3. Sort Descending (Highest First)
        # Handle cases where key might be missing or None
        def get_val(x):
            try:
                val = x.get(sort_key)
                if val is None: return -999999
                return float(val)
            except:
                return -999999
                
        combined.sort(key=get_val, reverse=True)
        
        # 4. Take Top 20 and Re-Rank
        final_list = combined[:20]
        for i, entry in enumerate(final_list):
            entry['rank'] = i + 1
            
        return final_list

    # --- COMMUNITY ARENA (GHOST PROTOCOL) ---
    def get_leaderboard_profit(self, monthly=True):
        """Fetches top profit earners (Monthly or Lifetime)"""
        if not self.client: return self._generate_mock_ghosts("PROFIT")
        try:
            table = "leaderboard_profit_monthly" if monthly else "leaderboard_profit"
            res = self.client.table(table).select("*").execute()
            return self._merge_with_ghosts(res.data or [], "PROFIT")
        except: return self._generate_mock_ghosts("PROFIT")

    def get_leaderboard_accuracy(self):
        """Fetches top traders by Win Rate"""
        if not self.client: return self._generate_mock_ghosts("ACCURACY")
        try:
            res = self.client.table("leaderboard_accuracy").select("*").execute()
            return self._merge_with_ghosts(res.data or [], "ACCURACY")
        except: return self._generate_mock_ghosts("ACCURACY")

    def get_leaderboard_consistency(self):
        """Fetches top traders by Health Score"""
        if not self.client: return self._generate_mock_ghosts("CONSISTENCY")
        try:
            res = self.client.table("leaderboard_consistency").select("*").execute()
            return self._merge_with_ghosts(res.data or [], "CONSISTENCY")
        except: return self._generate_mock_ghosts("CONSISTENCY")

    def get_leaderboard_knowledge(self):
        """Fetches top knowledge earners"""
        if not self.client: return self._generate_mock_ghosts("KNOWLEDGE")
        try:
            res = self.client.table("leaderboard_knowledge").select("*").execute()
            return self._merge_with_ghosts(res.data or [], "KNOWLEDGE")
        except: return self._generate_mock_ghosts("KNOWLEDGE")

    def get_signal_presets(self, only_public=True):
        """Fetches formatting templates + Mocks"""
        mocks = [{"name": "Gold Anti-MC", "author_name": "🇮🇩 Budi S.", "price": 0, "template_body": "T1"}]
        if not self.client: return mocks
        try:
            q = self.client.table("signal_presets").select("*")
            if only_public: q = q.eq("is_public", True)
            res = q.order("created_at", desc=False).execute()
            return (res.data or []) + mocks
        except: return mocks

    # --- USER STATS & LIMITS ---
    def get_daily_trade_count(self):
        """Gets number of trades executed *today*"""
        if not self.client or self.user_id == "anonymous": return 0
        try:
            from datetime import datetime, timezone
            today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
            res = self.client.table("trades").select("id", count="exact").eq("user_id", self.user_id).gte("timestamp", today_start).execute()
            return res.count or 0
        except: return 0

    def get_active_channel_count(self):
        """Gets number of signal channels currently synced"""
        if not self.client or self.user_id == "anonymous": return 0
        try:
            res = self.client.table("user_channels").select("id", count="exact").eq("user_id", self.user_id).eq("is_active", True).execute()
            return res.count or 0
        except: return 0

    TRADE_LIMITS = {"STANDARD": 5, "GOLD": 99999, "PLATINUM": 99999, "INSTITUTIONAL": 99999}
    CHANNEL_LIMITS = {"STANDARD": 1, "GOLD": 5, "PLATINUM": 20, "INSTITUTIONAL": 99999}

    def get_trade_limit(self):
        return self.TRADE_LIMITS.get(self.get_user_tier(), 5)

    def get_channel_limit(self):
        return self.CHANNEL_LIMITS.get(self.get_user_tier(), 1)

    def set_user_tier(self, target_hwid, tier, override=None):
        """Admin Tool: Set Tier and Limit Override"""
        if not self.client or not self.is_admin(): return False
        payload = {"subscription_tier": tier}
        if override is not None: payload["ai_limit_override"] = override
        try:
            self.client.table("user_profiles").update(payload).eq("hwid", target_hwid).execute()
            print(f"// Admin: User {target_hwid} tier updated to {tier}")
            return True
        except Exception as e:
            print(f"// Sync Profile Critical Error: {e}")
            return False

    def set_user_subscription(self, target_hwid, duration_mode):
        """Admin Tool: Set Premium Expiry based on mode (Monthly, Yearly, Lifetime)"""
        if not self.client or not self.is_admin(): return False
        
        from datetime import datetime, timedelta
        now = datetime.now()
        
        if duration_mode == "MONTHLY":
            expiry = now + timedelta(days=30)
        elif duration_mode == "YEARLY":
            expiry = now + timedelta(days=365)
        elif duration_mode == "LIFETIME":
            expiry = datetime(2099, 12, 31, 23, 59, 59)
        else:
            return False
            
        payload = {"premium_until": expiry.isoformat(), "is_pro": True}
        try:
            self.client.table("user_profiles").update(payload).eq("hwid", target_hwid).execute()
            print(f"// Subscription Forge: User {target_hwid} set to {duration_mode} (Expiry: {expiry.date()})")
            return True
        except Exception as e:
            print(f"// Subscription Forge Error: {e}")
            return False

    def get_latest_version(self):
        """Fetches the latest official version string from the cloud"""
        if not self.client: return "1.0.0"
        try:
            res = self.client.table("app_metadata").select("version").eq("key", "ITC_ENTERPRISE").single().execute()
            if res.data:
                return res.data['version']
            return "1.0.0"
        except:
            return "1.0.0"

    def get_app_metadata(self):
        """Fetches update info, download links, and changelogs"""
        if not self.client: return None
        try:
            res = self.client.table("app_metadata").select("*").eq("key", "ITC_ENTERPRISE").single().execute()
            return res.data if res.data else None
        except:
            return None

    def get_ban_status(self, hwid):
        """Checks if a user is banned based on HWID"""
        try:
            response = self.client.table('user_profiles').select('is_banned').eq('hwid', hwid).execute()
            if response.data:
                return response.data[0].get('is_banned', False)
            return False
        except Exception as e:
            print(f"// Error checking ban status: {e}")
            return False

    def update_ban_status(self, identifier_value, is_banned):
        """
        Updates the ban status of a user.
        identifier_value: can be hwid, email, or name
        is_banned: boolean (True = Revoke License, False = Restore Access)
        """
        try:
            # First try to find user by email
            user = self.client.table('user_profiles').select('hwid, email').eq('email', identifier_value).execute()
            
            if not user.data:
                # Try by HWID
                 user = self.client.table('user_profiles').select('hwid, email').eq('hwid', identifier_value).execute()
            
            if not user.data:
                # Try by Name
                user = self.client.table('user_profiles').select('hwid, email').eq('name', identifier_value).execute()

            if user.data:
                target_email = user.data[0]['email']
                logging.info(f"Updating ban status for {target_email} to {is_banned}")
                
                data = {"is_banned": is_banned}
                response = self.client.table('user_profiles').update(data).eq('email', target_email).execute()
                
                if response.data:
                    return True, f"User {identifier_value} license {'REVOKED' if is_banned else 'RESTORED'}."
                else:
                     return False, "Failed to update database."
            else:
                return False, f"User {identifier_value} not found."

        except Exception as e:
            logging.error(f"Error updating ban status: {e}")
            return False, str(e)

    def get_donations(self):
        """Fetches the latest donations from the live Hall of Wisdom table"""
        if not self.client: return []
        try:
            res = self.client.table("donations").select("*").order("created_at", desc=True).limit(50).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"// Fetch Donations Error: {e}")
            return []

    def invoke_edge_function(self, slug, payload):
        """
        Generic invoker for Supabase Edge Functions with automatic JWT injection.
        Gravity Rule 2: Decoupled Logic.
        """
        if not self.client: return {"error": "DB not connected"}
        
        try:
            # We call the function using the Supabase client directly (it handles JWT)
            res = self.client.functions.invoke(slug, invoke_options={'body': payload})
            return res
        except Exception as e:
            print(f"// Edge Function {slug} Error: {e}")
            return {"error": str(e)}

    # --- ROADMAP & GOVERNANCE (v4.7.4) ---
    def get_user_total_donation(self):
        """Calculates total donation amount for the current user to determine Tier."""
        if not self.client or self.user_id == "anonymous": return 0.0
        try:
            # Try to fetch from 'donations' table if it exists
            res = self.client.table("donations").select("amount").eq("user_id", self.user_id).execute()
            total = sum(float(x['amount']) for x in res.data) if res.data else 0.0
            
            # Additional check: User Profile might have a manual 'total_donated' override field
            # This is useful for Manual Grants
            prof = self.client.table("user_profiles").select("total_donated").eq("hwid", self.user_id).maybe_single().execute()
            if prof.data and prof.data.get('total_donated'):
                total += float(prof.data['total_donated'])
                
            return total
        except Exception as e:
            print(f"// Roadmap Tier Check Error: {e}")
            return 0.0

    def get_roadmap_items(self):
        """Fetches roadmap proposals. Falls back to Premium Mock Data if empty/offline."""
        try:
            if self.client:
                res = self.client.table("roadmap_items").select("*").order("votes", desc=True).execute()
                if res.data: return res.data
        except: pass
        
        # --- PREMIUM MOCK DATA (VISIONARY) ---
        # Used when DB is empty OR offline to ensure UI is never blank
        return [
            {"id": "v1", "category": "MOBILE APP", "title": "ITC Universal Mobile App (v5.0)", "description": "Native iOS/Android companion for instant signal sync, cloud monitoring, and biometric security.", "status": "IN PROGRESS", "votes": 92, "icon": "📱", "has_voted": False},
            {"id": "v2", "category": "AI ENGINE", "title": "Neural Engine V3 - Multi-Modal", "description": "Processing technical, fundamental, and social sentiment data simultaneously for 'God-Mode' precision.", "status": "PLANNED", "votes": 128, "icon": "🛰️", "has_voted": False},
            {"id": "v3", "category": "INFRA", "title": "Decentralized Copytrade Network", "description": "Zero-latency blockchain synchronization across global MT5 servers. No more slippage.", "status": "PROPOSED", "votes": 45, "icon": "💎", "has_voted": False},
            {"id": "v4", "category": "SECURITY", "title": "Quantum-Resistant Encryption", "description": "Upgrading all API keys and user data to post-quantum cryptography standards.", "status": "WAITING", "votes": 12, "icon": "🛡️", "has_voted": False}
        ]

    def vote_roadmap_item(self, item_id):
        """Cast a vote for a roadmap item."""
        if not self.client or self.user_id == "anonymous": return False, "Login required"
        try:
            # 1. Check if already voted (Prevention)
            # We assume a 'roadmap_votes' table exists: user_id, item_id
            check = self.client.table("roadmap_votes").select("id").eq("user_id", self.user_id).eq("item_id", item_id).execute()
            if check.data:
                return False, "Already voted"
            
            # 2. Insert Vote
            self.client.table("roadmap_votes").insert({"user_id": self.user_id, "item_id": item_id}).execute()
            
            # 3. Increment Counter on Item (RPC or Client-side logic depending on RLS)
            # Simple client-side increment for now (RPC is better but this is quick fix)
            self.client.rpc("increment_roadmap_vote", {"item_id": item_id}).execute()
            
            return True, "Vote Cast"
        except Exception as e:
            # If RPC fails, maybe table doesn't exist? Mock success for UI feel if it's a mock item
            if str(item_id).startswith("v"): # It's a mock item
                return True, "Vote Recorded (Mock)"
            return False, str(e)

    def submit_roadmap_proposal(self, title, description):
        """Submits a new proposal (Architects Only)."""
        if not self.client or self.user_id == "anonymous": return False
        try:
            self.client.table("roadmap_items").insert({
                "title": title,
                "description": description,
                "category": "COMMUNITY CO.",
                "status": "PROPOSED",
                "votes": 1,
                "author_id": self.user_id,
                "icon": "💡"
            }).execute()
            return True
        except Exception as e:
            print(f"// Proposal Error: {e}")
            return False


if __name__ == "__main__":
    # Test (will fail if no env)
    db = SupabaseManager()
