import os
import webbrowser
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS
from utils.tooltips import CTkToolTip

# --- THEME ---
# REMOVED STATIC THEME

class AIView:
    """
    Modular class for the AI Assistant page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the AI page and attaches it to the parent (App/GUI)."""
        # Dynamic Theme Injection
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK

        # 1. Main Container (Fixed, grid layout - No Page Scroll)
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(1, weight=1) # Row 1 (Chat) expands
        
        # 2. Header & Settings (Row 0)
        settings_container = ctk.CTkFrame(page, fg_color="transparent")
        settings_container.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        
        # Grid Layout for Header (Title Left, Copyright Right)
        settings_container.columnconfigure(0, weight=1)
        settings_container.columnconfigure(1, weight=0)
        
        # Title
        ctk.CTkLabel(settings_container, text=parent.translator.get("ai_title"), font=("Segoe UI Semibold", 22), 
                     text_color=theme["text_primary"], anchor="w").grid(row=0, column=0, sticky="w")
                     
        # Copyright
        lbl_copy = ctk.CTkLabel(settings_container, text=parent.translator.get("ai_copyright"), 
                                font=("Segoe UI", 10, "bold"), text_color="#3B8ED0", cursor="hand2")
        lbl_copy.grid(row=0, column=1, sticky="e", padx=(0, 10))
        lbl_copy.bind("<Button-1>", lambda e: webbrowser.open("https://www.haineo.com"))
        
        # Separator / Settings Box below
        settings = ctk.CTkFrame(settings_container, fg_color=theme["bg_secondary"], corner_radius=10)
        settings.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Row A: API Key (Moved up)
        row_a = ctk.CTkFrame(settings, fg_color="transparent")
        row_a.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(row_a, text=parent.translator.get("ai_key"), font=FONTS["body_small"],
                     text_color=theme["text_secondary"]).pack(side="left", padx=(0, 10))
        
        parent.entry_ai_key = ctk.CTkEntry(row_a, height=32, fg_color=theme["bg_tertiary"],
                                          border_color=theme["border_default"], width=300,
                                          placeholder_text="Optional (Leave empty for Free Server)")
        parent.entry_ai_key.insert(0, os.getenv("AI_API_KEY", ""))
        parent.entry_ai_key.pack(side="left", padx=(0, 15))

        # Row B: API Key Links
        row_b = ctk.CTkFrame(settings, fg_color="transparent")
        row_b.pack(fill="x", padx=15, pady=(0, 15))
        
        # Link buttons for getting keys
        
        for name, url in [("Get OpenRouter", "https://openrouter.ai/keys"), 
                          ("Get Gemini", "https://aistudio.google.com/app/apikey"), 
                          ("Get Groq", "https://console.groq.com/keys")]:
            ctk.CTkButton(row_b, text=name, width=80, height=28, font=("Segoe UI", 11),
                          fg_color=theme["bg_tertiary"], hover_color=theme["border_default"],
                          command=lambda u=url: webbrowser.open(u)).pack(side="left", padx=2)

        # 3. Chat Area (Row 1 - Expands)
        chat_frame = ctk.CTkFrame(page, fg_color="transparent")
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 10))
        
        ctk.CTkLabel(chat_frame, text=parent.translator.get("ai_chat_title"), font=FONTS["section_header"],
                     text_color=theme["text_secondary"], anchor="w").pack(fill="x", pady=(0, 5))
        
        parent.ai_chat_list = ctk.CTkScrollableFrame(chat_frame, fg_color="transparent")
        parent.ai_chat_list.pack(fill="both", expand=True)
        
        # Initial Welcome Bubble
        AIView.add_chat_bubble(parent, parent.translator.get('ai_chat_intro'), is_user=False)

        # 4. Quick Actions & Input Area (Row 2 & 3)
        input_container = ctk.CTkFrame(page, fg_color="transparent")
        input_container.grid(row=2, column=0, sticky="ew", padx=0, pady=(0, 5))
        
        # A. Quick Action Chips (Scrollable horizontal if needed, but simple row for now)
        chips_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        chips_frame.pack(fill="x", pady=(0, 5))
        
        # Search Toggle (Left side of chips)
        parent.search_var = ctk.BooleanVar(value=False)
        search_switch = ctk.CTkSwitch(chips_frame, text=parent.translator.get("ai_search_web"), 
                                     variable=parent.search_var, font=("Segoe UI Bold", 11),
                                     progress_color="#00E676", text_color="#00E676")
        search_switch.pack(side="left", padx=(0, 15))
        
        # Chip Buttons
        chips_data = [
            ("ai_chip_news", "berita viral hari ini"),
            ("ai_chip_xau", "analisa sentimen xauusd hari ini"),
            ("ai_chip_calendar", "kalender ekonomi hari ini impact high"),
            ("ai_chip_tech", "analisa teknikal market forex hari ini")
        ]
        
        for lang_key, prompt in chips_data:
            btn = ctk.CTkButton(chips_frame, text=parent.translator.get(lang_key), height=24,
                                font=("Segoe UI", 10), fg_color=theme["bg_tertiary"], 
                                text_color=theme["text_primary"], hover_color=theme["bg_secondary"],
                                corner_radius=12, width=80,
                                command=lambda p=prompt: parent.send_ai_message(force_search=True, prompt_override=p))
            btn.pack(side="left", padx=2)

        # B. Input Field
        input_row = ctk.CTkFrame(input_container, fg_color="transparent")
        input_row.pack(fill="x")

        parent.ai_input = ctk.CTkEntry(input_row, height=45, placeholder_text="Type your question here...",
                                      fg_color=theme["bg_tertiary"], border_width=1)
        parent.ai_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        parent.ai_input.bind("<Return>", lambda e: parent.send_ai_message())
        
        parent.ai_send_btn = ctk.CTkButton(input_row, text=parent.translator.get("ai_chat_send"), width=100, height=45, 
                                         command=lambda: parent.send_ai_message())
        parent.ai_send_btn.pack(side="right")
        CTkToolTip(parent.ai_send_btn, parent.translator.get("hint_ai_send"))
        
        # Check Cloud Pro Status (includes Admin check)
        is_pro = parent.db_manager.is_pro_user()
        
        # If not Pro, check usage
        if not is_pro:
             count = parent.db_manager.get_ai_message_count()
             if count >= 3:
                 AIView.show_locked_overlay(parent)
        else:
            # Auto-focus input for Pro/Admin users
            def update_ui():
                parent.ai_input.focus_set()
            parent.safe_ui_update(update_ui)
        
        return page

    @staticmethod
    def add_chat_bubble(parent, text, is_user=False, is_thinking=False):
        """Adds a WhatsApp-style chat bubble"""
        if not hasattr(parent, 'ai_chat_list') or not parent.ai_chat_list.winfo_exists(): return

        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        
        # Container for alignment
        row = ctk.CTkFrame(parent.ai_chat_list, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=10)
        
        # Bubble Styling
        bubble_color = theme["accent_primary"] if is_user else theme["bg_secondary"]
        text_color = "#FFFFFF" if is_user else theme["text_primary"]
        anchor = "e" if is_user else "w"
        justify = "right" if is_user else "left"
        
        # Inner Frame (The Bubble)
        bubble = ctk.CTkFrame(row, fg_color=bubble_color, corner_radius=16)
        bubble.pack(side="right" if is_user else "left", anchor=anchor, padx=5) # 'anchor' in pack doesn't work like grid, used side
        
        # Message Text
        font = ("Segoe UI", 13)
        if is_thinking:
            font = ("Segoe UI Italic", 12)
            
        label = ctk.CTkLabel(bubble, text=text, font=font, text_color=text_color, 
                             wraplength=450, justify="left", anchor="w") # Always left align text inside bubble for readability
        label.pack(padx=12, pady=8)
        
        # Auto-scroll
        parent.after(10, lambda: parent.ai_chat_list._parent_canvas.yview_moveto(1.0))
        
        return bubble # Return reference for updates (e.g. thinking)

    @staticmethod
    def show_locked_overlay(parent):
        """Displays the Pro Upgrade overlay over the AI page"""
        if not hasattr(parent, 'main_container'): return
        
        # Ensure we are on AI page
        if parent.current_page != "ai": return

        if hasattr(parent, 'ai_pro_overlay') and parent.ai_pro_overlay.winfo_exists():
            parent.ai_pro_overlay.destroy()

        # Find the active frame (it's parent.pages["ai"])
        page = parent.pages.get("ai")
        if not page: return

        parent.ai_pro_overlay = ctk.CTkFrame(page, fg_color="#15171c", corner_radius=12)
        # Position relative to current frame
        parent.ai_pro_overlay.place(relx=0.5, rely=0.75, relwidth=0.96, relheight=0.45, anchor="center")
        
        ctk.CTkLabel(parent.ai_pro_overlay, text=parent.translator.get("ai_locked_title"), font=("Segoe UI Bold", 18), text_color="#ff813f").pack(pady=(40, 5))
        ctk.CTkLabel(parent.ai_pro_overlay, text="Trial Limit Reached (3/3)", 
                        font=FONTS["body"], text_color="white").pack(pady=5)
        
        ctk.CTkButton(parent.ai_pro_overlay, text=parent.translator.get("ai_upgrade"), fg_color="#ff813f", hover_color="#e67339",
                        command=parent.show_donation_info).pack(pady=15)
        
        return page
