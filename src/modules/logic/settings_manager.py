import os
import threading
from dotenv import set_key
from CTkMessagebox import CTkMessagebox

class SettingsManager:
    """
    Handles environment configuration, .env saving/loading, and privacy settings.
    Follows Gravity Dev Rules: Separation of Logic.
    """
    
    @staticmethod
    def save_config(parent):
        """Save all configuration from the UI entries to .env file"""
        env_path = ".env"
        
        try:
            # Telegram Settings
            if hasattr(parent, 'entry_api_id'):
                set_key(env_path, "TG_API_ID", parent.entry_api_id.get())
            if hasattr(parent, 'entry_api_hash'):
                set_key(env_path, "TG_API_HASH", parent.entry_api_hash.get())
            if hasattr(parent, 'entry_channels'):
                set_key(env_path, "TG_CHANNELS", parent.entry_channels.get())
            
            # MT5 Settings
            if hasattr(parent, 'entry_mt5_login'):
                set_key(env_path, "MT5_LOGIN", parent.entry_mt5_login.get())
            if hasattr(parent, 'entry_mt5_pass'):
                set_key(env_path, "MT5_PASSWORD", parent.entry_mt5_pass.get())
            if hasattr(parent, 'entry_mt5_server'):
                set_key(env_path, "MT5_SERVER", parent.entry_mt5_server.get())
            
            # Trading Rules
            if hasattr(parent, 'entry_risk'):
                set_key(env_path, "RISK_PERCENT", parent.entry_risk.get())
            if hasattr(parent, 'entry_lot'):
                set_key(env_path, "FIXED_LOT", parent.entry_lot.get())
            if hasattr(parent, 'entry_magic'):
                set_key(env_path, "MAGIC_NUMBER", parent.entry_magic.get())
            if hasattr(parent, 'entry_suffix'):
                set_key(env_path, "SYMBOL_SUFFIX", parent.entry_suffix.get())
            if hasattr(parent, 'chk_auto_exec'):
                set_key(env_path, "AUTO_EXECUTE", str(parent.chk_auto_exec.get()))
            
            # SL/TP Override Settings
            if hasattr(parent, 'sltp_mode'):
                set_key(env_path, "SLTP_MODE", parent.sltp_mode.get())
            if hasattr(parent, 'entry_sl_pips'):
                set_key(env_path, "MANUAL_SL_PIPS", parent.entry_sl_pips.get())
            if hasattr(parent, 'entry_tp_pips'):
                set_key(env_path, "MANUAL_TP_PIPS", parent.entry_tp_pips.get())
            
            # Risk Management
            if hasattr(parent, 'entry_loss_limit'):
                set_key(env_path, "DAILY_LOSS_LIMIT", parent.entry_loss_limit.get())
            if hasattr(parent, 'entry_start'):
                set_key(env_path, "TRADE_START_HOUR", parent.entry_start.get())
            if hasattr(parent, 'entry_end'):
                set_key(env_path, "TRADE_END_HOUR", parent.entry_end.get())
            
            # AI Settings
            if hasattr(parent, 'ai_enabled'):
                set_key(env_path, "USE_AI", str(parent.ai_enabled.get()))
            if hasattr(parent, 'ai_provider'):
                set_key(env_path, "AI_PROVIDER", parent.ai_provider.get())
            if hasattr(parent, 'entry_ai_key'):
                set_key(env_path, "AI_API_KEY", parent.entry_ai_key.get())
            
            if hasattr(parent, 'entry_user_name'):
                set_key(env_path, "USER_NAME", parent.entry_user_name.get())
            if hasattr(parent, 'entry_user_email'):
                set_key(env_path, "USER_EMAIL", parent.entry_user_email.get())
            if hasattr(parent, 'entry_user_phone'):
                set_key(env_path, "USER_PHONE", parent.entry_user_phone.get())
                
            # Notification Settings
            if hasattr(parent, 'entry_bot_token'):
                set_key(env_path, "REPORT_BOT_TOKEN", parent.entry_bot_token.get())
            if hasattr(parent, 'entry_report_id'):
                set_key(env_path, "REPORT_CHAT_ID", parent.entry_report_id.get())
            
            # Privacy & Social
            if hasattr(parent, 'chk_pub_profit'):
                set_key(env_path, "PUBLISH_PROFIT", str(parent.chk_pub_profit.get()))
            if hasattr(parent, 'chk_pub_edu'):
                set_key(env_path, "PUBLISH_KNOWLEDGE", str(parent.chk_pub_edu.get()))
            if hasattr(parent, 'chk_initials'):
                set_key(env_path, "PUBLISH_INITIALS", str(parent.chk_initials.get()))
            if hasattr(parent, 'chk_show_hints'):
                set_key(env_path, "SHOW_HINTS", str(parent.chk_show_hints.get()))

            # Language Settings
            if hasattr(parent, 'lang_selector'):
                selected_raw = parent.lang_selector.get() 
                new_lang_code = selected_raw.split(" ")[0]
                set_key(env_path, "APP_LANGUAGE", new_lang_code)
                
                if new_lang_code != parent.translator.lang_code:
                    CTkMessagebox(title=parent.translator.get("popup_restart_title"), 
                                   message=parent.translator.get("popup_restart_msg"), 
                                   icon="info")

            # Cloud Sync
            if hasattr(parent, 'db_manager'):
                profile_data = {
                    "publish_profit": parent.chk_pub_profit.get() if hasattr(parent, 'chk_pub_profit') else False,
                    "publish_knowledge": parent.chk_pub_edu.get() if hasattr(parent, 'chk_pub_edu') else False,
                    "publish_initials_only": parent.chk_initials.get() if hasattr(parent, 'chk_initials') else True,
                    "ui_hints_enabled": parent.chk_show_hints.get() if hasattr(parent, 'chk_show_hints') else True
                }
                threading.Thread(target=lambda: parent.db_manager.sync_user_profile(profile_data), daemon=True).start()

            # Sync Analyzer
            if hasattr(parent, 'analyzer'):
                parent.analyzer.update_settings()
                
            parent.log("INFO", "✅ All settings saved and synced to Cloud!")
            CTkMessagebox(title="Success", message=parent.translator.get("popup_save_success"), icon="check")

        except Exception as e:
            parent.log("ERROR", f"Failed to save: {e}")

    @staticmethod
    def load_privacy_settings(parent):
        """Loads privacy toggles from environment with robust boolean check"""
        try:
            def is_true(val): return str(val).lower() in ["true", "1"]
            
            if is_true(os.getenv("PUBLISH_PROFIT")): parent.chk_pub_profit.select()
            if is_true(os.getenv("PUBLISH_KNOWLEDGE")): parent.chk_pub_edu.select()
            if is_true(os.getenv("PUBLISH_INITIALS")): parent.chk_initials.select()
            if is_true(os.getenv("SHOW_HINTS", "True")): parent.chk_show_hints.select()
        except:
            pass
