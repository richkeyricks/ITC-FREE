import os
import json
import threading
from dotenv import set_key
from CTkMessagebox import CTkMessagebox

class ConfigAggregator:
    """
    Handles complex configuration gathering and persistence.
    Follows Gravity Dev Rules: Business Logic separation.
    """

    @staticmethod
    def get_current_config_dict(parent):
        """Extracts current UI state into a Dictionary for Cloud Storage"""
        data = {}
        try:
            # Telegram
            if hasattr(parent, 'entry_channels'): data['channels'] = parent.entry_channels.get()
            
            # MT5 Credentials (Optional security choice: maybe don't sync password?)
            if hasattr(parent, 'entry_mt5_login'): data['mt5_login'] = parent.entry_mt5_login.get()
            if hasattr(parent, 'entry_mt5_pass'): data['mt5_password'] = parent.entry_mt5_pass.get()
            if hasattr(parent, 'entry_mt5_server'): data['mt5_server'] = parent.entry_mt5_server.get()
            
            # Trade Rules
            if hasattr(parent, 'entry_risk'): data['risk'] = parent.entry_risk.get()
            if hasattr(parent, 'entry_lot'): data['lot'] = parent.entry_lot.get()
            if hasattr(parent, 'entry_magic'): data['magic'] = parent.entry_magic.get()
            if hasattr(parent, 'entry_suffix'): data['suffix'] = parent.entry_suffix.get()
            if hasattr(parent, 'execution_mode'): data['mode'] = parent.execution_mode.get()
            
            # SL/TP
            if hasattr(parent, 'sltp_mode'): data['sltp_mode'] = parent.sltp_mode.get()
            if hasattr(parent, 'entry_sl_pips'): data['sl_pips'] = parent.entry_sl_pips.get()
            if hasattr(parent, 'entry_tp_pips'): data['tp_pips'] = parent.entry_tp_pips.get()
            
            # Risk Management
            if hasattr(parent, 'entry_loss_limit'): data['daily_loss'] = parent.entry_loss_limit.get()
            if hasattr(parent, 'entry_start'): data['start_hour'] = parent.entry_start.get()
            if hasattr(parent, 'entry_end'): data['end_hour'] = parent.entry_end.get()
            
            # AI
            if hasattr(parent, 'use_ai_parsing'): data['use_ai'] = str(parent.use_ai_parsing.get())
            if hasattr(parent, 'ai_provider'): data['ai_provider'] = parent.ai_provider.get()
            
            return data
        except Exception as e:
            print(f"// Config Extract Error: {e}")
            return {}

    @staticmethod
    def apply_config_dict(parent, data):
        """Loads a dictionary of settings into the UI"""
        try:
            def set_val(entry, val):
                if entry and val is not None:
                    try:
                        entry.delete(0, 'end')
                        entry.insert(0, str(val))
                    except: 
                        # Variable or Checkbox handling
                        try: entry.set(val)
                        except: pass

            # Telegram
            if 'channels' in data and hasattr(parent, 'entry_channels'): set_val(parent.entry_channels, data['channels'])
            
            # MT5
            if 'mt5_login' in data and hasattr(parent, 'entry_mt5_login'): set_val(parent.entry_mt5_login, data['mt5_login'])
            if 'mt5_password' in data and hasattr(parent, 'entry_mt5_pass'): set_val(parent.entry_mt5_pass, data['mt5_password'])
            if 'mt5_server' in data and hasattr(parent, 'entry_mt5_server'): set_val(parent.entry_mt5_server, data['mt5_server'])
            
            # Trade Rules
            if 'risk' in data and hasattr(parent, 'entry_risk'): set_val(parent.entry_risk, data['risk'])
            if 'lot' in data and hasattr(parent, 'entry_lot'): set_val(parent.entry_lot, data['lot'])
            if 'magic' in data and hasattr(parent, 'entry_magic'): set_val(parent.entry_magic, data['magic'])
            if 'suffix' in data and hasattr(parent, 'entry_suffix'): set_val(parent.entry_suffix, data['suffix'])
            if 'mode' in data and hasattr(parent, 'execution_mode'): parent.execution_mode.set(data['mode'])
            
            # SL/TP
            if 'sltp_mode' in data and hasattr(parent, 'sltp_mode'): parent.sltp_mode.set(data['sltp_mode'])
            if 'sl_pips' in data and hasattr(parent, 'entry_sl_pips'): set_val(parent.entry_sl_pips, data['sl_pips'])
            if 'tp_pips' in data and hasattr(parent, 'entry_tp_pips'): set_val(parent.entry_tp_pips, data['tp_pips'])
            
            # Risk Mgmt
            if 'daily_loss' in data and hasattr(parent, 'entry_loss_limit'): set_val(parent.entry_loss_limit, data['daily_loss'])
            if 'start_hour' in data and hasattr(parent, 'entry_start'): set_val(parent.entry_start, data['start_hour'])
            if 'end_hour' in data and hasattr(parent, 'entry_end'): set_val(parent.entry_end, data['end_hour'])

            # AI
            if 'ai_provider' in data and hasattr(parent, 'ai_provider'): parent.ai_provider.set(data['ai_provider'])
            
            return True
        except Exception as e:
            print(f"// Apply Config Error: {e}")
            return False

    @staticmethod
    def save_config(parent):
        """Save all configuration to .env file and Cloud (Updates Runtime Env too)"""
        env_path = ".env"
        
        # Helper to update both Disk .env and Runtime os.environ
        def save_var(key, value):
            if value is not None:
                val_str = str(value)
                try: set_key(env_path, key, val_str)
                except: pass
                os.environ[key] = val_str

        try:
            # Telegram Settings
            if hasattr(parent, 'entry_api_id'): save_var("TG_API_ID", parent.entry_api_id.get())
            if hasattr(parent, 'entry_api_hash'): save_var("TG_API_HASH", parent.entry_api_hash.get())
            if hasattr(parent, 'entry_channels'): 
                # --- Channel Limit Enforcement ---
                raw_channels = parent.entry_channels.get()
                if raw_channels and hasattr(parent, 'db_manager'):
                    import re
                    c_list = re.split(r'[;,]', raw_channels)
                    c_list = [c.strip() for c in c_list if c.strip()]
                    
                    limit = parent.db_manager.get_channel_limit()
                    if len(c_list) > limit:
                        tier = parent.db_manager.get_user_tier()
                        truncated = c_list[:limit]
                        final_channels = ", ".join(truncated)
                        
                        # Update UI to reflect limit
                        parent.entry_channels.delete(0, 'end')
                        parent.entry_channels.insert(0, final_channels)
                        
                        CTkMessagebox(title="Quota Limit", 
                                       message=f"Batas Channel Terlampaui!\n\nLevel {tier} hanya diperbolehkan memantau {limit} channel aktif.\nSistem telah membatasi ke {limit} channel pertama.", 
                                       icon="warning")
                
                save_var("TG_CHANNELS", parent.entry_channels.get())
            
            # MT5 Settings
            if hasattr(parent, 'entry_mt5_login'): save_var("MT5_LOGIN", parent.entry_mt5_login.get())
            if hasattr(parent, 'entry_mt5_pass'): save_var("MT5_PASSWORD", parent.entry_mt5_pass.get())
            if hasattr(parent, 'entry_mt5_server'): save_var("MT5_SERVER", parent.entry_mt5_server.get())
            
            # Trading Rules
            if hasattr(parent, 'entry_risk'): save_var("RISK_PERCENT", parent.entry_risk.get())
            if hasattr(parent, 'entry_lot'): save_var("FIXED_LOT", parent.entry_lot.get())
            if hasattr(parent, 'entry_magic'): save_var("MAGIC_NUMBER", parent.entry_magic.get())
            if hasattr(parent, 'entry_suffix'): save_var("SYMBOL_SUFFIX", parent.entry_suffix.get())
            if hasattr(parent, 'execution_mode'): save_var("EXECUTION_MODE", parent.execution_mode.get())
            
            # SL/TP Override Settings
            if hasattr(parent, 'sltp_mode'): save_var("SLTP_MODE", parent.sltp_mode.get())
            if hasattr(parent, 'entry_sl_pips'): save_var("MANUAL_SL_PIPS", parent.entry_sl_pips.get())
            if hasattr(parent, 'entry_tp_pips'): save_var("MANUAL_TP_PIPS", parent.entry_tp_pips.get())
            
            # Risk Management
            if hasattr(parent, 'entry_loss_limit'): save_var("DAILY_LOSS_LIMIT", parent.entry_loss_limit.get())
            if hasattr(parent, 'entry_start'): save_var("TRADE_START_HOUR", parent.entry_start.get())
            if hasattr(parent, 'entry_end'): save_var("TRADE_END_HOUR", parent.entry_end.get())
            
            # AI Settings (Now split between Telegram and AI View)
            if hasattr(parent, 'use_ai_parsing'): save_var("USE_AI", str(parent.use_ai_parsing.get()))
            if hasattr(parent, 'ai_provider'): save_var("AI_PROVIDER", parent.ai_provider.get())
            if hasattr(parent, 'entry_ai_key'): save_var("AI_API_KEY", parent.entry_ai_key.get())
            
            # User Info
            if hasattr(parent, 'entry_user_name'): save_var("USER_NAME", parent.entry_user_name.get())
            if hasattr(parent, 'entry_user_email'): save_var("USER_EMAIL", parent.entry_user_email.get())
            if hasattr(parent, 'entry_user_phone'): save_var("USER_PHONE", parent.entry_user_phone.get())
            
            # Country Settings (New)
            if hasattr(parent, 'entry_user_country'):
                raw_c = parent.entry_user_country.get()
                code = raw_c.split(" ")[0] if raw_c else "ID"
                save_var("USER_COUNTRY", code)
                
            # Notifications
            if hasattr(parent, 'entry_bot_token'): save_var("REPORT_BOT_TOKEN", parent.entry_bot_token.get())
            if hasattr(parent, 'entry_report_id'): save_var("REPORT_CHAT_ID", parent.entry_report_id.get())
            
            # Privacy & Social
            if hasattr(parent, 'chk_pub_profit'): save_var("PUBLISH_PROFIT", str(parent.chk_pub_profit.get()))
            if hasattr(parent, 'chk_pub_edu'): save_var("PUBLISH_KNOWLEDGE", str(parent.chk_pub_edu.get()))
            if hasattr(parent, 'chk_initials'): save_var("PUBLISH_INITIALS", str(parent.chk_initials.get()))
            if hasattr(parent, 'chk_show_hints'): save_var("SHOW_HINTS", str(parent.chk_show_hints.get()))
 
            # Language Settings
            if hasattr(parent, 'lang_selector'):
                selected_raw = parent.lang_selector.get()
                new_lang_code = selected_raw.split(" ")[0]
                save_var("APP_LANGUAGE", new_lang_code)
                if new_lang_code != parent.translator.lang_code:
                    CTkMessagebox(title=parent.translator.get("popup_restart_title"), 
                                   message=parent.translator.get("popup_restart_msg"), 
                                   icon="info")
 
            # Cloud Sync
            if hasattr(parent, 'db_manager'):
                c_code = "ID"
                if hasattr(parent, 'entry_user_country'):
                     c_code = parent.entry_user_country.get().split(" ")[0]
                elif os.getenv("USER_COUNTRY"):
                     c_code = os.getenv("USER_COUNTRY")
 
                # Collect Full Trading Config
                trading_config = ConfigAggregator.get_current_config_dict(parent)
 
                profile_data = {
                    "name": parent.entry_user_name.get() if hasattr(parent, 'entry_user_name') else os.getenv("USER_NAME"),
                    "email": parent.entry_user_email.get() if hasattr(parent, 'entry_user_email') else os.getenv("USER_EMAIL"),
                    "phone": parent.entry_user_phone.get() if hasattr(parent, 'entry_user_phone') else "",
                    "country": c_code,
                    "app_version": getattr(parent, 'APP_VERSION', "2.1.2"), # Sync version
                    "publish_profit": parent.chk_pub_profit.get() if hasattr(parent, 'chk_pub_profit') else False,
                    "publish_knowledge": parent.chk_pub_edu.get() if hasattr(parent, 'chk_pub_edu') else False,
                    "publish_initials_only": parent.chk_initials.get() if hasattr(parent, 'chk_initials') else True,
                    "ui_hints_enabled": parent.chk_show_hints.get() if hasattr(parent, 'chk_show_hints') else True,
                    "trading_config": json.dumps(trading_config) if isinstance(trading_config, dict) else trading_config # CRITICAL FIX: Serialize as proper JSON with double quotes
                }
                threading.Thread(target=lambda: parent.db_manager.sync_user_profile(profile_data), daemon=True).start()
 
            # Sync Analyzer
            if hasattr(parent, 'analyzer'):
                parent.analyzer.update_settings()
                
            parent.log("INFO", "✅ All settings saved and synced to Cloud!")
            CTkMessagebox(title="Success", message=parent.translator.get("popup_save_success"), icon="check")
 
        except Exception as e:
            parent.log("ERROR", f"Failed to save settings: {e}")

    @staticmethod
    def load_privacy_settings(parent):
        """Loads privacy toggles from environment with robust boolean check"""
        try:
            def is_true(val): return str(val).lower() in ["true", "1"]
            
            if is_true(os.getenv("PUBLISH_PROFIT")) and hasattr(parent, 'chk_pub_profit'): parent.chk_pub_profit.select()
            if is_true(os.getenv("PUBLISH_KNOWLEDGE")) and hasattr(parent, 'chk_pub_edu'): parent.chk_pub_edu.select()
            if is_true(os.getenv("PUBLISH_INITIALS")) and hasattr(parent, 'chk_initials'): parent.chk_initials.select()
            if is_true(os.getenv("SHOW_HINTS", "True")) and hasattr(parent, 'chk_show_hints'): parent.chk_show_hints.select()
        except:
            pass
