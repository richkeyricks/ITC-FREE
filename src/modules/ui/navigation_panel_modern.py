import customtkinter as ctk
import webbrowser
from ui_theme_modern import get_theme, FONTS
from utils.tooltips import CTkToolTip

class ModernNavigationPanel:
    """
    Modern, Sleek Sidebar & Topbar Component.
    Features glassmorphism, smooth animations, and professional design.
    """

    @staticmethod
    def create_topbar(parent):
        """Builds the Modern Topbar interface with glassmorphism effect"""
        theme = get_theme(parent.selected_theme if hasattr(parent, 'selected_theme') else 'dark')
        
        topbar = ctk.CTkFrame(parent, fg_color=theme["bg_secondary"], height=80, corner_radius=0)
        topbar.pack(fill="x", side="top", padx=10, pady=(10, 5))
        topbar.pack_propagate(False)

        # Left side - Branding & Navigation
        left_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        left_frame.pack(side="left", padx=15)

        # Brand Logo/Icon
        logo_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        logo_frame.pack(side="left", padx=(0, 20))

        # Brand Title
        brand_row = ctk.CTkFrame(logo_frame, fg_color="transparent")
        brand_row.pack()

        ctk.CTkLabel(brand_row, text="ITC", 
                     font=("Inter Black", 24), text_color=theme["accent_primary"]).pack(side="left")
        ctk.CTkLabel(brand_row, text=" +AI",
                     font=("Inter ExtraBold", 24), text_color=theme["accent_secondary"]).pack(side="left")

        # Subtitle
        lbl_sub = ctk.CTkLabel(logo_frame, text=parent.translator.get("nav_subtitle"),
                     font=("Inter", 10), text_color=theme["text_secondary"])
        lbl_sub.pack(anchor="w")

        # Center - Navigation Tabs (Modern Tab-like Interface)
        nav_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        nav_frame.pack(side="left", expand=True)

        # Navigation buttons with modern styling
        nav_items = [
            ("🏠", parent.translator.get("nav_dashboard"), "dashboard"),
            ("📊", parent.translator.get("nav_analytics"), "analysis"),
            ("🛍️", parent.translator.get("nav_marketplace"), "signals"),
            ("🤖", parent.translator.get("nav_ai"), "ai"),
            ("📰", parent.translator.get("nav_news"), "news"),
            ("🏆", parent.translator.get("nav_leaderboard"), "leaderboard"),
        ]

        parent.nav_buttons = {}
        for icon, label, page_id in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=f"{icon} {label}",
                font=FONTS["body_small"],
                fg_color=theme["bg_tertiary"],
                hover_color=theme["bg_secondary"],
                text_color=theme["text_secondary"],
                height=36,
                corner_radius=8,
                command=lambda p=page_id: parent.show_page(p)
            )
            btn.pack(side="left", padx=5)
            parent.nav_buttons[page_id] = btn

        # Right side - Status Badges & Controls
        # Container for Status & Membership (Vertical Stack)
        right_stack = ctk.CTkFrame(topbar, fg_color="transparent")
        right_stack.pack(side="right", padx=(10, 20), fill="y", pady=5)

        # Row 1: Status Badges (Top)
        status_row = ctk.CTkFrame(right_stack, fg_color="transparent", height=20)
        status_row.pack(side="top", anchor="e")
        
        parent.badge_net = ModernNavigationPanel._create_status_badge(parent, status_row, parent.translator.get("badge_internet"), "red", theme)
        parent.badge_tg = ModernNavigationPanel._create_status_badge(parent, status_row, parent.translator.get("badge_telegram"), "red", theme)
        parent.badge_mt5 = ModernNavigationPanel._create_status_badge(parent, status_row, parent.translator.get("badge_mt5"), "red", theme)

        # Row 2: Membership Badge (Bottom - Prominent)
        ModernNavigationPanel._create_membership_badge(parent, right_stack, theme)

        # Settings and help buttons (Far Right, outside the stack)
        controls_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        controls_frame.pack(side="right", padx=(0, 5))

        # Premium Shortcut (CROWN)
        ctk.CTkButton(controls_frame, text="👑", width=36, height=36,
                      fg_color="#ffd700", hover_color="#d97706",
                      text_color="#000000",
                      corner_radius=8,
                      command=lambda: parent.show_page("subscription")).pack(side="left", padx=3)

        ctk.CTkButton(controls_frame, text="⚙", width=36, height=36,
                      fg_color=theme["bg_tertiary"], hover_color=theme["bg_secondary"],
                      text_color=theme["text_primary"],
                      corner_radius=8,
                      command=lambda: parent.show_page("settings")).pack(side="left", padx=3)
        
        ctk.CTkButton(controls_frame, text="❓", width=36, height=36,
                      fg_color=theme["bg_tertiary"], hover_color=theme["bg_secondary"],
                      text_color=theme["text_primary"],
                      corner_radius=8,
                      command=parent.open_tutorial).pack(side="left", padx=3)

        return topbar

    @staticmethod
    def _create_membership_badge(parent, container, theme):
        """Creates the Premium Membership Identity Badge"""
        badge_frame = ctk.CTkFrame(container, fg_color="transparent")
        badge_frame.pack(side="top", anchor="e", pady=(2, 0))

        # 1. Determine Tier (Simulation Logic for now, to be replaced by DB Enum)
        tier_label = "FREE MEMBER"
        tier_color = theme["text_secondary"]
        is_pro = False
        
        if hasattr(parent, 'db_manager') and parent.db_manager:
            dm = parent.db_manager
            if dm.is_pro_user():
                is_pro = True
                
                # Use centralized logic from SupabaseManager
                tier = dm.get_user_tier().upper()
                cycle = dm.get_user_cycle() 
                cycle_text = parent.translator.get(f"cycle_{cycle.lower()}", cycle)
                
                if tier == "INSTITUTIONAL":
                    tier_label = f"💎 INSTITUTIONAL • {cycle_text}"
                    tier_color = "#DC143C" # Crimson
                elif tier == "PLATINUM":
                    tier_label = f"💠 PLATINUM VIP ({cycle_text})"
                    tier_color = "#00BFFF" # Deep Sky Blue
                else: 
                    # Default GOLD/Other pro
                    tier_label = f"👑 {tier} PRO ({cycle_text})"
                    tier_color = "#FFD700" # Gold
            else:
                tier_label = "FREE MEMBER"
                tier_color = "#9CA3AF" # Gray

        # 2. Render Badge
        # Glow Effect Layer (Shadow)
        shadow_lbl = ctk.CTkLabel(badge_frame, text=tier_label, 
                                font=("Segoe UI Black", 13), 
                                text_color=tier_color)
        shadow_lbl.pack()
        
        # Add 'glow' effect by stacking labels if needed, or just high contrast color
        # For now, simple high-contrast bold text is cleaner for MVP
        
        # Save reference to update later
        parent.lbl_membership = shadow_lbl

    @staticmethod
    def _create_status_badge(parent, container, text, color, theme):
        """Creates a modern status badge with icon and text"""
        frame = ctk.CTkFrame(container, fg_color="transparent")
        frame.pack(side="left", padx=8)

        # Status indicator circle
        status_circle = ctk.CTkLabel(frame, text="●", text_color=color, font=("Segoe UI", 14))
        status_circle.pack(side="left", padx=(0, 6))

        # Status text
        label = ctk.CTkLabel(frame, text=text.upper(), font=("Inter Medium", 10),
                             text_color=theme["text_secondary"])
        label.pack(side="left")

        return status_circle

    @staticmethod
    def create_sidebar(parent):
        """Builds the Modern Sidebar interface with sleek design"""
        theme = get_theme(parent.selected_theme if hasattr(parent, 'selected_theme') else 'dark')
        
        # --- SINGULAR SIDEBAR LOGIC (Permanent Container) ---
        if not hasattr(parent, 'sidebar_instance') or not parent.sidebar_instance.winfo_exists():
            sidebar = ctk.CTkFrame(parent, fg_color=theme["sidebar_bg"], width=220, corner_radius=12,
                                border_width=1, border_color=theme["border_default"])
            sidebar.pack(fill="y", side="left", padx=10, pady=10)
            sidebar.pack_propagate(False)
            parent.sidebar_instance = sidebar
            
            # Header
            header_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(15, 20))
            ctk.CTkLabel(header_frame, text=parent.translator.get("menu_title"), font=("Inter Bold", 14), 
                        text_color=theme["accent_primary"]).pack(anchor="w")

            # Content Scrollable (Permanent)
            parent.menu_scroll_frame = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
            parent.menu_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

            # Bottom Actions (Permanent)
            parent.bottom_frame = ctk.CTkFrame(sidebar, fg_color=theme["bg_tertiary"], corner_radius=10)
            parent.bottom_frame.pack(fill="x", padx=10, pady=10)
            bottom_inner = ctk.CTkFrame(parent.bottom_frame, fg_color="transparent")
            bottom_inner.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkButton(bottom_inner, text=parent.translator.get("menu_upgrade"), font=FONTS["body_small"],
                         fg_color="#ffd700", hover_color="#d97706", text_color="#000000",
                         height=36, corner_radius=8,
                         command=lambda: parent.show_page("subscription")).pack(fill="x", pady=(0, 8))
            
            ctk.CTkButton(bottom_inner, text=parent.translator.get("menu_logout"), font=FONTS["body_small"],
                         fg_color="#b91c1c", hover_color="#991b1b", 
                         height=36, corner_radius=8,
                         command=parent.logout).pack(fill="x")

            # Store mapping for visibility toggle
            parent.category_sub_frames = {} 
            parent.category_arrows = {}
            
            ModernNavigationPanel._build_menu_widgets(parent, theme)

        return parent.sidebar_instance

    @staticmethod
    def _build_menu_widgets(parent, theme):
        """Creates all menu widgets once without packing sub-items initially if collapsed"""
        if not hasattr(parent, 'menu_expanded'):
            parent.menu_expanded = {parent.translator.get("cat_broker"): False, parent.translator.get("cat_system_log"): False}

        menu_items = [
            ("🏠", parent.translator.get("nav_dashboard"), "dashboard", None),
            ("🤖", parent.translator.get("nav_ai"), "ai", None),
            ("📰", parent.translator.get("nav_news"), "news", None),
            ("💎", parent.translator.get("menu_upgrade"), "subscription", None),
            
            # Categories & Children
            ("💎", parent.translator.get("menu_merchant"), "merchant", None),
            
            ("🏢", parent.translator.get("cat_broker"), "toggle_broker", None),
            ("      ↳ 🔹", parent.translator.get("menu_broker"), "broker", parent.translator.get("cat_broker")),
            ("      ↳ 🔹", parent.translator.get("menu_vps"), "vps", parent.translator.get("cat_broker")),
            ("      ↳ 🔹", parent.translator.get("menu_partners"), "other_partners", parent.translator.get("cat_broker")),
            
            ("🛍️", parent.translator.get("nav_marketplace"), "signals", None),
            
            ("📡", parent.translator.get("menu_broadcast"), "spc", None),
            ("🎓", parent.translator.get("menu_academy"), "education", None), 
            
            ("🦉", parent.translator.get("menu_wisdom"), "donation", None),
            ("🏆", parent.translator.get("nav_leaderboard"), ("leaderboard", "ARENA"), None),
            ("🗺️", parent.translator.get("menu_roadmap"), "roadmap", None), # Moved up for prominence

            ("", parent.translator.get("cat_system_log"), "logs", None),
            ("📖", parent.translator.get("menu_journal"), "journal", None),
            
            ("📈", parent.translator.get("menu_mt5"), "mt5", None),
            ("⚡", parent.translator.get("menu_trading_rules"), "trading", None),
            ("🛡️", parent.translator.get("menu_risk"), "risk", None),
            ("📊", parent.translator.get("menu_ai_analysis"), "analysis", None),
            ("💬", parent.translator.get("menu_telegram"), "telegram", None),
            ("⚙️", parent.translator.get("menu_setting"), "settings", None),
        ]

        # Admin Panel (Guarded)
        try:
            is_admin = False
            if hasattr(parent, 'db_manager') and parent.db_manager:
                is_admin = parent.db_manager.check_is_admin()
        except: 
            is_admin = False
            
        if is_admin:
            menu_items.append(("️", "Admin Panel", "admin", None))
            menu_items.append(("", "Inspector Panel", "inspector", None))

        parent.menu_buttons = {}
        tips = {
            "dashboard": parent.translator.get("tip_dashboard"),
            "signals": parent.translator.get("tip_signals"),
            "news": parent.translator.get("nav_news"),
            "donation": "The Hall of Wisdom - Honor our global contributors.",
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
            "journal": "System technical history and chronicle.",
            "settings": parent.translator.get("tip_settings"),
            "admin": parent.translator.get("tip_admin")
        }

        for item in menu_items:
            icon, label_text, page_id, parent_id = item[0], item[1], item[2], item[3] if len(item) > 3 else None
            
            # 1. Handle Categories (Toggles)
            if str(page_id).startswith("toggle_"):
                # Create Category Header
                btn_frame = ctk.CTkFrame(parent.menu_scroll_frame, fg_color="transparent", corner_radius=10, height=40)
                btn_frame.pack(fill="x", pady=2, padx=5)
                btn_frame.pack_propagate(False)

                is_expanded = parent.menu_expanded.get(label_text, False)
                arrow = " ▾" if is_expanded else " ▸"
                
                icon_lbl = ctk.CTkLabel(btn_frame, text=icon, font=theme.get("body_font", FONTS["body"]), text_color=theme["text_primary"])
                icon_lbl.place(x=12, rely=0.5, anchor="w")
                
                text_lbl = ctk.CTkLabel(btn_frame, text=label_text + arrow, font=theme.get("body_font", FONTS["body"]), anchor="w", text_color=theme["text_primary"])
                text_lbl.place(x=48, rely=0.5, anchor="w")

                # Create Sub-Frame Container for children
                sub_frame = ctk.CTkFrame(parent.menu_scroll_frame, fg_color="transparent")
                if is_expanded:
                    sub_frame.pack(fill="x")
                
                parent.category_sub_frames[label_text] = sub_frame
                parent.category_arrows[label_text] = text_lbl

                def toggle_action(e, lbl=label_text, current_btn_frame=btn_frame):
                    state = not parent.menu_expanded.get(lbl, False)
                    parent.menu_expanded[lbl] = state
                    
                    # Flicker-free visibility toggle
                    if state:
                        parent.category_sub_frames[lbl].pack(fill="x", after=current_btn_frame)
                        parent.category_arrows[lbl].configure(text=lbl + " ▾")
                    else:
                        parent.category_sub_frames[lbl].pack_forget()
                        parent.category_arrows[lbl].configure(text=lbl + " ▸")

                for w in [btn_frame, icon_lbl, text_lbl]:
                    w.bind("<Button-1>", toggle_action)
                    w.bind("<Enter>", lambda e, f=btn_frame: f.configure(fg_color=theme["sidebar_hover_bg"]))
                    w.bind("<Leave>", lambda e, f=btn_frame: f.configure(fg_color="transparent"))
                    try: w.configure(cursor="hand2")
                    except: pass

            # 2. Handle Normal Items & Children
            else:
                target_container = parent.menu_scroll_frame if not parent_id else parent.category_sub_frames.get(parent_id, parent.menu_scroll_frame)
                
                btn_frame = ctk.CTkFrame(target_container, fg_color="transparent", corner_radius=10, height=40)
                btn_frame.pack(fill="x", pady=2, padx=5)
                btn_frame.pack_propagate(False)

                indent_x = 12 if not parent_id else 24
                text_x = 48 if not parent_id else 54

                icon_lbl = ctk.CTkLabel(btn_frame, text=icon, font=theme.get("body_font", FONTS["body"]), text_color=theme["text_primary"])
                icon_lbl.place(x=indent_x, rely=0.5, anchor="w")
                
                text_lbl = ctk.CTkLabel(btn_frame, text=label_text, font=theme.get("body_font", FONTS["body"]), anchor="w", text_color=theme["text_primary"])
                text_lbl.place(x=text_x, rely=0.5, anchor="w")

                def nav_click(e, p=page_id):
                    if isinstance(p, tuple): parent.show_page(p[0], sub_tab=p[1])
                    else: parent.show_page(p)

                for w in [btn_frame, icon_lbl, text_lbl]:
                    w.bind("<Button-1>", nav_click)
                    w.bind("<Enter>", lambda e, f=btn_frame: f.configure(fg_color=theme["sidebar_hover_bg"]))
                    
                    # Fix: Check if active before resetting to transparent
                    def _on_leave(e, f=btn_frame, p=page_id):
                        curr = getattr(parent, 'current_page', '')
                        # Handle Tuple IDs (e.g. Leaderboard)
                        match = (curr == p) or (isinstance(p, tuple) and curr == p[0])
                        
                        f.configure(fg_color=theme["bg_tertiary"] if match else "transparent")
                        
                    w.bind("<Leave>", _on_leave)
                    
                    try: w.configure(cursor="hand2")
                    except: pass

                parent.menu_buttons[page_id] = btn_frame
            
            if page_id in tips:
                CTkToolTip(btn_frame, tips[page_id])

    @staticmethod
    def render_menu_items(parent):
        """
        This method is now deprecated.
        The menu items are built once by _build_menu_widgets and
        their visibility is managed by pack/pack_forget for categories.
        This method is kept as a placeholder if external calls still exist.
        """
        # If the sidebar was just created, _build_menu_widgets already ran.
        # If it's a theme change, we might need to reconfigure colors, but not rebuild structure.
        # For now, this method does nothing as the structure is permanent.
        pass
