import os
import threading
import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox

class AuthView:
    """
    Modular Auth Screen (Login/Signup).
    Follows Gravity Dev Rules: Modular UI.
    """
    
    @staticmethod
    def build(parent, mode="login"):
        """Builds the Auth interface inside the parent window"""
        parent.clear_window()
        parent.title(parent.translator.get("auth_title"))
        
        # Determine theme dynamically
        from ui_theme import THEME_DARK
        if hasattr(parent, 'get_theme_data'):
            theme = parent.get_theme_data()
        elif hasattr(parent, 'theme_data'):
            theme = parent.theme_data
        else:
            theme = THEME_DARK
            
        THEME = theme # Use the determined theme
        
        # Main Background (Dark)
        bg = ctk.CTkFrame(parent, fg_color=THEME["bg_primary"])
        bg.pack(fill="both", expand=True)
        
        # Center Card - Auto adjust height based on mode
        card_width = 500 
        card_height = 840 if mode == "signup" else 750
        card = ctk.CTkFrame(bg, fg_color=THEME["bg_secondary"], width=card_width, height=card_height, corner_radius=20)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        # --- TOP BANNER IMAGE ---
        try:
            from utils.path_helper import resource_path
            banner_path = resource_path("assets/banner.png")
            
            if os.path.exists(banner_path):
                pil_img = Image.open(banner_path)
                ctk_banner = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(500, 160))
                banner_lbl = ctk.CTkLabel(card, text="", image=ctk_banner)
                banner_lbl.pack(side="top", fill="x")
        except Exception as e:
            parent.log("ERROR", f"Failed to load auth banner: {e}")
            ctk.CTkLabel(card, text="ITC +AI", font=("Arial Black", 40), text_color="#1f6feb").pack(pady=(40, 10))

        # --- FORM AREA ---
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        head_text = parent.translator.get("auth_header_login") if mode == "login" else parent.translator.get("auth_header_signup")
        sub_text = parent.translator.get("auth_desc_login") if mode == "login" else parent.translator.get("auth_desc_signup")
        
        ctk.CTkLabel(form_frame, text=head_text, font=("Segoe UI Bold", 26), 
                     text_color=THEME["text_primary"] if "text_primary" in THEME else "white").pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(form_frame, text=sub_text, font=("Segoe UI", 13), 
                     text_color=THEME["text_secondary"]).pack(anchor="w", pady=(0, 15))
        
        # --- PRIMARY GOOGLE ACTION (FAST TRACK) ---
        google_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        google_container.pack(fill="x", pady=(10, 20))
        
        def _google_login():
            from modules.logic.oauth_handler import OAuthHandler
            OAuthHandler.initiate_google_login(parent)

        google_text_key = "auth_google" if mode == "login" else "auth_google_signup"
        google_text = parent.translator.get(google_text_key)
        
        # Professional Google Button
        google_btn = ctk.CTkButton(google_container, 
                                 text=google_text, 
                                 font=("Segoe UI Bold", 16), 
                                 fg_color="#FFFFFF", border_width=1, border_color="#747775",
                                 text_color="#1f1f1f", height=55, corner_radius=12,
                                 command=_google_login)
        google_btn.pack(fill="x")
        
        # Subtle Divider
        divider_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        divider_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(divider_frame, text=f"────────  {parent.translator.get('auth_or')}  ────────", font=("Segoe UI", 10), text_color=THEME["text_secondary"]).pack()

        # --- HIDDEN MANUAL SECTION ---
        manual_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        # manual_frame is NOT packed by default unless mode is signup
        
        def toggle_manual():
            if manual_frame.winfo_ismapped():
                manual_frame.pack_forget()
                btn_toggle.configure(text=parent.translator.get("auth_signin_password"))
            else:
                manual_frame.pack(fill="x", before=divider)
                btn_toggle.configure(text=parent.translator.get("auth_hide_manual"))

        btn_toggle = ctk.CTkButton(form_frame, text=parent.translator.get("auth_signin_password"), font=("Segoe UI Semibold", 12),
                                 fg_color="transparent", text_color=THEME.get("accent_primary", "#0d6efd"),
                                 hover_color=THEME["bg_tertiary"], height=30, command=toggle_manual)
        if mode == "login":
            btn_toggle.pack(pady=(5, 15))
        else:
            manual_frame.pack(fill="x", before=divider)

        # Inputs (Moved into manual_frame)
        parent.lbl_user = ctk.CTkLabel(manual_frame, text=parent.translator.get("auth_user"), font=("Segoe UI Semibold", 13), 
                     text_color=THEME["text_secondary"])
        parent.auth_user = ctk.CTkEntry(manual_frame, height=50, placeholder_text=parent.translator.get("auth_user").replace(":", ""),
                                     fg_color=THEME["bg_tertiary"], border_width=1, border_color=THEME["bg_tertiary"],
                                     font=("Segoe UI", 14), corner_radius=10)
        
        if mode == "signup":
            parent.lbl_user.pack(anchor="w", pady=(0, 5))
            parent.auth_user.pack(fill="x", pady=(0, 15))
            
        ctk.CTkLabel(manual_frame, text=parent.translator.get("auth_email"), font=("Segoe UI Semibold", 13), 
                     text_color=THEME["text_secondary"]).pack(anchor="w", pady=(0, 5))
        
        parent.auth_email = ctk.CTkEntry(manual_frame, height=50, placeholder_text="name@example.com",
                                     fg_color=THEME["bg_tertiary"], border_width=1, border_color=THEME["bg_tertiary"],
                                     font=("Segoe UI", 14), corner_radius=10)
        parent.auth_email.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(manual_frame, text=parent.translator.get("auth_pass"), font=("Segoe UI Semibold", 13),
                                     text_color=THEME["text_secondary"]).pack(anchor="w", pady=(0, 5))
                                     
        parent.auth_pass = ctk.CTkEntry(manual_frame, height=50, show="*", placeholder_text=parent.translator.get("auth_pass").replace(":", ""),
                                    fg_color=THEME["bg_tertiary"], border_width=1, border_color=THEME["bg_tertiary"],
                                    font=("Segoe UI", 14), corner_radius=10)
        parent.auth_pass.pack(fill="x", pady=(0, 20))
        
        btn_desc = parent.translator.get("auth_login") if mode == "login" else parent.translator.get("auth_signup")

        def on_auth():
            email = parent.auth_email.get().strip()
            password = parent.auth_pass.get().strip()
            username = parent.auth_user.get().strip() if mode == "signup" else None
            
            if not email or not password:
                CTkMessagebox(title="Warning", message="Please fill all fields.", icon="warning")
                return

            if mode == "signup" and not username:
                CTkMessagebox(title="Warning", message="Username is required.", icon="warning")
                return
            
            # Disable input while processing
            btn_submit.configure(state="disabled", text="Processing...")
            
            # --- NON-BLOCKING AUTH THREAD ---
            def _auth_task():
                try:
                    from modules.logic.auth_service import AuthService
                    success, msg = False, ""
                    
                    if mode == "login":
                        success, msg = AuthService.login(parent, email, password)
                    else:
                        success, msg = AuthService.register(parent, email, password, username)
                    
                    # Back to main thread for UI
                    if success:
                        def _on_auth_success():
                            parent.log("SUCCESS", f"Auth Success: {msg}")
                            # CHECK FOR ADMIN 2FA
                            if os.getenv("IS_ADMIN") == "True":
                                AuthView.start_2fa_flow(parent)
                            else:
                                parent.start_boot_handshake()
                        
                        parent.after(0, _on_auth_success)
                    else:
                        # Clean error message
                        final_msg = msg.replace("Error: ", "").capitalize()
                        if "invalid login credentials" in final_msg.lower():
                            final_msg = "Email atau Password salah!"
                        elif "user already registered" in final_msg.lower():
                            final_msg = "Email sudah terdaftar. Silakan login."
                            
                        # Show error -> Context Aware Title
                        def _finish_auth_error():
                            btn_submit.configure(state="normal", text=btn_desc)
                            
                            err_title = parent.translator.get("auth_header_login") if mode == "login" else parent.translator.get("auth_header_signup")
                            err_title = err_title.replace("Buat", "Gagal").replace("Masuk", "Gagal")
                            
                            # Fallback if translation missing
                            if not err_title: err_title = "Authentication Failed"
                            
                            CTkMessagebox(title=err_title, message=final_msg, icon="cancel")
                        
                        parent.after(0, _finish_auth_error)
                        
                except Exception as e:
                    err_msg = str(e)
                    def _handle_error():
                        btn_submit.configure(state="normal", text=btn_desc)
                        CTkMessagebox(title="System Error", message=f"Authentication failed: {err_msg}", icon="cancel")
                    
                    parent.after(0, _handle_error)
                    parent.log("ERROR", f"Auth Task Exception: {e}")

            threading.Thread(target=_auth_task, daemon=True).start()

        # Primary Action Button (Moved inside manual_frame)
        btn_submit = ctk.CTkButton(manual_frame, text=btn_desc, font=("Segoe UI Bold", 15), 
                      fg_color=THEME.get("btn_primary_bg", "#0d6efd"), 
                      hover_color=THEME.get("btn_primary_hover", "#0b5ed7"),
                      text_color="white",
                      command=on_auth, height=50, corner_radius=10)
        btn_submit.pack(fill="x", pady=(0, 10))
        
        # --- ENTER KEY BINDINGS ---
        parent.auth_email.bind("<Return>", lambda e: on_auth())
        parent.auth_pass.bind("<Return>", lambda e: on_auth())
        if mode == "signup":
            parent.auth_user.bind("<Return>", lambda e: on_auth())
        
        
        # Forgot Password Link (Only in Login Mode)
        if mode == "login":
            def _forgot_pass():
                from modules.logic.auth_service import AuthService
                email = parent.auth_email.get()
                if not email:
                    CTkMessagebox(title="Error", message="Please enter your email address first.", icon="warning")
                    return
                
                # Logic
                success, msg = AuthService.reset_password(parent, email)
                icon = "check" if success else "cancel"
                CTkMessagebox(title="Password Reset", message=msg, icon=icon)

            forgot_btn = ctk.CTkButton(form_frame, text=parent.translator.get("auth_forgot_pass"), 
                                     font=("Segoe UI", 12), 
                                     fg_color="transparent", 
                                     text_color=THEME["text_secondary"],
                                     hover_color=THEME["bg_tertiary"],
                                     height=20,
                                     command=_forgot_pass)
            forgot_btn.pack(pady=(0, 15))

        divider = ctk.CTkFrame(form_frame, height=2, fg_color=THEME["bg_tertiary"])
        divider.pack(fill="x", pady=(0, 20))
        
        footer_pre = parent.translator.get("auth_no_account") if mode == "login" else parent.translator.get("auth_have_account")
        footer_link = parent.translator.get("auth_signup_now") if mode == "login" else parent.translator.get("auth_login_here")
        
        foot_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        foot_frame.pack()
        
        ctk.CTkLabel(foot_frame, text=footer_pre, font=("Segoe UI", 13), 
                     text_color=THEME["text_secondary"]).pack(side="left")
                     
        ctk.CTkButton(foot_frame, text=footer_link, font=("Segoe UI Bold", 13), 
                      fg_color="transparent", text_color=THEME.get("accent_primary", "#0d6efd"), hover_color=THEME["bg_tertiary"], 
                      width=60,
                      command=lambda: AuthView.build(parent, "signup" if mode == "login" else "login")).pack(side="left")

        # --- LANGUAGE TOGGLE (Floating Badge) ---
        lang_toggle_frame = ctk.CTkFrame(card, fg_color="transparent")
        lang_toggle_frame.place(relx=0.95, rely=0.05, anchor="ne")
        
        current_lang = parent.translator.lang_code
        toggle_text = "🇺🇸 EN" if current_lang == "ID" else "🇮🇩 ID"
        
        def _switch_lang():
            new_lang = "EN" if current_lang == "ID" else "ID"
            parent._set_lang_action(new_lang)
            # Re-building is handled by _set_lang_action -> check_initial_auth
            
        ctk.CTkButton(lang_toggle_frame, text=toggle_text, width=60, height=28, 
                      fg_color="#1A1B22", border_width=1, border_color="#333",
                      hover_color="#333", font=("Segoe UI Bold", 10),
                      command=_switch_lang).pack()

    @staticmethod
    def start_2fa_flow(parent):
        """Initiates the Google Authenticator Challenge"""
        from modules.logic.security_manager import SecurityManager
        from modules.ui.two_factor_view import TwoFactorView
        
        # 1. Dependency Check
        missing = SecurityManager.check_dependencies()
        if missing:
            confirm = CTkMessagebox(title="Security Update", 
                                    message="Admin Login requires 'Google Authenticator' support.\n\nInstall required components now?",
                                    icon="question", option_1="Install", option_2="Cancel")
            if confirm.get() == "Install":
                if not SecurityManager.install_dependencies(parent):
                    CTkMessagebox(title="Error", message="Installation failed. Check internet connection.", icon="cancel")
                    return
            else:
                return

        # 2. Determine State (Setup vs Verify)
        secret = SecurityManager.get_totp_secret()
        mode = "setup" if not SecurityManager.is_2fa_setup() else "verify"
        qr_path = None
        
        if mode == "setup":
             # We need user email for the QR Code label
             import os
             email = os.getenv("USER_EMAIL", "admin@gravity")
             qr_path = SecurityManager.generate_qr_code(secret, email)
        
        # 3. Define Callback for Success
        def on_2fa_success(code, window):
            if SecurityManager.verify_code(secret, code):
                window.destroy()
                parent.log("SUCCESS", "2FA Verification Passed")
                parent.start_boot_handshake()
            else:
                CTkMessagebox(title="Access Denied", message="Invalid Authenticator Code!", icon="cancel")

        # 4. Launch Dialog
        TwoFactorView(parent, mode=mode, secret=secret, qr_path=qr_path, callback=on_2fa_success)
