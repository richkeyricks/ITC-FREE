import os
import json
import time
from importlib.util import find_spec

class SecurityManager:
    """
    Handles Advanced Security Features (2FA, Encryption, etc.)
    Follows Gravity Dev Rules: Modular & Robust.
    """
    
    SECRETS_FILE = "secrets.json"
    
    @staticmethod
    def check_dependencies():
        """Checks if required security libs are installed"""
        missing = []
        if not find_spec("pyotp"): missing.append("pyotp")
        if not find_spec("qrcode"): missing.append("qrcode")
        return missing

    @staticmethod
    def install_dependencies(parent):
        """Auto-installs missing security libs"""
        import subprocess
        import sys
        
        missing = SecurityManager.check_dependencies()
        if not missing: return True
        
        parent.log("INFO", f"Installing Security Libs: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            return True
        except Exception as e:
            parent.log("ERROR", f"Failed to install security libs: {e}")
            return False

    @staticmethod
    def get_totp_secret():
        """Retrieves or Generates a persistent TOTP Secret for the Admin"""
        # Load existing
        if os.path.exists(SecurityManager.SECRETS_FILE):
            try:
                with open(SecurityManager.SECRETS_FILE, 'r') as f:
                    data = json.load(f)
                    if "admin_totp_secret" in data:
                        return data["admin_totp_secret"]
            except: pass
            
        # Generate NEW if missing
        try:
            import pyotp
            secret = pyotp.random_base32()
            
            # Save persistently
            data = {}
            if os.path.exists(SecurityManager.SECRETS_FILE):
                try:
                    with open(SecurityManager.SECRETS_FILE, 'r') as f:
                        data = json.load(f)
                except: pass
            
            data["admin_totp_secret"] = secret
            with open(SecurityManager.SECRETS_FILE, 'w') as f:
                json.dump(data, f, indent=4)
                
            return secret
        except ImportError:
            return None

    @staticmethod
    def generate_qr_code(secret, email):
        """Generates a QR Code image path for Google Authenticator"""
        try:
            import pyotp
            import qrcode
            
            # Create Provisioning URI (Standard for Google Auth)
            uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="ITC +AI Admin")
            
            # Create QR Image
            img = qrcode.make(uri)
            
            # Ensure assets dir exists
            assets_dir = os.path.join(os.getcwd(), "assets", "cache")
            os.makedirs(assets_dir, exist_ok=True)
            
            qr_path = os.path.join(assets_dir, "admin_2fa_qr.png")
            img.save(qr_path)
            return qr_path
        except Exception as e:
            print(f"// QR Gen Error: {e}")
            return None

    @staticmethod
    def verify_code(secret, code):
        """Verifies the 6-digit TOTP code"""
        try:
            import pyotp
            totp = pyotp.TOTP(secret)
            return totp.verify(code)
        except:
            return False
            
    @staticmethod
    def is_2fa_setup():
        """Checks if 2FA secret already exists on disk"""
        if os.path.exists(SecurityManager.SECRETS_FILE):
            try:
                with open(SecurityManager.SECRETS_FILE, 'r') as f:
                    data = json.load(f)
                    return "admin_totp_secret" in data
            except: pass
        return False
