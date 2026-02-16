import os
import customtkinter as ctk
from dotenv import set_key
from legal import EULA_TEXT

class EULAView:
    """
    Modular EULA Agreement Screen.
    Follows Gravity Dev Rules: Modular UI.
    """
    
    @staticmethod
    def build(parent):
        """Builds the EULA interface inside the parent window"""
        parent.clear_window()
        parent.title(parent.translator.get("eula_title"))
        
        from ui_theme import THEME_DARK, FONTS as LEGACY_FONTS
        from ui_theme_modern import get_theme as get_modern_theme, FONTS as MODERN_FONTS
        
        if hasattr(parent, 'get_theme_data'):
            theme = parent.get_theme_data()
            fonts = MODERN_FONTS if parent.selected_theme in ["light", "neutral"] else LEGACY_FONTS
        else:
            theme = THEME_DARK
            fonts = LEGACY_FONTS
            
        THEME = theme
        
        # Center container
        container = ctk.CTkFrame(parent, fg_color=THEME["bg_secondary"], corner_radius=16, width=700, height=650)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header
        ctk.CTkLabel(container, text=parent.translator.get("eula_header"), font=("Segoe UI Bold", 20), 
                     text_color="#ff813f").pack(pady=20)
        
        # Scrollable EULA Text
        text_box = ctk.CTkTextbox(container, width=650, height=400, font=("Consolas", 12),
                                  fg_color=THEME["bg_tertiary"], text_color=THEME.get("text_primary", "white"))
        text_box.pack(padx=25, pady=5)
        text_box.insert("0.0", EULA_TEXT)
        text_box.configure(state="disabled")
        
        # Checkbox Logic
        parent.agree_var = ctk.BooleanVar(value=False)
        def toggle_btn():
            if parent.agree_var.get():
                btn_proceed.configure(state="normal", fg_color=THEME["accent_success"])
            else:
                btn_proceed.configure(state="disabled", fg_color="grey")
                
        check = ctk.CTkCheckBox(container, text=parent.translator.get("eula_checkbox"),
                                variable=parent.agree_var, command=toggle_btn, font=fonts["body_small"],
                                fg_color=THEME.get("accent_primary"))
        check.pack(pady=15)
        
        def on_accept():
            set_key(".env", "AGREEMENT_ACCEPTED", "True")
            os.environ["AGREEMENT_ACCEPTED"] = "True"
            parent.show_main_interface()
            parent.log("INFO", "⚖️ EULA Accepted. All systems active.")
            
        btn_proceed = ctk.CTkButton(container, text=parent.translator.get("eula_accept"), state="disabled", fg_color="grey",
                                   command=on_accept, height=45, font=fonts.get("button_large", ("Segoe UI Bold", 14)))
        btn_proceed.pack(pady=(0, 20), fill="x", padx=100)
