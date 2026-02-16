import customtkinter as ctk
import os
import webbrowser
from CTkMessagebox import CTkMessagebox
from ui_theme import THEME_DARK

class StartupView:
    """
    Modular Startup & Setup Screens.
    Follows Gravity Dev Rules: Modular UI.
    """

    @staticmethod
    def show_language_view(parent):
        """First Run: Language Selection Screen"""
        parent.clear_window()
        theme = THEME_DARK
        
        # Center Frame
        center = ctk.CTkFrame(parent, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Icon
        ctk.CTkLabel(center, text="🌍", font=("Segoe UI", 60)).pack(pady=(0, 20))
        
        ctk.CTkLabel(center, text="WELCOME / SELAMAT DATANG", 
                     font=("Segoe UI Bold", 24), text_color="white").pack(pady=(0, 10))
        ctk.CTkLabel(center, text="Please select your preferred language\nSilakan pilih bahasa yang Anda inginkan", 
                     font=("Segoe UI", 14), text_color=theme["text_secondary"]).pack(pady=(0, 30))
        
        btns = ctk.CTkFrame(center, fg_color="transparent")
        btns.pack()
        
        # ID Button
        btn_id = ctk.CTkButton(btns, text="INDONESIA 🇮🇩", font=("Segoe UI Bold", 16),
                             width=180, height=60, fg_color=theme["bg_secondary"],
                             border_width=2, border_color=theme["accent_primary"],
                             hover_color=theme["bg_tertiary"],
                             command=lambda: parent._set_lang_action("ID"))
        btn_id.pack(side="left", padx=15)
        
        # EN Button
        btn_en = ctk.CTkButton(btns, text="ENGLISH 🇺🇸", font=("Segoe UI Bold", 16),
                             width=180, height=60, fg_color=theme["bg_secondary"],
                             border_width=2, border_color="#27ae60",
                             hover_color=theme["bg_tertiary"],
                             command=lambda: parent._set_lang_action("EN"))
        btn_en.pack(side="left", padx=15)

    @staticmethod
    def show_update_prompt(parent, msg, metadata, app_version):
        """Displays update notification"""
        confirm = CTkMessagebox(title=parent.translator.get("popup_update_title"), 
                               message=msg,
                               icon="info", 
                               option_1=parent.translator.get("popup_update_btn1"), 
                               option_2=parent.translator.get("popup_update_btn2"))
        
        if confirm.get() == parent.translator.get("popup_update_btn1"):
            url = metadata.get("download_url", "https://github.com/richkeyricks/ITC-FREE") if metadata else "https://github.com/richkeyricks/ITC-FREE"
            webbrowser.open(url)
