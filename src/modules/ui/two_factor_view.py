import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image

class TwoFactorView:
    """
    UI Dialog for Google Authenticator 2FA.
    """
    
    def __init__(self, parent, mode="verify", secret=None, qr_path=None, callback=None):
        self.parent = parent
        self.mode = mode
        self.secret = secret
        self.qr_path = qr_path
        self.callback = callback
        
        # Create TopLevel Window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Admin Security Challenge")
        self.window.geometry("400x550")
        self.window.resizable(False, False)
        
        # Center the window
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 275
        self.window.geometry(f"+{x}+{y}")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Header
        ctk.CTkLabel(self.window, text="🔒 GOD MODE ACCESS", 
                     font=("Segoe UI Bold", 20), text_color="#dc3545").pack(pady=(20, 5))
        
        ctk.CTkLabel(self.window, text="Two-Factor Authentication Required", 
                     font=("Segoe UI", 12), text_color="gray").pack()
        
        # 2. Content Area (Dynamic)
        content_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        if self.mode == "setup":
            self.build_setup_ui(content_frame)
        else:
            self.build_verify_ui(content_frame)
            
    def build_setup_ui(self, frame):
        """Shows QR Code for First Time Setup"""
        ctk.CTkLabel(frame, text="1. Install Google Authenticator\n2. Scan this QR Code", 
                     font=("Segoe UI", 14), justify="center").pack(pady=(0, 20))
        
        # Show QR Image
        if self.qr_path:
            try:
                pil_img = Image.open(self.qr_path)
                qr_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(200, 200))
                ctk.CTkLabel(frame, text="", image=qr_img).pack(pady=10)
            except:
                ctk.CTkLabel(frame, text="[QR IMAGE ERROR]", text_color="red").pack(pady=50)
                
        ctk.CTkLabel(frame, text=f"Secret Key: {self.secret}", 
                     font=("Consolas", 10), text_color="gray").pack(pady=5)
                     
        ctk.CTkLabel(frame, text="3. Enter the 6-digit code below:", 
                     font=("Segoe UI", 12)).pack(pady=(15, 5))
                     
        self.code_entry = ctk.CTkEntry(frame, placeholder_text="000 000", justify="center",
                                       font=("Segoe UI Bold", 18), width=150)
        self.code_entry.pack(pady=5)
        
        ctk.CTkButton(frame, text="VERIFY & ENABLE", fg_color="#198754", hover_color="#157347",
                      command=self.on_submit).pack(pady=20, fill="x")

    def build_verify_ui(self, frame):
        """Simple Input for Login Verification"""
        ctk.CTkLabel(frame, text="Enter the 6-digit code from your\nAuthenticator App", 
                     font=("Segoe UI", 14), justify="center").pack(pady=(40, 30))
                     
        self.code_entry = ctk.CTkEntry(frame, placeholder_text="000 000", justify="center",
                                       font=("Segoe UI Bold", 24), height=50)
        self.code_entry.pack(pady=20, fill="x")
        
        self.code_entry.bind("<Return>", lambda e: self.on_submit())
        
        ctk.CTkButton(frame, text="UNLOCK DASHBOARD", height=45, font=("Segoe UI Bold", 14),
                      command=self.on_submit).pack(pady=20, fill="x")
                      
    def on_submit(self):
        code = self.code_entry.get().replace(" ", "").strip()
        if len(code) != 6 or not code.isdigit():
            CTkMessagebox(title="Invalid Code", message="Please enter a valid 6-digit code.", icon="warning")
            return
            
        if self.callback:
            self.callback(code, self.window)

