import os
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS
from utils.tooltips import CTkToolTip

# --- THEME ---
# REMOVED STATIC THEME

class TelegramView:
    """
    Modular class for the Telegram Settings page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Telegram page and attaches it to the parent (App/GUI)."""
        # Dynamic Theme Loading
        theme = parent.theme_data if hasattr(parent, 'theme_data') else THEME_DARK
        
        page = ctk.CTkScrollableFrame(parent.main_container, fg_color="transparent")
        
        # Title with status
        title_row = ctk.CTkFrame(page, fg_color="transparent")
        title_row.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(title_row, text=parent.translator.get("tg_title"), font=("Segoe UI Semibold", 22), 
                     text_color=theme["text_primary"]).pack(side="left")
        
        parent.tg_status = ctk.CTkLabel(title_row, text=f"● {parent.translator.get('status_disconnected')}", font=FONTS["body_small"],
                                       text_color="#f85149")
        parent.tg_status.pack(side="right")
        
        card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        card.pack(fill="x")
        
        # Info text
        ctk.CTkLabel(card, text=parent.translator.get("tg_get_api"), font=FONTS["body_small"],
                     text_color=theme["text_disabled"]).pack(anchor="w", padx=20, pady=(15, 5))
        
        parent.entry_api_id = TelegramView._create_field(parent, card, "API ID", os.getenv("TG_API_ID", ""), theme)
        CTkToolTip(parent.entry_api_id, parent.translator.get("hint_tg_id"))
        
        parent.entry_api_hash = TelegramView._create_field(parent, card, "API Hash", os.getenv("TG_API_HASH", ""), theme)
        CTkToolTip(parent.entry_api_hash, parent.translator.get("hint_tg_hash"))
        
        # Phone Number for Telegram Login (OTP flow)
        parent.entry_phone = TelegramView._create_field(parent, card, "Phone Number", os.getenv("USER_PHONE", ""), theme, "+628xxx...")
        CTkToolTip(parent.entry_phone, "Nomor HP Telegram Anda untuk login OTP. Contoh: +6281234567890")
        
        parent.entry_channels = TelegramView._create_field(parent, card, "Channel IDs", os.getenv("TG_CHANNELS", ""), theme, "-100...")
        CTkToolTip(parent.entry_channels, parent.translator.get("hint_tg_chan"))
        
        # AI Parsing Engine Section
        parse_card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        parse_card.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(parse_card, text="🧠 AI Parsing Engine (Signal Decoder)", font=FONTS["section_header"],
                     text_color=theme["text_primary"]).pack(anchor="w", padx=20, pady=(15, 5))
                     
        # Toggle Use AI
        row_ai = ctk.CTkFrame(parse_card, fg_color="transparent")
        row_ai.pack(fill="x", padx=20, pady=5)
        
        parent.use_ai_parsing = ctk.BooleanVar(value=str(os.getenv("USE_AI", "False")).lower() == "true")
        ctk.CTkSwitch(row_ai, text="Enable AI Fallback (Smart Parsing)", variable=parent.use_ai_parsing, 
                      font=FONTS["body_bold"], text_color=theme["text_primary"]).pack(side="left")
        CTkToolTip(row_ai, "Aktifkan jika format sinyal berantakan/tidak standar. AI akan mencoba menerjemahkannya.")

        # Provider Selector
        row_prov = ctk.CTkFrame(parse_card, fg_color="transparent")
        row_prov.pack(fill="x", padx=20, pady=(5, 15))
        
        ctk.CTkLabel(row_prov, text="AI Provider:", font=FONTS["body"], 
                     text_color=theme["text_secondary"]).pack(side="left", padx=(0, 10))
        
        parent.ai_provider = ctk.StringVar(value=os.getenv("AI_PROVIDER", "Groq"))
        ctk.CTkSegmentedButton(row_prov, values=["Gemini", "OpenRouter", "Groq"], 
                                variable=parent.ai_provider).pack(side="left")
        
        # Buttons
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkButton(btn_row, text=parent.translator.get("config_save"), font=FONTS["button"],
                      fg_color=theme["accent_success"], height=40, text_color="white",
                      command=parent.save_config).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(btn_row, text=parent.translator.get("tg_test"), font=FONTS["button"],
                      fg_color=theme["accent_primary"], height=40, text_color="white",
                      command=parent.test_telegram).pack(side="left", padx=(0, 10))

        # Start Button (Hidden initially, shown after success)
        parent.btn_start_copy_shortcut = ctk.CTkButton(btn_row, text="🚀 MULAI COPY TRADING", 
                                                      font=FONTS["button"],
                                                      fg_color="#10b981", hover_color="#059669",
                                                      height=40, text_color="white",
                                                      state="disabled",
                                                      command=lambda: parent.toggle_copier(from_shortcut=True))
        parent.btn_start_copy_shortcut.pack(side="left")
        
        if not getattr(parent, 'is_telegram_validated', False):
             parent.btn_start_copy_shortcut.pack_forget()
        
        # Contextual Tutorial Card 1: API Config
        from modules.ui.ui_components import ContextualTutorialCard
        tut_card_api = ContextualTutorialCard(
            page, 
            title=parent.translator.get("tut_card_tg_title"),
            steps_text=parent.translator.get("tut_card_tg_steps")
        )
        tut_card_api.pack(fill="x", pady=(20, 10))
        
        # Contextual Tutorial Card 2: Channel ID
        tut_card_chan = ContextualTutorialCard(
            page, 
            title=parent.translator.get("tut_card_chan_title"),
            steps_text=parent.translator.get("tut_card_chan_steps")
        )
        tut_card_chan.pack(fill="x", pady=(0, 20))
        
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
