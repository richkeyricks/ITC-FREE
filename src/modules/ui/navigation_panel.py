import customtkinter as ctk
import webbrowser
from ui_theme import THEME_DARK, FONTS
from utils.tooltips import CTkToolTip

class NavigationPanel:
    """
    Modular Sidebar & Topbar Component.
    Follows Gravity Dev Rules: Modular UI.
    """

    @staticmethod
    def create_topbar(parent):
        """Builds the Topbar interface with Combined Navigation Row"""
        # Slimmer height for a more professional look (105 -> 90)
        topbar = ctk.CTkFrame(parent, fg_color="#1a1d23", height=90, corner_radius=0)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)
        
        # ROW 1: Branding (Centered) & Status (Right)
        brand_row = ctk.CTkFrame(topbar, fg_color="transparent", height=45)
        brand_row.pack(fill="x", side="top", padx=15, pady=(2, 0))
        brand_row.pack_propagate(False)

        # CENTER - Branding Title
        title_frame = ctk.CTkFrame(brand_row, fg_color="transparent")
        title_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        branding_box = ctk.CTkFrame(title_frame, fg_color="transparent")
        branding_box.pack()
        
        ctk.CTkLabel(branding_box, text="INTELLIGENCE TELEGRAM COPYTRADE (ITC)", 
                     font=("Segoe UI Semibold", 16), text_color="white").pack(side="left")
        ctk.CTkLabel(branding_box, text=" +AI", 
                     font=("Segoe UI Bold", 19), text_color=THEME_DARK["accent_primary"]).pack(side="left")
        
        # Right side - Status Badges
        status_frame = ctk.CTkFrame(brand_row, fg_color="transparent")
        status_frame.pack(side="right")
        
        parent.badge_net = NavigationPanel._create_badge(parent, status_frame, parent.translator.get("status_online"), "red")
        parent.badge_tg = NavigationPanel._create_badge(parent, status_frame, "Telegram", "red")
        parent.badge_mt5 = NavigationPanel._create_badge(parent, status_frame, "MT5", "red")

        # ROW 2: Combined Menu Row (Utilities + Navigation)
        menu_row = ctk.CTkFrame(topbar, fg_color="transparent", height=40)
        menu_row.pack(fill="x", side="bottom", pady=(0, 5))
        menu_row.pack_propagate(False)

        # 1. UTILITY BUTTONS (Aligned Left)
        utils_frame = ctk.CTkFrame(menu_row, fg_color="transparent")
        utils_frame.pack(side="left", padx=15)
        
        for icon, cmd, color in [("👑", lambda: parent.show_page("subscription"), "#ffd700"), ("❓", parent.open_tutorial, THEME_DARK["bg_tertiary"]), ("⚙", lambda: parent.show_page("settings"), THEME_DARK["bg_tertiary"]), ("📋", parent.show_changelog, THEME_DARK["bg_tertiary"])]:
            ctk.CTkButton(utils_frame, text=icon, width=32, height=32, corner_radius=8,
                          fg_color=color, hover_color=THEME_DARK["accent_primary"] if color != "#ffd700" else "#d97706",
                          text_color="#000000" if color == "#ffd700" else "white",
                          command=cmd).pack(side="left", padx=3)

        # 2. MAIN NAVIGATION (Centered)
        nav_container = ctk.CTkFrame(menu_row, fg_color="transparent")
        nav_container.place(relx=0.5, rely=0.5, anchor="center")

        quick_items = [
            ("🏠 Dashboard", "dashboard"),
            ("🛍️ Marketplace", "signals"),
            ("🤖 Asisten AI", "ai"),
            ("📊 AI Analysis", "analysis"),
            ("🏆 Leaderboard", "leaderboard")
        ]

        for text, page_id in quick_items:
            btn = ctk.CTkButton(nav_container, text=text, height=30, width=120,
                               fg_color=THEME_DARK["bg_tertiary"],
                               hover_color=THEME_DARK["accent_primary"],
                               text_color="white", corner_radius=8,
                               font=FONTS["body_small"],
                               command=lambda p=page_id: parent.show_page(p))
            btn.pack(side="left", padx=4)
        
        return topbar

    @staticmethod
    def _create_badge(parent, container, text, color):
        """Creates a compact, professional status indicator"""
        frame = ctk.CTkFrame(container, fg_color="transparent")
        frame.pack(side="left", padx=6) # Reduced padding
        
        # Glow Dot
        dot = ctk.CTkLabel(frame, text="●", text_color=color, font=("Segoe UI", 11))
        dot.pack(side="left", padx=(0, 2))
        
        # Label (Small & Subtle)
        label = ctk.CTkLabel(frame, text=text.upper(), font=("Segoe UI Bold", 8), 
                              text_color=THEME_DARK["text_secondary"])
        label.pack(side="left")
        
        return dot

    @staticmethod
    def create_sidebar(parent):
        """Builds the Sidebar interface (Standardized)"""
        sidebar = ctk.CTkFrame(parent, fg_color=THEME_DARK["sidebar_bg"], width=220, corner_radius=0,
                                     border_width=1, border_color=THEME_DARK["border_default"])
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)
        
        # Menu Items
        menu_items = [
            ("🏠", parent.translator.get("menu_dashboard"), "dashboard"),
            ("💎", "UPGRADE PREM", "subscription"),
            ("🏦", "MERCHANT BANK", "merchant"),
            ("🛍️", "MARKETPLACE", "signals"),
            ("💎", parent.translator.get("menu_spc"), "spc"),
            ("🤖", parent.translator.get("menu_ai"), "ai"),
            ("🎓", parent.translator.get("menu_education"), "education"),
            ("🏆", "COMMUNITY", "leaderboard"),
            ("📊", parent.translator.get("menu_analysis"), "analysis"),
            ("💬", parent.translator.get("menu_telegram"), "telegram"),
            ("📈", parent.translator.get("menu_mt5"), "mt5"),
            ("⚡", parent.translator.get("menu_trading"), "trading"),
            ("🛡️", parent.translator.get("menu_risk"), "risk"),
            ("📔", parent.translator.get("menu_journal"), "journal"),
            ("📝", parent.translator.get("menu_logs"), "logs"),
            ("⚙️", parent.translator.get("menu_settings"), "settings"),
        ]
        
        if hasattr(parent, 'db_manager') and parent.db_manager.is_admin():
            # Standardized Title Case
            menu_items.insert(-1, ("👑", "Admin Panel", "admin"))
        
        # Bottom Actions
        bottom_box = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom_box.pack(side="bottom", fill="x", padx=10, pady=20)

        ctk.CTkButton(bottom_box, text="☕ DONASI", font=FONTS["body_small"],
                      fg_color="#ff813f", hover_color="#e67339", height=28, corner_radius=6,
                      command=parent.show_donation_info).pack(fill="x", pady=(0, 5))
        
        ctk.CTkButton(bottom_box, text="🚪 LOGOUT", font=FONTS["body_small"],
                      fg_color="#30363d", hover_color="#dc3545", height=28, corner_radius=6,
                      command=parent.logout).pack(fill="x")
        
        parent.menu_buttons = {}
        tips = {
            "dashboard": parent.translator.get("tip_dashboard"),
            "signals": parent.translator.get("tip_signals"),
            "spc": parent.translator.get("tip_spc"),
            "leaderboard": parent.translator.get("tip_leaderboard"),
            "education": parent.translator.get("tip_education"),
            "analysis": parent.translator.get("tip_analysis"),
            "telegram": parent.translator.get("tip_telegram"),
            "mt5": parent.translator.get("tip_mt5"),
            "trading": parent.translator.get("tip_trading"),
            "risk": parent.translator.get("tip_risk"),
            "ai": parent.translator.get("tip_ai"),
            "logs": parent.translator.get("tip_logs"),
            "journal": "Riwayat pembaruan sistem dan jurnal teknikal.",
            "settings": parent.translator.get("tip_settings"),
            "admin": parent.translator.get("tip_admin")
        }
        
        # Create scrollable frame for menu items to ensure consistency
        menu_scroll_frame = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        menu_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(10, 10))

        for icon, label, page_id in menu_items:
            # Use standard font for all (User Request: Seragam)
            btn_font = FONTS["body"]
            
            # --- ABSOLUTE GRID SYSTEM (The "Sejajar" Master Logic) ---
            # We use fixed height and .place() to force pixel-perfect alignment, 
            # bypassing all widget width fluctuations.
            
            btn_frame = ctk.CTkFrame(menu_scroll_frame, fg_color="transparent", corner_radius=8, height=40)
            btn_frame.pack(fill="x", pady=2, padx=5)
            btn_frame.pack_propagate(False) # Strict height enforcement
            
            # 1. Icon (Absolute X=12)
            icon_lbl = ctk.CTkLabel(btn_frame, text=icon, font=btn_font,
                                   text_color=THEME_DARK["text_primary"])
            icon_lbl.place(x=12, rely=0.5, anchor="w")
            
            # 2. Text (Absolute X=48)
            # This ensures every single title starts at the exact same horizontal pixel.
            text_lbl = ctk.CTkLabel(btn_frame, text=label, font=btn_font, anchor="w",
                                   text_color=THEME_DARK["text_secondary"])
            text_lbl.place(x=48, rely=0.5, anchor="w")

            # --- CLICK HANDLERS ---
            def on_enter(e, f=btn_frame):
                f.configure(fg_color=THEME_DARK["sidebar_hover_bg"])
                
            def on_leave(e, f=btn_frame): 
                f.configure(fg_color="transparent")
                
            def on_click(e, p=page_id):
                parent.show_page(p)

            # Bind events to frame and labels
            for widget in [btn_frame, icon_lbl, text_lbl]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.bind("<Button-1>", on_click)
                try: widget.configure(cursor="hand2")
                except: pass

            # Attach labels for external update (gui.py compability)
            btn_frame.icon_lbl = icon_lbl
            btn_frame.text_lbl = text_lbl

            parent.menu_buttons[page_id] = btn_frame
            if page_id in tips:
                CTkToolTip(btn_frame, tips[page_id])
                
        return sidebar
