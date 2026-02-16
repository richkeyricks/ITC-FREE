import os
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS
from utils.tooltips import CTkToolTip

# --- THEME ---
# REMOVED STATIC THEME

class MT5View:
    """
    Modular class for the MT5 Settings page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the MT5 page and attaches it to the parent (App/GUI)."""
        # Dynamic Theme Loading
        theme = parent.theme_data if hasattr(parent, 'theme_data') else THEME_DARK
        
        page = ctk.CTkScrollableFrame(parent.main_container, fg_color="transparent")
        
        # Title with status
        title_row = ctk.CTkFrame(page, fg_color="transparent")
        title_row.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(title_row, text=parent.translator.get("mt5_title"), font=("Segoe UI Semibold", 22), 
                     text_color=theme["text_primary"]).pack(side="left")
        
        parent.mt5_status = ctk.CTkLabel(title_row, text=f"● {parent.translator.get('status_not_logged')}", font=FONTS["body_small"],
                                        text_color="#f85149")
        parent.mt5_status.pack(side="right")
        
        card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        card.pack(fill="x")
        
        parent.entry_mt5_login = MT5View._create_field(parent, card, "Login ID", os.getenv("MT5_LOGIN", ""), theme)
        CTkToolTip(parent.entry_mt5_login, parent.translator.get("hint_mt5_login"))
        
        parent.entry_mt5_pass = MT5View._create_field(parent, card, "Password", os.getenv("MT5_PASSWORD", ""), theme, show="*")
        CTkToolTip(parent.entry_mt5_pass, parent.translator.get("hint_mt5_pass"))
        
        parent.entry_mt5_server = MT5View._create_field(parent, card, "Server", os.getenv("MT5_SERVER", ""), theme)
        CTkToolTip(parent.entry_mt5_server, parent.translator.get("hint_mt5_server"))
        
        # Show password checkbox
        parent.show_pass = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(card, text=parent.translator.get("mt5_show_pass"), variable=parent.show_pass, font=FONTS["body_small"],
                        text_color=theme["text_primary"],
                        command=parent.toggle_password).pack(anchor="w", padx=20, pady=(0, 10))
        
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkButton(btn_row, text=parent.translator.get("config_save"), font=FONTS["button"],
                      fg_color=theme["accent_success"], height=40, text_color="white",
                      command=parent.save_config).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(btn_row, text=parent.translator.get("mt5_test"), font=FONTS["button"],
                      fg_color=theme["accent_primary"], height=40, text_color="white",
                      command=parent.test_mt5).pack(side="left")
        
        parent.btn_test_mt5 = list(btn_row.winfo_children())[-1]
        CTkToolTip(parent.btn_test_mt5, parent.translator.get("hint_mt5_test"))
        
        # Contextual Tutorial Card
        from modules.ui.ui_components import ContextualTutorialCard
        tut_card = ContextualTutorialCard(
            page, 
            title=parent.translator.get("tut_card_mt5_title"),
            steps_text=parent.translator.get("tut_card_mt5_steps"),
            height=180
        )
        tut_card.pack(fill="x", pady=(20, 10))
        
        return page

    @staticmethod
    def _create_field(parent, container, label, initial, theme, placeholder="", show=""):
        """Helper to create a labeled input field."""
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=8)
        
        ctk.CTkLabel(row, text=label, font=FONTS["body"], width=120, anchor="w",
                     text_color=theme["text_secondary"]).pack(side="left")
        
        entry = ctk.CTkEntry(row, height=36, fg_color=theme["bg_tertiary"],
                              border_color=theme["border_default"], corner_radius=6,
                              text_color=theme["text_primary"],
                              placeholder_text=placeholder, show=show)
        entry.insert(0, initial)
        entry.pack(side="left", fill="x", expand=True)
        return entry
