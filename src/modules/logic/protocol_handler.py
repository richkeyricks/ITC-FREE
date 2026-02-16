import winreg
import sys
import os

class ProtocolManager:
    """
    Handles registration and management of custom Windows URI schemes (itc-app://)
    Follows Gravity Rule: Professional Infrastructure.
    """
    PROTOCOL = "itc-app"
    
    @staticmethod
    def register():
        """Registers the itc-app protocol in the Windows Registry"""
        if sys.platform != "win32":
            return False
            
        try:
            # Path to the current executable or python script
            app_path = sys.executable
            script_path = os.path.abspath(sys.argv[0])
            
            # Command to run when protocol is triggered
            # Format: "C:\path\to\python.exe" "C:\path\to\gui.py" "%1"
            command = f'"{app_path}" "{script_path}" "%1"'
            
            # Create Registry Keys
            key_path = rf"Software\Classes\{ProtocolManager.PROTOCOL}"
            
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, f"URL:{ProtocolManager.PROTOCOL} Protocol")
                winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
                
                with winreg.CreateKey(key, r"DefaultIcon") as icon_key:
                    winreg.SetValue(icon_key, "", winreg.REG_SZ, f"{app_path},0")
                    
                with winreg.CreateKey(key, r"shell\open\command") as cmd_key:
                    winreg.SetValue(cmd_key, "", winreg.REG_SZ, command)
            
            return True
        except Exception as e:
            print(f"// Protocol Registration Error: {e}")
            return False

    @staticmethod
    def handle_args(args):
        """Parses command line arguments for deep link data"""
        for arg in args:
            if arg.startswith(f"{ProtocolManager.PROTOCOL}://"):
                try:
                    # structure: itc-app://auth?code=...  OR  itc-app://auth?access_token=...&refresh_token=...
                    from urllib.parse import urlparse, parse_qs
                    parsed = urlparse(arg)
                    params = parse_qs(parsed.query)
                    
                    token_data = {
                        "code": params.get("code", [None])[0],  # PKCE flow
                        "access_token": params.get("access_token", [None])[0],  # Implicit flow
                        "refresh_token": params.get("refresh_token", [None])[0],
                        "invite": params.get("invite", [None])[0] # Stealth Referral
                    }
                    return token_data
                except Exception as e:
                    print(f"// Deep Link Parse Error: {e}")
        return None
