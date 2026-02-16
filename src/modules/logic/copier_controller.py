import os
import threading
from CTkMessagebox import CTkMessagebox
from index import app as tg_app, get_mt5_status, create_telegram_client

class CopierController:
    """
    Handles Copier Lifecycle and Testing.
    Follows Gravity Dev Rules: Business Logic separation.
    """

    @staticmethod
    def start_copier(parent):
        """Starts the copier service with validation"""
        # Stop Check
        if getattr(parent, "copier_running", False):
            parent.copier_running = False
            parent.log("INFO", "🛑 Copier stopping... (waiting for clean shutdown)")
            from ui_theme import THEME_DARK
            parent.after(0, lambda: parent.btn_start.configure(state="normal", text="START COPIER", fg_color=THEME_DARK["accent_primary"]))
            # Note: run_telegram loop will detect copier_running=False and stop gracefully
            return

        # Input Validation
        errors = []
        if not hasattr(parent, 'entry_api_id') or not parent.entry_api_id.get().strip(): errors.append("TG_API_ID")
        if not hasattr(parent, 'entry_api_hash') or not parent.entry_api_hash.get().strip(): errors.append("TG_API_HASH")
        
        if errors:
            parent.log("ERROR", f"Missing: {', '.join(errors)}")
            return

        # Guard: Prevent double-click spawning multiple threads
        if hasattr(parent, '_copier_thread') and parent._copier_thread and parent._copier_thread.is_alive():
            parent.log("WARN", "⚠️ Copier already running!")
            return

        parent.copier_running = True
        parent.log("INFO", "🚀 Copier started!")
        from ui_theme import THEME_DARK
        parent.after(0, lambda: parent.btn_start.configure(state="normal", text="STOP COPIER", fg_color="#f85149"))

        # Import here to avoid circular
        from index import monitor_trades, set_signal_callback

        # Register callback for signals
        set_signal_callback(lambda sig: parent.on_signal_detected(sig))

        # Start background threads (store reference for guard check)
        threading.Thread(target=monitor_trades, daemon=True).start()
        parent._copier_thread = threading.Thread(target=lambda: CopierController.run_telegram(parent), daemon=True)
        parent._copier_thread.start()

    @staticmethod
    def run_telegram(parent):
        """Dedicated Telegram worker with isolated event loop and graceful stop."""
        import asyncio
        import index

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def _worker():
            # Clear stale client reference (test_telegram already disconnected it)
            index.app = None

            parent.log("INFO", "📡 Creating Telegram Client for Copier...")
            client = create_telegram_client(caller="RUN")

            if client is None:
                parent.log("ERROR", "❌ Telegram Client could not be created.")
                return

            try:
                await client.start()
                index.is_telegram_active = True
                parent.log("INFO", "✅ Telegram connected. Listening for signals...")

                # Graceful loop — checks copier_running every second
                while parent.copier_running:
                    await asyncio.sleep(1)

            except Exception as e:
                parent.log("ERROR", f"Telegram error: {e}")
                import traceback; traceback.print_exc()
            finally:
                # Clean shutdown
                index.is_telegram_active = False
                try:
                    if client.is_connected:
                        await client.stop()
                        parent.log("INFO", "📴 Telegram Client disconnected cleanly.")
                except Exception:
                    pass
                index.app = None

        try:
            loop.run_until_complete(_worker())
        except Exception as e:
            print(f"// Telegram worker error: {e}")
        finally:
            loop.close()
            parent.copier_running = False
            from ui_theme import THEME_DARK
            parent.after(0, lambda: parent.btn_start.configure(state="normal", text="START COPIER", fg_color=THEME_DARK["accent_primary"]))

    @staticmethod
    def emergency_close(parent):
        """Closes all trades and syncs logout"""
        import datetime
        from index import close_all_orders
        try:
            if hasattr(parent, 'db_manager'):
                 parent.db_manager.sync_user_profile({"last_logout": datetime.datetime.now(datetime.timezone.utc).isoformat()})
        except: pass
        
        if close_all_orders():
            parent.log("INFO", "🛑 All positions closed!")
        else:
            parent.log("ERROR", "Emergency close failed.")

    # --- PHASE 7: In-App Telegram Login (Industrial-Grade) ---

    @staticmethod
    def test_telegram(parent):
        """Tests Telegram connection with In-App OTP Login (Phase 7)."""
        if getattr(parent, "_tg_testing", False):
            parent.log("WARN", "⚠️ Test is already running. Please wait.")
            return
            
        parent._tg_testing = True
        
        def _test_task():
            import asyncio
            import index
            from pyrogram.errors import (
                ApiIdInvalid, AuthKeyUnregistered, UserDeactivated,
                UserDeactivatedBan, PhoneCodeInvalid, PhoneCodeExpired,
                SessionPasswordNeeded, PasswordHashInvalid
            )
            from index import create_telegram_client
            
            # --- RESET FLAGS ---
            index.is_telegram_validated = False
            index.is_telegram_failed = False
            
            # --- SESSION FILE PATH ---
            import index as idx_module
            session_dir = os.path.dirname(os.path.abspath(idx_module.__file__))
            session_file = os.path.join(session_dir, "itc_copier_session.session")
            session_journal = session_file + "-journal"
            
            print(f"// TG Auth: Session file: {session_file} (exists: {os.path.exists(session_file)})")
            
            # --- EVENT LOOP ---
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            except Exception as e:
                parent.log("ERROR", f"Loop Init Error: {e}")
                parent._tg_testing = False
                return

            parent.log("INFO", "📡 Starting Telegram connection test...")
            if hasattr(parent, 'tg_status'):
                parent.after(0, lambda: parent.tg_status.configure(text="● Connecting...", text_color="#388bfd"))
            
            # --- READ UI VALUES ---
            ui_api_id = parent.entry_api_id.get().strip() if hasattr(parent, 'entry_api_id') else None
            ui_api_hash = parent.entry_api_hash.get().strip() if hasattr(parent, 'entry_api_hash') else None
            ui_channels = parent.entry_channels.get().strip() if hasattr(parent, 'entry_channels') else None
            ui_phone = parent.entry_phone.get().strip() if hasattr(parent, 'entry_phone') else ""
            
            # Fallback phone sources
            if not ui_phone and hasattr(parent, 'entry_user_phone'):
                ui_phone = parent.entry_user_phone.get().strip()
            if not ui_phone:
                ui_phone = os.getenv("USER_PHONE", "").strip()
            
            print(f"// TG Auth: API ID: {ui_api_id[:4]}..." if ui_api_id and len(ui_api_id) >= 4 else "// TG Auth: No API ID")
            print(f"// TG Auth: Phone: {ui_phone[:6]}..." if ui_phone and len(ui_phone) >= 6 else "// TG Auth: No phone yet")
            
            # --- CREATE CLIENT ---
            client = create_telegram_client(caller="TEST", api_id=ui_api_id, api_hash=ui_api_hash, channels=ui_channels)
            if client is None:
                parent.log("ERROR", "❌ Test Failed: API ID or Hash is missing.")
                if hasattr(parent, 'tg_status'):
                    parent.after(0, lambda: parent.tg_status.configure(text="● Invalid Config", text_color="#f85149"))
                parent._tg_testing = False
                return

            # --- Helper: Delete session files ---
            def _delete_session():
                for f in [session_file, session_journal]:
                    if os.path.exists(f):
                        try:
                            os.remove(f)
                            print(f"// TG Auth: Deleted {f}")
                        except Exception as err:
                            print(f"// TG Auth: Failed to delete {f}: {err}")

            # --- Helper: Show popup on GUI thread and wait for result ---
            def _ask_popup(title, text):
                """Shows a CTkInputDialog on the main thread, returns result."""
                import customtkinter as ctk
                result = [None]
                event = threading.Event()
                def _show():
                    dialog = ctk.CTkInputDialog(text=text, title=title)
                    result[0] = dialog.get_input()
                    event.set()
                parent.after(0, _show)
                event.wait(timeout=120)
                return result[0]

            try:
                async def _run_auth():
                    nonlocal client, ui_phone
                    
                    # ========== STEP 1: CONNECT ==========
                    print("// TG Auth: Step 1 - Connecting...")
                    try:
                        await asyncio.wait_for(client.connect(), timeout=15)
                    except asyncio.TimeoutError:
                        parent.log("ERROR", "❌ Connection Timeout. Check internet.")
                        return "TIMEOUT", None
                    except ApiIdInvalid:
                        parent.log("ERROR", "❌ API ID or Hash is invalid!")
                        return "INVALID", None
                    
                    print("// TG Auth: MTProto connected.")
                    
                    # ========== STEP 2: CHECK EXISTING SESSION ==========
                    print("// TG Auth: Step 2 - Checking existing session...")
                    try:
                        me = await client.get_me()
                        if me:
                            parent.log("INFO", f"✅ Session valid! Connected as {me.first_name}")
                            print(f"// TG Auth: Session valid. User: {me.first_name} (@{me.username})")
                            return "SUCCESS", me.first_name
                    except (AuthKeyUnregistered, UserDeactivated, UserDeactivatedBan) as e:
                        print(f"// TG Auth: Session expired ({type(e).__name__}). Will login fresh.")
                        parent.log("INFO", "🔄 Session expired. Starting fresh login...")
                        # Disconnect and delete old session
                        try: await client.disconnect()
                        except: pass
                        _delete_session()
                        # Recreate client with fresh session
                        client = create_telegram_client(caller="TEST-REAUTH", api_id=ui_api_id, api_hash=ui_api_hash, channels=ui_channels)
                        if client is None:
                            return "ERROR", None
                        await asyncio.wait_for(client.connect(), timeout=15)
                    except Exception as e:
                        print(f"// TG Auth: get_me() failed ({e}). Proceeding to login...")
                    
                    # ========== STEP 3: GET PHONE NUMBER ==========
                    if not ui_phone:
                        print("// TG Auth: Step 3 - No phone. Showing popup...")
                        if hasattr(parent, 'tg_status'):
                            parent.after(0, lambda: parent.tg_status.configure(text="● Enter Phone...", text_color="#d29922"))
                        
                        ui_phone = _ask_popup(
                            "📱 Telegram Login",
                            "Masukkan nomor HP Telegram:\n(Contoh: +6281234567890)"
                        )
                        if not ui_phone or not ui_phone.strip():
                            parent.log("ERROR", "❌ Phone number required for login.")
                            return "ERROR", None
                        ui_phone = ui_phone.strip()
                    
                    # Normalize phone number
                    if not ui_phone.startswith("+"):
                        if ui_phone.startswith("0"):
                            ui_phone = "+62" + ui_phone[1:]
                        else:
                            ui_phone = "+" + ui_phone
                    
                    # ========== STEP 4: SEND OTP ==========
                    print(f"// TG Auth: Step 4 - Sending OTP to {ui_phone[:6]}...")
                    parent.log("INFO", f"📨 Sending OTP to {ui_phone[:6]}...")
                    if hasattr(parent, 'tg_status'):
                        parent.after(0, lambda: parent.tg_status.configure(text="● Sending OTP...", text_color="#d29922"))
                    
                    try:
                        sent_code = await client.send_code(ui_phone)
                        phone_code_hash = sent_code.phone_code_hash
                        print(f"// TG Auth: OTP sent! Hash: {phone_code_hash[:8]}...")
                    except ApiIdInvalid:
                        parent.log("ERROR", "❌ API ID/Hash invalid!")
                        return "INVALID", None
                    except Exception as e:
                        parent.log("ERROR", f"❌ Failed to send OTP: {e}")
                        print(f"// TG Auth: send_code error: {e}")
                        import traceback; traceback.print_exc()
                        return "ERROR", None
                    
                    # ========== STEP 5: OTP POPUP ==========
                    print("// TG Auth: Step 5 - Waiting for OTP from user...")
                    parent.log("INFO", "📲 OTP sent! Enter code in popup.")
                    if hasattr(parent, 'tg_status'):
                        parent.after(0, lambda: parent.tg_status.configure(text="● Enter OTP...", text_color="#d29922"))
                    
                    otp_code = _ask_popup(
                        "🔐 Telegram OTP",
                        f"Kode OTP dikirim ke {ui_phone}\nMasukkan kode verifikasi:"
                    )
                    if not otp_code or not otp_code.strip():
                        parent.log("ERROR", "❌ OTP not entered. Login cancelled.")
                        return "ERROR", None
                    
                    # ========== STEP 6: SIGN IN ==========
                    print(f"// TG Auth: Step 6 - Signing in...")
                    if hasattr(parent, 'tg_status'):
                        parent.after(0, lambda: parent.tg_status.configure(text="● Verifying...", text_color="#d29922"))
                    
                    try:
                        await client.sign_in(ui_phone, phone_code_hash, otp_code.strip())
                        me = await client.get_me()
                        if me:
                            parent.log("INFO", f"✅ Login Success! Welcome {me.first_name}")
                            print(f"// TG Auth: SUCCESS - {me.first_name} (@{me.username})")
                            return "SUCCESS", me.first_name
                        return "SUCCESS", "User"
                    
                    except SessionPasswordNeeded:
                        # ========== STEP 7: 2FA PASSWORD ==========
                        print("// TG Auth: Step 7 - 2FA required!")
                        parent.log("INFO", "🔒 Two-Factor Authentication required.")
                        if hasattr(parent, 'tg_status'):
                            parent.after(0, lambda: parent.tg_status.configure(text="● Enter 2FA...", text_color="#d29922"))
                        
                        password = _ask_popup(
                            "🔒 Two-Factor Authentication",
                            "Akun Anda memiliki 2FA.\nMasukkan password Telegram:"
                        )
                        if not password or not password.strip():
                            parent.log("ERROR", "❌ 2FA password not entered.")
                            return "ERROR", None
                        
                        try:
                            await client.check_password(password.strip())
                            me = await client.get_me()
                            parent.log("INFO", f"✅ 2FA Login Success! Welcome {me.first_name}")
                            print(f"// TG Auth: 2FA SUCCESS - {me.first_name}")
                            return "SUCCESS", me.first_name
                        except PasswordHashInvalid:
                            parent.log("ERROR", "❌ Wrong 2FA password!")
                            return "INVALID", None
                    
                    except PhoneCodeInvalid:
                        parent.log("ERROR", "❌ Wrong OTP code!")
                        return "INVALID", None
                    except PhoneCodeExpired:
                        parent.log("ERROR", "❌ OTP expired! Try again.")
                        return "TIMEOUT", None
                    except Exception as e:
                        parent.log("ERROR", f"❌ Login Error: {e}")
                        print(f"// TG Auth: sign_in error: {e}")
                        import traceback; traceback.print_exc()
                        return "ERROR", None

                # --- RUN THE AUTH FLOW ---
                status, name = loop.run_until_complete(_run_auth())
                
                # --- UPDATE UI ---
                def _update_ui():
                    if status == "SUCCESS":
                        index.is_telegram_validated = True
                        parent.is_telegram_validated = True
                        index.is_telegram_failed = False
                        parent.tg_status.configure(text=f"● Validated ({name})", text_color="#3fb950")
                        # AUTO-SYNC: Sync successful TG Auth to Cloud
                        threading.Thread(target=parent.save_config, daemon=True).start()
                        
                        # UX: Reveal "Start Copy Trading" Shortcut
                        if hasattr(parent, 'btn_start_copy_shortcut'):
                            parent.btn_start_copy_shortcut.pack(side="left", padx=(10, 0))
                            parent.btn_start_copy_shortcut.configure(state="normal")
                    elif status == "INVALID":
                        index.is_telegram_validated = False
                        parent.is_telegram_validated = False
                        index.is_telegram_failed = True
                        parent.tg_status.configure(text="● Auth Failed", text_color="#f85149")
                    elif status == "TIMEOUT":
                        index.is_telegram_validated = False
                        index.is_telegram_failed = True
                        parent.tg_status.configure(text="● Timeout / Expired", text_color="#f85149")
                    else:
                        index.is_telegram_validated = False
                        index.is_telegram_failed = True
                        parent.tg_status.configure(text="● Error", text_color="#f85149")
                    
                    # Note: Stepper & indicators are auto-synced by AppController monitoring loop (5s)
                
                if hasattr(parent, 'tg_status'):
                    parent.after(0, _update_ui)
                        
            except Exception as e:
                index.is_telegram_validated = False
                index.is_telegram_failed = True
                parent.log("ERROR", f"❌ Telegram Test Error: {e}")
                print(f"// TG Auth: OUTER ERROR: {e}")
                import traceback; traceback.print_exc()
                if hasattr(parent, 'tg_status'):
                    parent.after(0, lambda: parent.tg_status.configure(text="● Error", text_color="#f85149"))
            finally:
                # Disconnect client safely (must use async wrapper for Pyrogram hybrid method)
                try:
                    if client and client.is_connected:
                        async def _cleanup():
                            await client.disconnect()
                        loop.run_until_complete(_cleanup())
                        print("// TG Auth: Client disconnected. Session file released.")
                except Exception as e:
                    print(f"// TG Auth: Disconnect cleanup error: {e}")
                # Clear global reference so run_telegram creates fresh client
                index.app = None
                loop.close()
                parent._tg_testing = False

        threading.Thread(target=_test_task, daemon=True).start()

    @staticmethod
    def test_mt5(parent):
        """Tests MT5 connection using current UI credentials"""
        parent.log("INFO", "Testing MT5 login...")
        from modules.mt5.mt5_service import MT5Service
        
        # Extract credentials from UI if available
        login = int(parent.entry_mt5_login.get()) if hasattr(parent, 'entry_mt5_login') and parent.entry_mt5_login.get().isdigit() else None
        password = parent.entry_mt5_pass.get() if hasattr(parent, 'entry_mt5_pass') else ""
        server = parent.entry_mt5_server.get() if hasattr(parent, 'entry_mt5_server') else ""
        
        service = MT5Service.instance()
        
        # Initialize with explicit credentials
        if service.initialize(login=login, password=password, server=server):
            if hasattr(parent, 'mt5_status'):
                parent.mt5_status.configure(text="● Connected", text_color="#3fb950")
            parent.is_mt5_connected = True
            # Note: Stepper & indicators auto-synced by monitoring loop
            parent.log("INFO", f"✅ MT5 Login Success: {login}")
            
            # AUTO-SYNC: Save and Push to Cloud if successful
            threading.Thread(target=parent.save_config, daemon=True).start()
        else:
            if hasattr(parent, 'mt5_status'):
                parent.mt5_status.configure(text="● Failed", text_color="#f85149")
            parent.log("ERROR", "❌ MT5 Login Failed. Check credentials.")

    @staticmethod
    def open_history(parent):
        """Opens trade history CSV"""
        if os.path.exists('trade_history.csv'):
            os.startfile('trade_history.csv')
        else:
            parent.log("WARN", "No trade history found.")
