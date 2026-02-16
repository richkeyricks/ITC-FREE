# ══════════════════════════════════════════════════════════════════════════════
# 📊 MERCHANT DASHBOARD (CYBER-FINTECH EDITION v5.3)
# 🎯 ROLE: Viral Marketing Command Center & Affiliate Management
# 🎨 STYLE: High-Fidelity Dark Mode, Glassmorphism Hints, Neon Accents
# ══════════════════════════════════════════════════════════════════════════════

import threading
import time
import random
import webbrowser
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from modules.logic.merchant_service import MerchantService
from modules.logic.affiliate_service import AffiliateService
from modules.db.supabase_client import SupabaseManager
from utils.currency import format_currency, format_per_referral_estimate
from constants.marketing_data import SOCIAL_PLATFORMS, LEADERBOARD_NAMES
from ui_theme import RADIUS, SPACING

class MerchantDashboardView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#09090A") # Ultra Dark Background
        self.controller = controller
        
        try:
            # Initialize Services
            self.service = MerchantService(controller.db_manager)
            self.affiliate_service = AffiliateService(controller.db_manager)
            # Safe user_id access
            if hasattr(controller, 'db_manager') and hasattr(controller.db_manager, 'user_id'):
                self.user_id = controller.db_manager.user_id
            else:
                self.user_id = "anonymous"
            
            # Internal State
            self.ticker_index = 0
            self.boost_overlay = None # Singleton tracker
            
            self._setup_ui()
            self.refresh_data()
            self._start_ticker()
            
        except Exception as e:
            # CRITICAL ERROR HANDLER - Prevents Blank Screen
            print(f"MERCHANT DASHBOARD CRASH: {e}")
            traceback.print_exc()
            self._render_crash_screen(e)

    def _render_crash_screen(self, error):
        """Fallback UI if initialization fails"""
        for widget in self.winfo_children(): widget.destroy()
        
        err_frame = ctk.CTkFrame(self, fg_color="#18181B", corner_radius=12, border_width=1, border_color="red")
        err_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(err_frame, text="⚠️ SYSTEM FAILURE", font=("Consolas", 20, "bold"), text_color="red").pack(pady=(20, 10))
        ctk.CTkLabel(err_frame, text=f"Error: {str(error)}", font=("Consolas", 12), text_color="white").pack(padx=20, pady=10)
        ctk.CTkButton(err_frame, text="RETRY", command=lambda: self.controller.show_page("merchant")).pack(pady=20)

    def _setup_ui(self):
        self.columnconfigure(0, weight=3, minsize=300) # Left Zone (Fixed Width optimized)
        self.columnconfigure(1, weight=7) # Right Zone
        self.rowconfigure(0, weight=0)    # Ticker
        self.rowconfigure(1, weight=1)    # Main

        # 0. LEADERBOARD TICKER
        self._create_ticker_section()

        # 1. LEFT ZONE: DIGITAL IDENTITY CARD
        self.left_panel = ctk.CTkFrame(self, fg_color="#121214", corner_radius=0)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 1))
        
        # Inner "Card" Container
        self.card_frame = ctk.CTkFrame(self.left_panel, fg_color="#18181B", corner_radius=16, 
                                       border_width=1, border_color="#2A2A2F")
        self.card_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_identity_zone(self.card_frame)

        # 2. RIGHT ZONE: MATRIX & INTELLIGENCE
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        # Grid Configuration for Right Panel
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=0) # Header
        self.right_panel.rowconfigure(1, weight=0) # Matrix (Fixed Height)
        self.right_panel.rowconfigure(2, weight=0) # Financial Cards
        self.right_panel.rowconfigure(3, weight=0) # Calculator
        self.right_panel.rowconfigure(4, weight=1) # Logs (Expandable)

        self._create_matrix_zone(self.right_panel)
        self._create_financial_zone(self.right_panel)

    # ══════════════════════════════════════════════════════════════════════════
    # ZONE 0: TICKER (THE LAS VEGAS STRIP)
    # ══════════════════════════════════════════════════════════════════════════
    def _create_ticker_section(self):
        self.ticker_frame = ctk.CTkFrame(self, fg_color="#050505", height=32, corner_radius=0)
        self.ticker_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.ticker_frame.pack_propagate(False)
        
        # Blinking Dot
        self.lbl_dot = ctk.CTkLabel(self.ticker_frame, text="●", font=("Arial", 10), text_color="#FF0000")
        self.lbl_dot.pack(side="left", padx=(15, 5))
        self._blink_dot()
        
        ctk.CTkLabel(self.ticker_frame, text="LIVE PAYOUTS:", font=("Consolas", 10, "bold"), text_color="#00FFAA").pack(side="left", padx=(0, 15))
        
        # Scrolling Text
        self.lbl_ticker = ctk.CTkLabel(self.ticker_frame, text="Loading...", font=("Consolas", 10, "bold"), text_color="#FFD700")
        self.lbl_ticker.pack(side="left", fill="x", expand=True)

    def _blink_dot(self):
        if not self.winfo_exists(): return
        current_color = self.lbl_dot.cget("text_color")
        # Fix: transparency crashes CTk, toggle with BG color instead
        next_color = "#050505" if current_color == "#FF0000" else "#FF0000"
        self.lbl_dot.configure(text_color=next_color)
        self.after(800, self._blink_dot)

    def _start_ticker(self):
        def _run():
            # Generate static batch of fake data first
            data_pool = []
            for name in LEADERBOARD_NAMES:
                amt = random.randint(120, 8500)
                emoji = random.choice(["💸", "🚀", "💎", "⚡"])
                data_pool.append(f"{emoji} {name} ${amt}")
            
            # Scrolling logic
            display_width = 100 # Approx chars
            full_text = "   //   ".join(data_pool) * 2 # Duplicate for loop
            idx = 0
            
            while True:
                if not self.winfo_exists(): break
                try:
                    # Slicing for marquee effect
                    visible_text = full_text[idx:idx+display_width]
                    
                    # Update UI
                    if hasattr(self, 'lbl_ticker'):
                        self.lbl_ticker.configure(text=visible_text)
                    
                    idx += 1
                    if idx >= len(full_text)//2: idx = 0
                except: pass
                
                time.sleep(0.2) # Speed of scroll

        threading.Thread(target=_run, daemon=True).start()

    # ══════════════════════════════════════════════════════════════════════════
    # ZONE 1: IDENTITY CARD
    # ══════════════════════════════════════════════════════════════════════════
    def _create_identity_zone(self, parent):
        # Header Chip
        chip_frame = ctk.CTkFrame(parent, fg_color="transparent")
        chip_frame.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(chip_frame, text="ITC PARTNER ID", font=("OCR A Extended", 10), text_color="#555").pack(anchor="w")
        
        # Avatar & Glow
        av_cnt = ctk.CTkFrame(parent, fg_color="#000", width=90, height=90, corner_radius=45, border_width=2, border_color="#333")
        av_cnt.pack(pady=10)
        av_cnt.pack_propagate(False)
        ctk.CTkLabel(av_cnt, text="👾", font=("Arial", 42)).place(relx=0.5, rely=0.5, anchor="center")
        
        # Code Display
        self.lbl_code = ctk.CTkLabel(parent, text="---", font=("Consolas", 26, "bold"), text_color="white")
        self.lbl_code.pack(pady=(5, 0))
        
        # Tier Title
        self.lbl_tier_badge = ctk.CTkLabel(parent, text="STARTER AGENT", font=("Segoe UI", 12, "bold"), text_color="#666")
        self.lbl_tier_badge.pack(pady=(0, 20))

        # Divider
        ctk.CTkFrame(parent, height=2, fg_color="#222").pack(fill="x", padx=20, pady=5)

        # Progress Section
        p_frame = ctk.CTkFrame(parent, fg_color="transparent")
        p_frame.pack(fill="x", padx=20, pady=15)
        
        self.lbl_next_goal = ctk.CTkLabel(p_frame, text="Next: Gold (0/10)", font=("Segoe UI", 10), text_color="#888")
        self.lbl_next_goal.pack(anchor="w", pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(p_frame, height=6, corner_radius=3, progress_color="#00FFAA", fg_color="#333")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x")
        
        # BUTTONS (Bottom)
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom", padx=20, pady=20)
        
        # 🚀 INITIATE BOOST (Neon High-Performance)
        self.btn_boost = ctk.CTkButton(btn_frame, text="🚀  INITIATE BOOST", height=45,
                                       fg_color="#00FFAA", text_color="black", hover_color="#00FFCC",
                                       font=("Segoe UI Black", 13),
                                       border_width=2, border_color="#00FFAA",
                                       command=lambda: self._show_boost_overlay())
        self.btn_boost.pack(fill="x", pady=(0, 10))
        
        # 🏛️ ACCESS MARKET VAULT (Glassmorphism Luxury)
        self.btn_vault = ctk.CTkButton(btn_frame, text="🏛️  ACCESS MARKET VAULT", height=40,
                                       fg_color="#1F1F23",  # Semi-dark base
                                       hover_color="#2A2A2F", 
                                       border_width=1, border_color="#FFD700", # Gold glow
                                       text_color="#FFD700",
                                       font=("Segoe UI Black", 11),
                                       command=lambda: self.controller.show_page("marketing_vault"))
        self.btn_vault.pack(fill="x")

    # ══════════════════════════════════════════════════════════════════════════
    # ZONE 2: NEON MATRIX (GRID SYSTEM)
    # ══════════════════════════════════════════════════════════════════════════
    def _create_matrix_zone(self, parent):
        # Header with Gradient-like line
        h_box = ctk.CTkFrame(parent, fg_color="transparent")
        h_box.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(h_box, text="EMPYREAN ROADMAP", font=("Segoe UI Black", 14), text_color="#fff").pack(side="left")
        ctk.CTkLabel(h_box, text=" //  UNLOCK HIGHER COMMISSIONS", font=("Consolas", 10, "bold"), text_color="#444").pack(side="left", padx=10, pady=(4,0))
        
        # Main Grid Container
        self.matrix_grid = ctk.CTkFrame(parent, fg_color="#0D0D0F", corner_radius=10)
        self.matrix_grid.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Configure Grid Columns (7 Columns now)
        weights = [2, 1, 1, 1, 1, 1, 2] # Name, Req, Comm, Bonus, Expiry, Status, Action
        for i, w in enumerate(weights):
            self.matrix_grid.columnconfigure(i, weight=w)

        # HEADERS
        headers = ["RANK", "REQ", "COMM", "BONUS", "EXPIRY", "STATUS", "ACTION"]
        for idx, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.matrix_grid, text=h, font=("Segoe UI", 9, "bold"), text_color="#555")
            lbl.grid(row=0, column=idx, pady=10, padx=5, sticky="ew")
            # Vertical Divider (Visual Guide)
            if idx < len(headers)-1:
                sep = ctk.CTkFrame(self.matrix_grid, width=1, height=15, fg_color="#222")
                sep.grid(row=0, column=idx, sticky="e")

        # ROWS
        self.tier_rows = {}
        tiers = [
            ("STARTER", "0 Refs", "10%", "-", "#aaaaaa", 0),
            ("GOLD", "10 Refs", "15%", "$50", "#FFD700", 10),
            ("PLATINUM", "50 Refs", "20%", "$250", "#E5E4E2", 50),
            ("INSTITUTION", "100 Refs", "25%", "$1,000", "#00FFAA", 100)
        ]
        
        # Mock user tier for initial render (will be updated by _update_matrix_state)
        current_tier_threshold = 0 
        
        for idx, (name, req, comm, bonus, col, thres) in enumerate(tiers, start=1):
            # Rank
            icon = "🥉" if thres==0 else "🥇" if thres==10 else "💎" if thres==50 else "🏦"
            ctk.CTkLabel(self.matrix_grid, text=f"  {icon}  {name}", font=("Segoe UI Bold", 11), text_color=col, anchor="w").grid(row=idx, column=0, sticky="ew", pady=8, padx=10)
            # Req
            ctk.CTkLabel(self.matrix_grid, text=req, font=("Consolas", 11), text_color="#888").grid(row=idx, column=1, sticky="ew")
            # Comm
            ctk.CTkLabel(self.matrix_grid, text=comm, font=("Segoe UI Bold", 11), text_color="white").grid(row=idx, column=2, sticky="ew")
            # Bonus
            ctk.CTkLabel(self.matrix_grid, text=bonus, font=("Segoe UI", 11), text_color="#2CC985" if bonus!="-" else "#444").grid(row=idx, column=3, sticky="ew")
            
            # Expiry (Dynamic Placeholder)
            lbl_expiry = ctk.CTkLabel(self.matrix_grid, text="-", font=("Consolas", 10), text_color="#666")
            lbl_expiry.grid(row=idx, column=4, sticky="ew")

            # Status (Dynamic)
            lbl_stat = ctk.CTkLabel(self.matrix_grid, text="LOCKED", font=("Segoe UI", 10, "bold"), text_color="#444")
            lbl_stat.grid(row=idx, column=5, sticky="ew")
            
            # Action (Dynamic)
            btn = ctk.CTkButton(self.matrix_grid, text="...", height=24, font=("Segoe UI", 9, "bold"), corner_radius=12)
            btn.grid(row=idx, column=6, sticky="ew", padx=10)
            
            # Horizontal Divider
            if idx < len(tiers):
                div = ctk.CTkFrame(self.matrix_grid, height=1, fg_color="#1A1A1D")
                div.grid(row=idx, column=0, columnspan=7, sticky="ew", pady=(25, 0))

            self.tier_rows[name] = {
                "idx": idx, "status": lbl_stat, "action": btn, "expiry": lbl_expiry,
                "data": (name, req, comm, bonus, col, thres)
            }

    # ══════════════════════════════════════════════════════════════════════════
    # ZONE 3: FINANCIAL INTELLIGENCE (Widgets)
    # ══════════════════════════════════════════════════════════════════════════
    def _create_financial_zone(self, parent):
        # Grid for Cards (ROW 2)
        grid = ctk.CTkFrame(parent, fg_color="transparent")
        grid.grid(row=2, column=0, sticky="ew", pady=20)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)
        
        self.card_active = self._create_widget(grid, 0, "ACTIVE BALANCE", format_currency(0), "#2CC985")
        self.card_pending = self._create_widget(grid, 1, "PENDING (72H)", format_currency(0), "#FFD700")
        self.card_total = self._create_widget(grid, 2, "LIFETIME REVENUE", format_currency(0), "#666")

        # Wealth Calculator (ROW 3)
        calc_box = ctk.CTkFrame(parent, fg_color="#18181B", corner_radius=12, border_width=1, border_color="#222")
        calc_box.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        top = ctk.CTkFrame(calc_box, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(top, text="WEALTH SIMULATOR", font=("Segoe UI Bold", 11), text_color="#888").pack(side="left")
        
        self.lbl_calc_val = ctk.CTkLabel(top, text="10 Referrals", font=("Consolas", 11), text_color="#ccc")
        self.lbl_calc_val.pack(side="right")
        
        self.slider_calc = ctk.CTkSlider(calc_box, from_=0, to=1000, number_of_steps=100, 
                                         button_color="#00FFAA", button_hover_color="#00DD99", progress_color="#00FFAA",
                                         command=self._update_calculator)
        self.slider_calc.set(10)
        self.slider_calc.pack(fill="x", padx=15, pady=(0, 10))
        
        self.lbl_calc_result = ctk.CTkLabel(calc_box, text=format_per_referral_estimate(10), font=("Segoe UI", 16, "bold"), text_color="#00FFAA")
        self.lbl_calc_result.pack(pady=(0, 15))

        # Recent Activity (ROW 4)
        log_box = ctk.CTkFrame(parent, fg_color="#121214", corner_radius=12, border_width=1, border_color="#222")
        log_box.grid(row=4, column=0, sticky="nsew") 
        
        ctk.CTkLabel(log_box, text="REAL-TIME SIGNALS", font=("Segoe UI Bold", 10), text_color="#444").pack(anchor="w", padx=15, pady=10)
        
        self.log_scroll = ctk.CTkScrollableFrame(log_box, fg_color="transparent")
        self.log_scroll.pack(fill="both", expand=True, padx=5, pady=5)

    def _create_widget(self, parent, col, title, val, color):
        f = ctk.CTkFrame(parent, fg_color="#18181B", corner_radius=12, border_width=1, border_color="#222")
        f.grid(row=0, column=col, sticky="ew", padx=6)
        
        ctk.CTkLabel(f, text=title, font=("Segoe UI", 9, "bold"), text_color="#555").pack(anchor="w", padx=15, pady=(15, 0))
        lbl = ctk.CTkLabel(f, text=val, font=("Segoe UI", 18, "bold"), text_color=color)
        lbl.pack(anchor="w", padx=15, pady=(5, 15))
        f.lbl_val = lbl
        return f

    # ══════════════════════════════════════════════════════════════════════════
    # LOGIC
    # ══════════════════════════════════════════════════════════════════════════
    def _update_calculator(self, val):
        count = int(val)
        self.lbl_calc_val.configure(text=f"{count} Referrals")
        self.lbl_calc_result.configure(text=format_per_referral_estimate(count))

    def _show_boost_overlay(self):
        # SINGLETON CHECK
        if self.boost_overlay is not None and self.boost_overlay.winfo_exists():
            self.boost_overlay.lift()
            self.boost_overlay.focus_force()
            return

        self.boost_overlay = ctk.CTkToplevel(self)
        self.boost_overlay.title("SYNDICATE")
        self.boost_overlay.geometry("640x520")
        self.boost_overlay.configure(fg_color="#09090A")
        self.boost_overlay.attributes("-topmost", True)
        self.boost_overlay.transient(self) # Bind to main window
        self.boost_overlay.grab_set() # Modal Mode
        
        ctk.CTkLabel(self.boost_overlay, text="DEPLOY TO NETWORK", font=("Segoe UI Black", 18), text_color="#00FFAA").pack(pady=25)
        
        grid = ctk.CTkScrollableFrame(self.boost_overlay, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=30, pady=10)
        
        for i in range(4): grid.columnconfigure(i, weight=1)
        
        my_link = f"https://itc.app/ref/{getattr(self, 'my_ref_code', 'JOIN')}"
        
        for idx, item in enumerate(SOCIAL_PLATFORMS):
            btn = ctk.CTkButton(grid, text=f"{item['icon']}  {item['name']}", 
                                fg_color="#18181B", hover_color=item['color'], 
                                border_width=1, border_color="#222",
                                width=120, height=55,
                                font=("Segoe UI Bold", 11),
                                command=lambda x=item: self._share_to(x, my_link))
            btn.grid(row=idx//4, column=idx%4, padx=6, pady=6)
            
        ctk.CTkButton(self.boost_overlay, text="DISMISS", command=self.boost_overlay.destroy, 
                      fg_color="transparent", text_color="gray", hover_color="#111").pack(pady=15)

    def _share_to(self, platform, link):
        text_template = platform.get("template_id", "")
        final_text = text_template.replace("{link}", link)
        
        self.clipboard_clear()
        self.clipboard_append(final_text)
        
        url_scheme = platform.get("url_scheme", "")
        if url_scheme and url_scheme != "COPY":
            from urllib.parse import quote
            safe_text = quote(final_text)
            safe_link = quote(link)
            final_url = url_scheme.replace("{link}", safe_link).replace("{text}", safe_text)
            webbrowser.open(final_url)
            CTkMessagebox(title="Launching", message=f"Opening {platform['name']}...", icon="info")
        else:
             CTkMessagebox(title="Copied", message="Link Copied!", icon="check")
    
    def refresh_data(self):
        def _task():
            # mock failure protection
            wallet = {"balance_active": 0, "balance_pending": 0, "total_earned": 0}
            stats = {"code": "---", "count": 0, "earnings": 0, "tier_info": {"name": "STARTER", "color": "#aaaaaa", "next": 10}}
            profile = {}

            try:
                # 1. Fetch Wallet via SERVICE (Returns Dict, not Float)
                if hasattr(self, 'service'):
                     w_res = self.service.get_wallet_balance(self.user_id)
                     if w_res: wallet = w_res
                
                # 3. Fetch User Profile
                if hasattr(self.controller.db_manager, 'get_user_profile'):
                    p_res = self.controller.db_manager.get_user_profile()
                    if p_res: profile = p_res

                # 2. Fetch Affiliate Stats
                if hasattr(self.controller, 'affiliate_service') and self.controller.affiliate_service:
                    stats = self.controller.affiliate_service.get_my_stats()

            except Exception as e:
                print(f"// Dashboard Data Error: {e}")

            # UI Update
            def _update():
                if not self.winfo_exists(): return
                
                try:
                    # Identity
                    code = stats.get("code", "Generate Now")
                    if code == "Generate Now" and hasattr(self.controller, 'affiliate_service'): 
                        try:
                            code = self.controller.affiliate_service.generate_my_code() or "ERR"
                        except: code = "ERR-GEN"
                    
                    self.lbl_code.configure(text=code)
                    self.my_ref_code = code
                    
                    tier_info = stats.get("tier_info", {})
                    t_name = tier_info.get("name", "STARTER")
                    t_color = tier_info.get("color", "#aaaaaa")
                    self.lbl_tier_badge.configure(text=f"{t_name} AGENT", text_color=t_color)
                    
                    # ADMIN OVERRIDE: Show special badge
                    if hasattr(self.controller, 'db_manager') and self.controller.db_manager.is_admin():
                        self.lbl_tier_badge.configure(text="⚡ SYSTEM ADMIN", text_color="#FF4444")
                    
                    count = stats.get("count", 0)
                    next_t = tier_info.get("next", 100)
                    if next_t:
                        self.progress_bar.set(min(count/next_t, 1.0))
                        self.lbl_next_goal.configure(text=f"Next: {count}/{next_t}")
                    else:
                        self.progress_bar.set(1.0)
                        self.lbl_next_goal.configure(text="MAX RANK REACHED")

                    # Wallet
                    self.card_active.lbl_val.configure(text=format_currency(wallet.get('balance_active', 0)))
                    self.card_pending.lbl_val.configure(text=format_currency(wallet.get('balance_pending', 0)))
                    self.card_total.lbl_val.configure(text=format_currency(wallet.get('total_earned', 0)))
                    
                    # Matrix State (New)
                    try:
                        self._update_matrix_state(profile, count)
                    except Exception as e:
                        print(f"Matrix Update Error: {e}")
                    
                    # Logs
                    logs = []
                    try:
                         if hasattr(self.controller, 'db_manager'):
                            logs = self.controller.db_manager.get_referral_logs(limit=20)
                    except: pass
                    self._render_logs(logs)
                    
                except Exception as e:
                    print(f"UI UPDATE ERROR: {e}")
                    import traceback
                    traceback.print_exc()

            if hasattr(self.controller, 'safe_ui_update'):
                self.controller.safe_ui_update(_update)
            else:
                self.after(0, _update)
            
        threading.Thread(target=_task, daemon=True).start()

    def _update_matrix_state(self, profile, ref_count):
        """
        Updates Matrix Buttons & Expiry based on User Tier & Date.
        """
        # ADMIN OVERRIDE: Admin = INSTITUTIONAL + LIFETIME
        if hasattr(self.controller, 'db_manager') and self.controller.db_manager.is_admin():
            sub_tier = "institutional"
            sub_expiry = None  # Will be treated as LIFETIME
        else:
            sub_tier = profile.get("subscription_tier", "free").lower() if profile else "free"
            # CORRECT COLUMN: 'premium_until' (Supabase)
            sub_expiry = profile.get("premium_until")
        
        # Map sub_tier to matrix thresholds/names for comparison
        tier_map = {"free": 0, "standard": 0, "gold": 10, "platinum": 50, "institutional": 100}
        user_level = tier_map.get(sub_tier, 0)
        
        for name, row_data in self.tier_rows.items():
            # row_data: {idx, status, action, expiry, data}
            # data: (name, req, comm, bonus, col, thres)
            thres = row_data["data"][5]
            
            # EXPIRY LOGIC
            expiry_text = "-"
            
            # STARTER / FREE LOGIC: Always Active Lifetime if level is 0
            if thres == 0:
                 if user_level == 0:
                     expiry_text = "LIFETIME"
                 elif user_level > 0:
                     expiry_text = "COMPLETED"

            # HIGHER TIERS LOGIC
            elif thres == user_level: 
                # -------------------------------------------------------------
                # 🛡️ SELF-HEALING PROTOCOL: MISSING EXPIRY DATE
                # If User is Paid Tier (Gold+) but expiry is NULL -> Auto-Fix
                # -------------------------------------------------------------
                if not sub_expiry and sub_tier in ["gold", "platinum", "institutional", "titan"]:
                    try:
                        from datetime import datetime, timedelta
                        # 1. Calculate New Expiry (Today + 30 Days)
                        now = datetime.now()
                        new_expiry = now + timedelta(days=30)
                        iso_expiry = new_expiry.isoformat()
                        
                        # 2. Update Local Display IMMEDIATELY
                        expiry_text = "ACTIVE (Restored)"
                        sub_expiry = iso_expiry # Update local var for next loop
                        
                        # 3. Spawn Thread to Persist to DB (Don't block UI)
                        def _heal_db():
                            print(f"// SELF-HEALING: Fixing missing expiry for {sub_tier} user...")
                            if hasattr(self.controller, 'db_manager'):
                                # CORRECT COLUMN IS 'premium_until'
                                self.controller.db_manager.update_user_profile({"premium_until": iso_expiry})
                                
                        threading.Thread(target=_heal_db, daemon=True).start()
                        
                    except Exception as e:
                        print(f"// Self-Healing Error: {e}")
                        expiry_text = "MONTHLY ACCESS"

                elif sub_expiry:
                    from datetime import datetime
                    try:
                        # Parse ISO format (Supabase default) with dateutil for robustness
                        try:
                            from dateutil import parser
                            exp_dt = parser.isoparse(sub_expiry)
                        except ImportError:
                            # Fallback manually if needed
                            exp_str = sub_expiry.replace("Z", "+00:00")
                             # Pad micros if needed (simplified fallback)
                            if "." in exp_str and "+" in exp_str:
                                head, tail = exp_str.split(".")
                                micros, tz = tail.split("+")
                                if len(micros) < 6:
                                    micros = micros.ljust(6, "0")
                                exp_str = f"{head}.{micros}+{tz}"
                            exp_dt = datetime.fromisoformat(exp_str)

                        # Simplified visual calculation
                        now = datetime.now(exp_dt.tzinfo) if exp_dt.tzinfo else datetime.now()
                        diff = exp_dt.date() - now.date()
                        days = diff.days
                        
                        if days > 3650: # Cap at 10 years for lifetime check
                            expiry_text = "LIFETIME"
                        elif days > 30:
                            expiry_text = f"{days // 30} MO LEFT"
                        elif days > 0:
                            expiry_text = f"{days} DAYS LEFT"
                        else:
                            expiry_text = "EXPIRED"
                    except Exception as e:
                        print(f"// Dashboard Date Error: {e}")
                        expiry_text = "Active"
                elif sub_tier in ["institutional", "titan", "lifetime"]:
                     expiry_text = "LIFETIME"
            
            row_data["expiry"].configure(text=expiry_text)

            # BUTTON LOGIC
            btn = row_data["action"]
            lbl = row_data["status"]
            
            # ACTIVE LOGIC: Matches level OR is Starter (0) when user is Free
            is_active_tier = (thres == user_level)
            
            if is_active_tier:
                # CURRENT TIER
                lbl.configure(text="✅ ACTIVE", text_color="#00FFAA")
                btn.configure(text="🚀 BOOST", state="normal", fg_color="#00FFAA", text_color="black",
                              command=lambda: self._show_boost_overlay())
            
            elif thres < user_level:
                # LOWER TIER / PASSED
                lbl.configure(text="PASSED", text_color="gray") 
                btn.configure(text="DONE", state="disabled", fg_color="transparent", text_color="#555")
            
            else:
                # HIGHER TIER / LOCKED
                lbl.configure(text="🔒 LOCKED", text_color="#444")
                btn.configure(text="UPGRADE ⇪", state="normal", fg_color="#FFD700", text_color="black",
                              command=lambda: self.controller.show_page("upgrade"))

    def _render_logs(self, logs):
        for w in self.log_scroll.winfo_children(): w.destroy()
        
        if not logs:
            # Motivational empty state — NO fake ghost data
            ctk.CTkLabel(self.log_scroll, text="⚡ START YOUR MISSION", 
                         font=("Roboto", 13, "bold"), text_color="#E5E4E2").pack(pady=(20, 5))
            ctk.CTkLabel(self.log_scroll, text="Invite friends to see real activity here!\nYour referral earnings will appear in this feed.",
                         font=("Segoe UI", 10), text_color="#666", justify="center").pack(pady=(0, 10))
            ctk.CTkButton(self.log_scroll, text="🚀 LAUNCH CAMPAIGN", height=32, fg_color="#00FFAA", text_color="black",
                          font=("Segoe UI Bold", 10), hover_color="#00DD99",
                          command=lambda: self._show_boost_overlay()).pack(pady=(5, 15))
            return

        for l in logs:
            r = ctk.CTkFrame(self.log_scroll, fg_color="#18181B", height=28, corner_radius=4)
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=f"{l.get('email', 'User')[:10]}..", font=("Consolas", 10, "bold"), text_color="#ccc").pack(side="left", padx=10)
            ctk.CTkLabel(r, text=f"+ {format_currency(l.get('amount', 0))}", font=("Segoe UI Bold", 10), text_color="#00FFAA").pack(side="right", padx=10)
