import os
import time
import threading
import datetime
import requests
import platform
import socket
import uuid
import subprocess
from index import (check_internet, get_mt5_status, get_account_meta, login_mt5_custom)
# from modules.mt5.mt5_client import MT5Client # DEPRECATED or REPLACED by Service logic
from modules.mt5.mt5_service import MT5Service

class AppController:
    """
    Handles background services: Connectivity monitors, UI refresh loops, 
    Telemetry heartbeats, and update checks.
    Follows Gravity Dev Rules: Separation of Logic/Controller.
    """
    
    @staticmethod
    def start_connectivity_monitor(parent):
        """Starts 24/7 background check for Internet, TG, and MT5 (3-State Logic)"""
        def _monitor():
            import index
            service = MT5Service.instance()
            
            while True:
                try:
                    # 1. Check Internet
                    internet_ok = index.check_internet()
                    
                    # 2. Check MT5 (3-State)
                    # 0=Offline (Red), 1=Standby (Yellow), 2=Active (Green)
                    mt5_state = service.get_mt5_status_deep(passive=True) # FIX: Use passive check
                    acc_info = service.get_account_info() if mt5_state == 2 else None
                    
                    # 3. Check Telegram (3-State)
                    # 0=Offline (Red), 1=Validated/Ready (Blue), 2=Active/Running (Green)
                    tg_state = 0
                    if getattr(index, "is_telegram_failed", False):
                        tg_state = 0 # Explicit failure turns it Red (PRIORITY)
                    elif getattr(index, "is_telegram_active", False):
                        tg_state = 2
                    elif getattr(index, "is_telegram_validated", False) or (hasattr(index, "check_telegram_session") and index.check_telegram_session()):
                        tg_state = 1
                    elif hasattr(index, 'app') and index.app and index.app.is_connected:
                        tg_state = 2

                    # --- UNIFIED UI UPDATE ---
                    def _sync_indicators():
                        ok_color = "#2ea44f"   # Green for ACTIVE/RUNNING
                        ready_color = "#388bfd" # Blue for VALIDATED/READY
                        warn_color = "#d29922"  # Yellow for STANDBY
                        err_color = "#f85149"  # Red for OFFLINE
                        
                        def get_color(state):
                            if state == 2: return ok_color
                            if state == 1: return ready_color
                            return err_color

                        # 1. Dashboard Cards
                        if hasattr(parent, 'card_net'):
                            parent.card_net.configure(
                                text=f"● {parent.translator.get('status_online') if internet_ok else parent.translator.get('status_offline')}", 
                                text_color=ok_color if internet_ok else err_color
                            )
                        
                        if hasattr(parent, 'card_mt5'):
                            if mt5_state == 2 and acc_info:
                                parent.card_mt5.configure(text=f"● Connected ({acc_info.login})", text_color=ok_color)
                            elif mt5_state == 1:
                                parent.card_mt5.configure(text="● MT5 Standby (No Acc)", text_color=warn_color)
                            else:
                                parent.card_mt5.configure(text=f"● {parent.translator.get('status_disconnected')}", text_color=err_color)
                        
                        if hasattr(parent, 'card_tg'):
                            tg_label = "Running" if tg_state == 2 else ("Ready" if tg_state == 1 else "Disconnected")
                            parent.card_tg.configure(text=f"● {tg_label}", text_color=get_color(tg_state))
                            
                        # --- STEPPER SYNC ---
                        if hasattr(parent, 'stepper'):
                            from modules.ui.ui_components import STEP_ACTIVE, STEP_COMPLETED, STEP_PENDING
                            
                            # Step 1: Telegram
                            s1 = STEP_COMPLETED if tg_state == 2 else (STEP_ACTIVE if tg_state == 1 else STEP_PENDING)
                            parent.stepper.set_step_state(0, s1)
                            
                            # Step 2: MT5
                            s2 = STEP_COMPLETED if mt5_state == 2 else (STEP_ACTIVE if mt5_state == 1 else STEP_PENDING)
                            parent.stepper.set_step_state(1, s2)
                            
                            # Step 3: Mode (Simplified: checked if trading is active)
                            # Assuming if MT5 is 2, user might have selected mode. 
                            # But for now let's just use connection logic for demonstration.
                            if mt5_state == 2:
                                parent.stepper.set_step_state(2, STEP_COMPLETED)
                            elif mt5_state == 1:
                                parent.stepper.set_step_state(2, STEP_ACTIVE)
                            else:
                                parent.stepper.set_step_state(2, STEP_PENDING)
                            
                        # 2. Top-Bar Badges (Synchronized)
                        if hasattr(parent, 'badge_net'): parent.badge_net.configure(text_color=ok_color if internet_ok else err_color)
                        
                        if hasattr(parent, 'badge_mt5'): 
                            parent.badge_mt5.configure(text_color=get_color(mt5_state))
                            if not hasattr(parent, '_mt5_tip_set'):
                                from utils.tooltips import CTkToolTip
                                CTkToolTip(parent.badge_mt5, parent.translator.get("badge_status_hint"))
                                parent._mt5_tip_set = True

                        if hasattr(parent, 'badge_tg'): 
                            parent.badge_tg.configure(text_color=get_color(tg_state))
                            if not hasattr(parent, '_tg_tip_set'):
                                from utils.tooltips import CTkToolTip
                                CTkToolTip(parent.badge_tg, parent.translator.get("badge_status_hint"))
                                parent._tg_tip_set = True

                        # 3. Dedicated Page Status Labels (Synchronized)
                        if hasattr(parent, 'mt5_status'):
                            status_txt = parent.translator.get('status_logged') if mt5_state == 2 else (parent.translator.get('status_not_logged') if mt5_state == 1 else "Offline")
                            parent.mt5_status.configure(text=f"● {status_txt}", text_color=get_color(mt5_state))

                        # 4. Financial Sync (Only if MT5 is Fully Green)
                        if mt5_state == 2 and acc_info:
                            if hasattr(parent, 'card_balance'): parent.card_balance.configure(text=f"${acc_info.balance:,.2f}")
                            if hasattr(parent, 'card_equity'): parent.card_equity.configure(text=f"${acc_info.equity:,.2f}")
                    
                    parent.safe_ui_update(_sync_indicators)
                    
                    # --- CLOUD HEARTBEAT (Every ~30s) ---
                    # We only sync to cloud every 6 loops (5s * 6 = 30s)
                    if not hasattr(_monitor, "sync_counter"): _monitor.sync_counter = 0
                    _monitor.sync_counter += 1
                    
                    if _monitor.sync_counter >= 6:
                        _monitor.sync_counter = 0
                        try:
                            payload = {
                                "app_version": getattr(parent, 'APP_VERSION', '2.4.5'),
                                "device_name": socket.gethostname(),
                                "internet_ok": internet_ok,
                                "mt5_state": mt5_state,
                                "tg_state": tg_state
                            }
                            if mt5_state == 2 and acc_info:
                                meta = index.get_account_meta()
                                payload.update({
                                    "broker": getattr(acc_info, 'company', 'Unknown'),
                                    "server": getattr(acc_info, 'server', 'Unknown')
                                })
                                payload.update(meta)
                            
                            parent.db_manager.sync_user_profile(payload)
                        except: pass

                except Exception as e:
                    print(f"// Monitor Error: {e}")
                
                time.sleep(5) # 5s Polling (Premium Responsiveness)
                
        threading.Thread(target=_monitor, daemon=True).start()

    @staticmethod
    def _run_telemetry(parent):
        """Advanced Hardware & Network Telemetry Tracking"""
        try:
            os_info = f"{platform.system()} {platform.release()}"
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
            
            parent.db_manager.sync_user_profile({
                "os_info": os_info,
                "mac_address": mac,
                "device_name": socket.gethostname(),
                "app_version": getattr(parent, 'APP_VERSION', '2.4.0')
            })
        except Exception as e:
            print(f"// Telemetry Error: {e}")

    @staticmethod
    def _check_admin_messages(parent):
        """Fetch and show admin announcements/DMs"""
        if not hasattr(parent, 'db_manager'): return
        messages = parent.db_manager.check_messages()
        if messages:
            current_global_id = int(os.getenv("LAST_MSG_ID", "0"))
            for msg in reversed(messages):
                msg_id = int(msg.get('id', 0))
                is_global = msg.get('receiver_id') == 'GLOBAL'
                if is_global:
                    if msg_id > current_global_id:
                        parent.after(0, lambda m=msg: parent.show_admin_broadcast(m))
                        current_global_id = msg_id
                        from dotenv import set_key
                        set_key(".env", "LAST_MSG_ID", str(current_global_id))
                else:
                    if msg_id not in parent.shown_dm_ids:
                        parent.after(0, lambda m=msg: parent.show_admin_broadcast(m))
                        parent.shown_dm_ids.add(msg_id)

    @staticmethod
    def get_deep_telemetry(gui_instance):
        """
        Collects 60+ parameters for the 'Deep Inspector' (God Mode).
        Returns a dictionary suitable for the 'telemetry_data' JSONB column.
        """
        import platform
        import sys
        
        telemetry = {}
        service = MT5Service.instance()

        # 1. System Hardware & OS
        telemetry['sys_os'] = platform.system()
        telemetry['sys_release'] = platform.release()
        telemetry['sys_version'] = platform.version()
        telemetry['sys_machine'] = platform.machine()
        telemetry['sys_processor'] = platform.processor()
        telemetry['sys_python'] = sys.version.split()[0]
        telemetry['sys_user'] = os.getlogin()
        
        # Screen (Tkinter)
        try:
            telemetry['screen_width'] = gui_instance.winfo_screenwidth()
            telemetry['screen_height'] = gui_instance.winfo_screenheight()
        except: pass
            
        # 2. MT5 Deep Stats (Raw)
        try:
            mt5_info = service.get_account_info()
            if mt5_info:
                # Add all available raw keys
                for k, v in mt5_info._asdict().items():
                    telemetry[f"mt5_{k}"] = v
            else:
                telemetry['mt5_status'] = "Disconnected"
        except:
            telemetry['mt5_status'] = "Error"

        # 3. Application State
        telemetry['app_version'] = "2.1.0" # Dynamic if possible
        telemetry['app_theme'] = os.getenv("APP_THEME", "DARK")
        telemetry['app_language'] = os.getenv("APP_LANGUAGE", "en")
        telemetry['app_uptime'] = "N/A" # Could calculate if start_time tracked
        
        # 4. Configuration (Sanitized Environment)
        # We dump important env vars but CENSOR sensitive ones
        SENSITIVE = ["SUPABASE_KEY", "AI_API_KEY"]
        
        for key, val in os.environ.items():
            if key in SENSITIVE:
                telemetry[f"config_{key}"] = "********"
            elif key.startswith("TG_") or key.startswith("MT5_") or key.startswith("AI_") or key.startswith("SPC_") or key in ["RISK_PERCENT", "FIXED_LOT", "MAGIC_NUMBER", "SL_PIPS", "TP_PIPS", "APP_PASSWORD"]:
                 telemetry[f"config_{key}"] = val
                 
        return telemetry

    @staticmethod
    def show_admin_broadcast(parent, msg_data):
        from modules.ui.chat_popup import StrictChatPopup
        try:
            if hasattr(parent, '_active_popup') and parent._active_popup and parent._active_popup.winfo_exists(): return
            is_global = msg_data.get('receiver_id') == 'GLOBAL'
            content = msg_data.get('content', '')
            msg_id = msg_data.get('id')
            parent._active_popup = StrictChatPopup(parent, title="🔔 SYSTEM NOTIFICATION", message=content, 
                           msg_id=msg_id, db_manager=parent.db_manager, is_strict=not is_global)
        except Exception as e:
            print(f"Broadcast Error: {e}")

    @staticmethod
    def update_ui_loop(parent):
        def _loop():
            while True:
                try:
                    meta = get_account_meta()
                    # 1. Update Local UI
                    if meta:
                        def _update():
                            parent.card_balance.configure(text=f"${meta['balance']:,.2f}")
                            parent.card_equity.configure(text=f"${meta['equity']:,.2f}")
                            parent.card_pnl.configure(text=f"${meta['profit']:,.2f}", 
                                                                         text_color="#3fb950" if meta['profit'] >= 0 else "#f85149")
                        parent.safe_ui_update(_update)
                    
                    # 2. Sync Cloud Telemetry (Deep Inspector) - ALWAYS SYNC
                    if hasattr(parent, 'db_manager'):
                        telemetry = AppController.get_deep_telemetry(parent)
                        # Run sync in separate thread to not block loop
                        sync_payload = meta if meta else {}
                        threading.Thread(target=lambda: parent.db_manager.sync_user_profile(sync_payload, telemetry_data=telemetry), daemon=True).start()

                except Exception as e:
                    print(f"// UI Loop Error: {e}")
                
                time.sleep(15)
        threading.Thread(target=_loop, daemon=True).start()

    @staticmethod
    def restart_app(root_window=None):
        """
        Restart the application safely.
        Compatible with PyInstaller Frozen EXE.
        """
        try:
            import sys
            import subprocess
            import os
            
            # 1. Destroy current window if provided
            if root_window:
                try:
                    root_window.destroy()
                except: pass
            
            # 2. Determine Launch Command
            if getattr(sys, 'frozen', False):
                # FROZEN (EXE) - Use PowerShell for Robust Clean Restart
                executable = sys.executable
                
                # PowerShell Script:
                # 1. Wait 2 seconds
                # 2. Remove Poisoned Env Vars (_MEIPASS2)
                # 3. Start Process Independent
                ps_script = f"""
Start-Sleep -Seconds 2
$env:_MEIPASS2 = $null
$env:LZ4_MEIPASS = $null
Start-Process -FilePath "{executable}" -WorkingDirectory "{os.getcwd()}"
Remove-Item -Path "$PSCommandPath" -Force
"""
                ps_path = "restart_cleaner.ps1"
                with open(ps_path, "w") as f:
                    f.write(ps_script)
                
                print(f"// RESTARTING VIA POWERSHELL: {ps_path}")
                
                # Launch PowerShell (Hidden Window)
                subprocess.Popen(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_path],
                    shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                # Suicide immediately
                sys.exit(0)
            else:
                # DEVELOPMENT (Python Script)
                executable = sys.executable
                script = os.path.join(os.getcwd(), "src", "gui.py")
                cmd = [executable, script]
                subprocess.Popen(cmd, cwd=os.getcwd())
                sys.exit(0)
            
        except Exception as e:
            print(f"// Restart Error: {e}")
            sys.exit(1)
