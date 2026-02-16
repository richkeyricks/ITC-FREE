import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS

# --- THEME ---
# REMOVED STATIC THEME

class UIHelpers:
    """
    Utility class for shared UI components and patterns.
    Follows Gravity Dev Rules: DRY & Modular.
    """

    @staticmethod
    def create_field(container, label, value, theme, placeholder="", is_password=False, label_width=160):
        """Creates a standard label + entry field row with consistent alignment."""
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(row, text=label, font=FONTS["body"], width=label_width, anchor="w",
                     text_color=theme["text_secondary"]).pack(side="left")
        
        entry = ctk.CTkEntry(row, height=36, placeholder_text=placeholder, 
                             fg_color=theme["bg_tertiary"], border_color=theme["border_default"],
                             show="*" if is_password else "")
        entry.insert(0, str(value or ""))
        entry.pack(side="left", fill="x", expand=True)
        return entry

    @staticmethod
    def create_field_compact(container, label, value, theme):
        """Creates a compact label + entry field row for multi-column layouts."""
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row, text=label, font=FONTS["body"], width=100, anchor="w",
                     text_color=theme["text_secondary"]).pack(side="left")
        
        entry = ctk.CTkEntry(row, height=32, fg_color=theme["bg_tertiary"], 
                             border_color=theme["border_default"])
        entry.insert(0, str(value or ""))
        entry.pack(side="left", fill="x", expand=True)
        return entry

    @staticmethod
    def create_status_card(container, icon, title, status, theme):
        """Creates a glassmorphic status card with border glow."""
        card = ctk.CTkFrame(container, fg_color=theme["card_bg"], corner_radius=12, height=75,
                            border_width=1, border_color=theme["card_border"])
        card.pack(side="left", expand=True, fill="both", padx=(0, 12))
        card.pack_propagate(False)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(expand=True, padx=18)
        
        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack()
        
        icon_frame = ctk.CTkFrame(row, fg_color=theme["accent_primary"], corner_radius=10,
                                   width=44, height=44)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text=icon, font=("Segoe UI", 20), text_color="#fff").pack(expand=True)
        
        text_frame = ctk.CTkFrame(row, fg_color="transparent")
        text_frame.pack(side="left")
        
        ctk.CTkLabel(text_frame, text=title, font=FONTS["body_bold"], text_color=theme["text_primary"], anchor="w").pack(anchor="w")
        lbl_status = ctk.CTkLabel(text_frame, text=f"● {status}", font=FONTS["body_small"], 
                                   text_color="#f85149", anchor="w")
        lbl_status.pack(anchor="w")
        
        return lbl_status

    @staticmethod
    def create_value_card(container, icon, label, value, theme, color=None):
        """Creates a glassmorphic value card with premium styling."""
        card = ctk.CTkFrame(container, fg_color=theme["card_bg"], corner_radius=12, height=75,
                            border_width=1, border_color=theme["card_border"])
        card.pack(side="left", expand=True, fill="both", padx=(0, 12))
        card.pack_propagate(False)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(expand=True, padx=18)
        
        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack()
        
        icon_bg = theme["accent_secondary"] if "P/L" in label else theme["accent_primary"]
        icon_lbl = ctk.CTkLabel(row, text=icon, font=("Segoe UI", 16), width=44, height=44,
                                 fg_color=icon_bg, corner_radius=22, text_color="#fff")
        icon_lbl.pack(side="left", padx=(0, 12))
        
        text_frame = ctk.CTkFrame(row, fg_color="transparent")
        text_frame.pack(side="left")
        
        ctk.CTkLabel(text_frame, text=label, font=FONTS["body_small"], 
                     text_color=theme["text_secondary"], anchor="w").pack(anchor="w")
        lbl_value = ctk.CTkLabel(text_frame, text=value, font=("Segoe UI Semibold", 20), 
                                  text_color=color or theme["text_primary"], anchor="w")
        lbl_value.pack(anchor="w")
        
        return lbl_value
