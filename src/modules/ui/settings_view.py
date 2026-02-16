import os
import webbrowser
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from ui_theme import THEME_DARK, FONTS
from modules.ui.ui_helpers import UIHelpers

# --- THEME ---
# --- THEME ---
# REMOVED STATIC THEME

class SettingsView:
    """
    Modular class for the Settings page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Settings page and attaches it to the parent (App/GUI)."""
        # Dynamic Theme Loading
        theme = parent.theme_data if hasattr(parent, 'theme_data') else THEME_DARK
        
        page = ctk.CTkScrollableFrame(parent.main_container, fg_color="transparent", 
                                       scrollbar_button_color=theme["bg_tertiary"],
                                       scrollbar_button_hover_color=theme["accent_primary"],
                                       scrollbar_fg_color="transparent")
        
        # Profile Settings Card
        profile_card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        profile_card.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(profile_card, text=parent.translator.get("profile_header"), font=FONTS["section_header"],
                     text_color=theme["text_primary"]).pack(anchor="w", padx=20, pady=(15, 5))
        
        parent.entry_user_name = UIHelpers.create_field(profile_card, parent.translator.get("profile_name"), os.getenv("USER_NAME", ""), theme, "Ex: John Doe")
        parent.entry_user_email = UIHelpers.create_field(profile_card, parent.translator.get("profile_email"), os.getenv("USER_EMAIL", ""), theme, "Ex: john@example.com")
        parent.entry_user_phone = UIHelpers.create_field(profile_card, parent.translator.get("profile_phone"), os.getenv("USER_PHONE", ""), theme, "Ex: 08123456789")
        
        # Country Selection (Precise Alignment)
        row_c = ctk.CTkFrame(profile_card, fg_color="transparent")
        row_c.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(row_c, text="🏳️ Country / Region:", font=FONTS["body"], width=160, anchor="w", # Increased to 160 and anchored west
                     text_color=theme["text_secondary"]).pack(side="left")
        
        current_country = os.getenv("USER_COUNTRY", "ID")
        country_opts = ["ID (Indonesia)", "MY (Malaysia)", "US (United States)", "CN (China)", "IN (India)", "SG (Singapore)", "UK (United Kingdom)"]
        
        # Map code to full string for display
        display_val = next((x for x in country_opts if x.startswith(current_country)), "ID (Indonesia)")
        
        parent.entry_user_country = ctk.CTkOptionMenu(row_c, values=country_opts, font=FONTS["body"], 
                                                      height=36, # Matched height to entries
                                                      fg_color=theme["bg_tertiary"], button_color=theme["accent_primary"],
                                                      text_color=theme["text_primary"])
        parent.entry_user_country.set(display_val)
        parent.entry_user_country.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(page, text=parent.translator.get("settings_pro_info"), 
                     font=FONTS["body_small"], text_color=theme["text_disabled"], anchor="w").pack(fill="x", padx=25, pady=5) # Slightly more padx
        
        # Notification Bot Card
        notif_card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        notif_card.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(notif_card, text="📢 Notification Bot (Telegram Report)", font=FONTS["section_header"],
                     text_color=theme["text_primary"]).pack(anchor="w", padx=20, pady=(15, 5))
        
        row1 = ctk.CTkFrame(notif_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(row1, text="Bot Token:", font=FONTS["body"], width=160, anchor="w", # Standardized to 160 and anchored 'w'
                     text_color=theme["text_secondary"]).pack(side="left")
        parent.entry_bot_token = ctk.CTkEntry(row1, height=36, fg_color=theme["bg_tertiary"], text_color=theme["text_primary"])
        parent.entry_bot_token.insert(0, os.getenv("REPORT_BOT_TOKEN", ""))
        parent.entry_bot_token.pack(side="left", fill="x", expand=True)
        
        row2 = ctk.CTkFrame(notif_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(5, 15))
        ctk.CTkLabel(row2, text="Chat ID:", font=FONTS["body"], width=160, anchor="w", # Standardized to 160 and anchored 'w'
                     text_color=theme["text_secondary"]).pack(side="left")
        parent.entry_report_id = ctk.CTkEntry(row2, height=36, fg_color=theme["bg_tertiary"], text_color=theme["text_primary"])
        parent.entry_report_id.insert(0, os.getenv("REPORT_CHAT_ID", ""))
        parent.entry_report_id.pack(side="left", fill="x", expand=True)
        
        # Privacy Card
        privacy_card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        privacy_card.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(privacy_card, text=parent.translator.get("settings_privacy"), font=FONTS["section_header"],
                     text_color=theme["text_primary"]).pack(anchor="w", padx=20, pady=(15, 5))
        
        parent.chk_pub_profit = ctk.CTkCheckBox(privacy_card, text=parent.translator.get("settings_pub_profit"), font=FONTS["body"], text_color=theme["text_primary"])
        parent.chk_pub_profit.pack(anchor="w", padx=25, pady=5)
        # Robust boolean check: works for "True", "1", "True", etc.
        if str(os.getenv("PUBLISH_PROFIT", "False")).lower() in ["true", "1"]:
            parent.chk_pub_profit.select()
        
        parent.chk_pub_edu = ctk.CTkCheckBox(privacy_card, text=parent.translator.get("settings_pub_edu"), font=FONTS["body"], text_color=theme["text_primary"])
        parent.chk_pub_edu.pack(anchor="w", padx=25, pady=5)
        if str(os.getenv("PUBLISH_KNOWLEDGE", "True")).lower() in ["true", "1"]:
            parent.chk_pub_edu.select()

        parent.chk_initials = ctk.CTkCheckBox(privacy_card, text=parent.translator.get("settings_initials"), font=FONTS["body"], text_color=theme["text_primary"])
        parent.chk_initials.pack(anchor="w", padx=25, pady=5)
        if str(os.getenv("PUBLISH_INITIALS", "False")).lower() in ["true", "1"]:
            parent.chk_initials.select()

        parent.chk_show_hints = ctk.CTkCheckBox(privacy_card, text=parent.translator.get("settings_hints"), font=FONTS["body"], text_color=theme["text_primary"])
        parent.chk_show_hints.pack(anchor="w", padx=25, pady=(5, 15))
        if str(os.getenv("SHOW_HINTS", "True")).lower() in ["true", "1"]:
            parent.chk_show_hints.select()
        
        # Language Selector
        lang_frame = ctk.CTkFrame(privacy_card, fg_color="transparent")
        lang_frame.pack(fill="x", padx=25, pady=(5, 15))
        ctk.CTkLabel(lang_frame, text=parent.translator.get("settings_lang"), font=FONTS["body"], 
                     text_color=theme["text_secondary"]).pack(side="left", padx=(0, 10))
        parent.lang_selector = ctk.CTkOptionMenu(lang_frame, values=["ID (Indonesia)", "EN (English)"],
                                                font=FONTS["body"], fg_color=theme["bg_tertiary"],
                                                text_color=theme["text_primary"],
                                                button_color=theme["accent_primary"], width=200,
                                                command=lambda val: SettingsView._handle_instant_language(parent, val))
        current_lang = os.getenv("APP_LANGUAGE", "ID")
        parent.lang_selector.set(f"{current_lang} ({'Indonesia' if current_lang == 'ID' else 'English'})")
        parent.lang_selector.pack(side="left")

        # --- THEME & PERSONALIZATION CARD ---
        theme_card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        theme_card.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(theme_card, text="🎨 Personalization & Theme", font=FONTS["section_header"],
                     text_color=theme["text_primary"]).pack(anchor="w", padx=20, pady=(15, 5))
        
        theme_row = ctk.CTkFrame(theme_card, fg_color="transparent")
        theme_row.pack(fill="x", padx=20, pady=(5, 15))
        
        ctk.CTkLabel(theme_row, text="Select Interface Style:", font=FONTS["body"], width=150,
                     text_color=theme["text_secondary"]).pack(side="left")
        
        parent.theme_selector = ctk.CTkOptionMenu(theme_row, 
                                                 values=["Legacy Dark", "Modern Dark", "Modern Light", "Neutral Professional"],
                                                 font=FONTS["body"], fg_color=theme["bg_tertiary"],
                                                 text_color=theme["text_primary"],
                                                 button_color=theme["accent_primary"], width=230,
                                                 command=lambda val: SettingsView._handle_instant_theme(parent, val))
        
        current_theme_flag = os.getenv("UI_THEME", "dark")
        theme_map_rev = {
            "dark": "Legacy Dark", "dark_modern": "Modern Dark", 
            "light": "Modern Light", "neutral": "Neutral Professional"
        }
        parent.theme_selector.set(theme_map_rev.get(current_theme_flag, "Legacy Dark"))
        parent.theme_selector.pack(side="left", padx=10)

        # About Card
        about_card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        about_card.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(about_card, text=parent.translator.get("settings_about"), font=FONTS["section_header"],
                     text_color=theme["text_primary"]).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(about_card, text=parent.translator.get("app_title"),
                     font=FONTS["body"], text_color=theme["text_secondary"]).pack(anchor="w", padx=20)
        lbl_sub = ctk.CTkLabel(about_card, text="Powered By Haineo Operating System (OS) AI Richkeyrick",
                     font=FONTS["body_small"], text_color=theme["text_disabled"], cursor="hand2")
        lbl_sub.pack(anchor="w", padx=20, pady=(0, 10))
        lbl_sub.bind("<Button-1>", lambda e: webbrowser.open("https://richkeyrick.com"))
        
        ctk.CTkButton(about_card, text=parent.translator.get("settings_support"), font=FONTS["button"],
                      fg_color="#d29922", text_color="black", hover_color="#b8860b",
                      command=lambda: webbrowser.open("https://saweria.co/richkeyrick")).pack(padx=20, pady=(0, 5))

        # Check Updates Button
        ctk.CTkButton(about_card, text="🔄 Check For Updates", font=FONTS["button"],
                      fg_color=theme["bg_tertiary"], hover_color=theme["accent_primary"], text_color=theme["text_primary"],
                      command=lambda: parent.check_for_updates()).pack(padx=20, pady=(0, 15))
        
        # Action buttons row
        btn_row = ctk.CTkFrame(page, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=(15, 20))
        
        ctk.CTkButton(btn_row, text=parent.translator.get("settings_save"), font=("Segoe UI Semibold", 14),
                      fg_color=theme["accent_success"], height=48, corner_radius=8,
                      command=parent.save_config).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(btn_row, text=parent.translator.get("settings_logout"), font=("Segoe UI Semibold", 14),
                      fg_color="#30363d", hover_color="#e74c3c", height=48, corner_radius=8,
                      command=parent.logout).pack(side="left", fill="x", expand=True)
        
        return page

    @staticmethod
    def _handle_instant_theme(parent, selected_display):
        """Helper to map selection and trigger live theme change with confirmation."""
        theme_map = {
            "Legacy Dark": "dark",
            "Modern Dark": "dark_modern",
            "Modern Light": "light",
            "Neutral Professional": "neutral"
        }
        
        current_theme = os.getenv("UI_THEME", "dark")
        new_theme_flag = theme_map.get(selected_display, "dark")
        
        # 1. Ignore if same theme selected
        if new_theme_flag == current_theme:
            return

        # 2. Confirm Restart
        msg = CTkMessagebox(title="Restart Required", 
                            message="Changing the theme requires an application restart.\nDo you want to proceed?",
                            icon="question", option_1="Yes", option_2="No")
        
        if msg.get() == "Yes":
            if hasattr(parent, 'change_theme'):
                parent.change_theme(new_theme_flag)
        else:
            # Revert selection to current theme
            reverse_map = {v: k for k, v in theme_map.items()}
            old_display = reverse_map.get(current_theme, "Legacy Dark")
            parent.theme_selector.set(old_display)

    @staticmethod
    def _handle_instant_language(parent, selected_val):
        """Helper to map selection and trigger live language change with confirmation."""
        # Map Display -> Code
        lang_code = "ID" if "Indonesia" in selected_val else "EN"
        
        current_lang = os.getenv("APP_LANGUAGE", "ID")
        
        # 1. Ignore if same
        if lang_code == current_lang:
            return

        # 2. Confirm Restart
        msg = CTkMessagebox(title="Restart Required", 
                            message="Changing the language requires an application restart.\nDo you want to proceed?",
                            icon="question", option_1="Yes", option_2="No")
        
        if msg.get() == "Yes":
            if hasattr(parent, 'change_language'):
                parent.change_language(lang_code)
        else:
            # Revert selection
            old_display = f"{current_lang} ({'Indonesia' if current_lang == 'ID' else 'English'})"
            parent.lang_selector.set(old_display)
