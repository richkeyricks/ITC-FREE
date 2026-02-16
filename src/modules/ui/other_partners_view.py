"""
Other Partners View
Displays Payment Gateways, Stock Platforms, Copy Trade, and Crypto Exchanges.
Following Gravity Rules: Modular, Separation of Concerns, LOCALIZATION.
"""

# --- IMPORTS ---
import webbrowser
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS

try:
    from constants.partner_data import PARTNER_CATEGORIES_ID, PARTNER_CATEGORIES_EN
except ImportError:
    PARTNER_CATEGORIES_ID = []
    PARTNER_CATEGORIES_EN = []

# --- CONSTANTS ---
CARD_PADDING = 15
SECTION_SPACING = 20

# --- CLASS ---
class OtherPartnersView:
    """
    Standalone View for Other Partners (Payment, Stocks, Crypto, etc).
    Now supports bilingual localization.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Other Partners interface."""
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        lang_code = parent.translator.lang_code if hasattr(parent, 'translator') else "EN"
        
        # Select category data based on language
        categories = PARTNER_CATEGORIES_ID if lang_code == "ID" else PARTNER_CATEGORIES_EN
        
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        # --- HEADER (Localized) ---
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", pady=(10, 5))
        
        header_text = "🤝 MITRA LAINNYA" if lang_code == "ID" else "🤝 OTHER PARTNERS"
        sub_text = "Mitra Afiliasi & Layanan Terpercaya" if lang_code == "ID" else "Trusted Affiliate Partners & Services"
        
        ctk.CTkLabel(header, text=header_text, font=("Segoe UI Bold", 26), 
                     text_color=theme["accent_primary"]).pack(side="top", anchor="center")
        ctk.CTkLabel(header, text=sub_text, font=("Segoe UI", 12),
                     text_color=theme["text_secondary"]).pack(side="top", anchor="center")

        # --- SCROLLABLE CONTENT ---
        content_area = ctk.CTkScrollableFrame(page, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=20, pady=10)
        
        # --- RENDER CATEGORIES ---
        for cat_icon, cat_name, cat_items in categories:
            OtherPartnersView._render_category(content_area, cat_icon, cat_name, cat_items, theme, lang_code)
        
        return page
    
    @staticmethod
    def _render_category(parent, icon: str, name: str, items: list, theme: dict, lang_code: str):
        """Renders a single category section with its items."""
        
        # Category Header
        cat_header = ctk.CTkFrame(parent, fg_color="transparent")
        cat_header.pack(fill="x", pady=(SECTION_SPACING, 8))
        
        ctk.CTkLabel(cat_header, text=f"{icon}  {name}", 
                     font=("Segoe UI Bold", 18), 
                     text_color=theme["accent_primary"]).pack(side="left")
        
        # Separator Line
        sep = ctk.CTkFrame(parent, fg_color=theme["border_default"], height=1)
        sep.pack(fill="x", pady=(0, 10))
        
        # Items Grid
        for item in items:
            OtherPartnersView._render_partner_card(parent, item, theme, lang_code)
    
    @staticmethod
    def _render_partner_card(parent, item: dict, theme: dict, lang_code: str):
        """Renders a single partner card with localized description."""
        
        is_featured = item.get("is_featured", False)
        
        # Get localized description
        desc_key = f"desc_{lang_code.lower()}"
        description = item.get(desc_key) or item.get("desc", "")
        
        # Card Container
        card = ctk.CTkFrame(parent, fg_color=theme["bg_secondary"], corner_radius=10, 
                          border_width=1, border_color=theme["border_default"])
        card.pack(fill="x", pady=6)
        
        # Hover Effect
        def on_enter(e, f=card): f.configure(fg_color=theme["bg_tertiary"])
        def on_leave(e, f=card): f.configure(fg_color=theme["bg_secondary"])
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Header Row
        h_frame = ctk.CTkFrame(card, fg_color="transparent")
        h_frame.pack(fill="x", padx=CARD_PADDING, pady=12)
        
        icon = item.get("icon", "🔗")
        nm_col = "#f59e0b" if is_featured else theme["text_primary"]
        
        # Title with Icon
        title_lbl = ctk.CTkLabel(h_frame, text=f"{icon}  {item['name']}", 
                               font=("Segoe UI Bold", 16), text_color=nm_col)
        title_lbl.pack(side="left")
        
        # Featured Badge (Localized)
        if is_featured:
            badge_text = "⭐ UNGGULAN" if lang_code == "ID" else "⭐ FEATURED"
            badge = ctk.CTkLabel(h_frame, text=badge_text, font=("Segoe UI Bold", 10),
                               text_color="#f59e0b", fg_color=theme["bg_tertiary"],
                               corner_radius=4, padx=6, pady=2)
            badge.pack(side="right")
        
        # Description
        desc = ctk.CTkLabel(card, text=description, font=("Segoe UI", 12), 
                          text_color=theme["text_secondary"], justify="left", anchor="w")
        desc.pack(fill="x", padx=CARD_PADDING, pady=(0, 10))
        
        # CTA Button (Localized)
        if is_featured:
            btn_txt = "BUKA AKUN 🚀" if lang_code == "ID" else "OPEN ACCOUNT 🚀"
        else:
            btn_txt = "KUNJUNGI" if lang_code == "ID" else "VISIT PARTNER"
        
        btn_col = "#f59e0b" if is_featured else theme["bg_tertiary"]
        text_col = "black" if is_featured else theme["text_primary"]
        
        ctk.CTkButton(card, text=btn_txt, fg_color=btn_col, 
                     hover_color="#d97706" if is_featured else theme["border_active"],
                     text_color=text_col, height=36, font=("Segoe UI Bold", 12),
                     command=lambda u=item['url']: webbrowser.open_new_tab(u)).pack(fill="x", padx=CARD_PADDING, pady=(0, CARD_PADDING))
