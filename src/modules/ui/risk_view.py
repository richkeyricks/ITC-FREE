import os
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS
from utils.tooltips import CTkToolTip
from modules.ui.ui_helpers import UIHelpers

# --- THEME ---
# --- THEME ---
# REMOVED STATIC THEME

class RiskView:
    """
    Modular class for the Risk Management page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Risk page and attaches it to the parent (App/GUI)."""
        # Dynamic Theme Loading
        theme = parent.theme_data if hasattr(parent, 'theme_data') else THEME_DARK
        
        page = ctk.CTkScrollableFrame(parent.main_container, fg_color="transparent")
        
        ctk.CTkLabel(page, text=parent.translator.get("risk_title"), font=("Segoe UI Semibold", 22), 
                     text_color=theme["text_primary"], anchor="w").pack(fill="x", pady=(0, 15))
        
        # Daily Loss Card
        loss_card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        loss_card.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(loss_card, text=parent.translator.get("risk_protection"), font=FONTS["section_header"],
                     text_color=theme["text_primary"]).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(loss_card, text=parent.translator.get("risk_loss_desc"),
                     font=FONTS["body_small"], text_color=theme["text_disabled"]).pack(anchor="w", padx=20)
        
        parent.entry_loss_limit = UIHelpers.create_field(loss_card, "Max Daily Loss %", os.getenv("DAILY_LOSS_LIMIT", "5.0"), theme)
        CTkToolTip(parent.entry_loss_limit, parent.translator.get("hint_risk_limit"))
        
        # Time Filter Card
        time_card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        time_card.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(time_card, text=parent.translator.get("risk_time"), font=FONTS["section_header"],
                     text_color=theme["text_primary"]).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(time_card, text=parent.translator.get("risk_time_desc"),
                     font=FONTS["body_small"], text_color=theme["text_disabled"]).pack(anchor="w", padx=20)
        
        time_row = ctk.CTkFrame(time_card, fg_color="transparent")
        time_row.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(time_row, text="Start:", font=FONTS["body"], width=50, text_color=theme["text_primary"]).pack(side="left")
        parent.entry_start = ctk.CTkEntry(time_row, width=60, height=36, fg_color=theme["bg_tertiary"], text_color=theme["text_primary"])
        parent.entry_start.insert(0, os.getenv("TRADE_START_HOUR", "0"))
        parent.entry_start.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(time_row, text="End:", font=FONTS["body"], width=50, text_color=theme["text_primary"]).pack(side="left")
        parent.entry_end = ctk.CTkEntry(time_row, width=60, height=36, fg_color=theme["bg_tertiary"], text_color=theme["text_primary"])
        parent.entry_end.insert(0, os.getenv("TRADE_END_HOUR", "24"))
        parent.entry_end.pack(side="left")
        
        # Save button
        ctk.CTkButton(page, text=parent.translator.get("settings_save"), font=FONTS["button"],
                      fg_color=theme["accent_success"], height=40, text_color="white",
                      command=parent.save_config).pack(fill="x", pady=15)
        
        return page
