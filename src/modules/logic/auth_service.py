import os
import sys
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from index import (get_env_list)

class AuthService:
    """
    Handles Authentication Screen, EULA, and License validation.
    Follows Gravity Dev Rules: Separate Logic and Presentation.
    """
    
    @staticmethod
    def check_initial_auth(parent):
        """Routing logic at startup"""
        try:
            if parent.db_manager.user_id != "anonymous":
                # --- CHECK BAN STATUS ---
                if parent.db_manager.get_ban_status(parent.db_manager.user_id):
                    parent.withdraw()
                    CTkMessagebox(title="LICENSE REVOKED", 
                                  message="ACCESS DENIED: Your license has been revoked by the administrator.\n\nContact Support: admin@itc.com", 
                                  icon="cancel")
                    sys.exit(0)
                
                if os.getenv("AGREEMENT_ACCEPTED") == "True":
                    parent.start_boot_handshake()
                else:
                    parent.show_eula_view()
            else:
                parent.show_auth_view(mode="login")
        except Exception as e:
            parent.log("ERROR", f"Routing Error: {e}")
            parent.show_auth_view(mode="login")

    @staticmethod
    def show_auth_view(parent, mode="login"):
        """Professional Authentication Screen Building (Redelegated from gui.py)"""
        # (This would contain the UI building logic previously in gui.py)
        # We can keep the UI building in gui.py for now OR move it to a dedicated AuthView.
        # Given the "Gravity" rules, a dedicated AuthView is better.
        pass

    @staticmethod
    def login(parent, email, password, username=""):
        """Bridges UI call to Database Manager logic and pulls cloud config"""
        if hasattr(parent, 'db_manager'):
            success, msg = parent.db_manager.login(email, password)
            if success:
                # CRITICAL: Pull User Config after successful login
                parent.db_manager.pull_user_config()
            return success, msg
        return False, "Database Manager Not Found"

    @staticmethod
    def create_account(parent, email, password, username):
        """Bridges UI call to Database Manager logic"""
        if hasattr(parent, 'db_manager'):
            return parent.db_manager.sign_up(email, password, username)
        return False, "Database Manager Not Found"

    @staticmethod
    def reset_password(parent, email):
        """Bridges UI call to Database Manager logic"""
        if hasattr(parent, 'db_manager'):
            return parent.db_manager.reset_password(email)
        return False, "Database Manager Not Found"

    @staticmethod
    def logout(parent):
        """Clean logout and restart"""
        confirm = CTkMessagebox(title=parent.translator.get("popup_logout_title"), 
                                message=parent.translator.get("popup_logout_msg"),
                                icon="question", 
                                option_1=parent.translator.get("popup_logout_yes"), 
                                option_2=parent.translator.get("popup_logout_no"))
        if confirm.get() == parent.translator.get("popup_logout_yes"):
            parent.db_manager.logout()
            import subprocess
            parent.destroy()
            subprocess.Popen([sys.executable] + sys.argv)

    @staticmethod
    def register(parent, email, password, username):
        """Alias for create_account"""
        return AuthService.create_account(parent, email, password, username)
