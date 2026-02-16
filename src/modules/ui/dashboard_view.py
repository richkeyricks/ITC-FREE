import os
import threading
import random
import webbrowser
from datetime import datetime
import customtkinter as ctk
from PIL import Image, ImageTk
from ui_theme import THEME_DARK, FONTS
from utils.tooltips import CTkToolTip

class DashboardView:
    """
    Modular class for the Dashboard page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent, progress_callback=None):
        """Builds the Dashboard page with Premium Overhaul."""
        theme = parent.theme_data if hasattr(parent, 'theme_data') else THEME_DARK
        
        def _report(percent, text):
            if progress_callback:
                progress_callback(percent, text)
        
        # Standardize padding for the scroll frame
        page = ctk.CTkScrollableFrame(parent.main_container, fg_color="transparent")
        
        # --- PERSONAL GREETING ---
        _report(60, "Drawing Personal Hub...")
        greeting_row = ctk.CTkFrame(page, fg_color="transparent", height=40)
        greeting_row.pack(fill="x", pady=(0, 10))
        greeting_row.pack_propagate(False)
        
        hour = datetime.now().hour
        user_name = os.getenv("USER_NAME", "")
        if not user_name or user_name.lower() == "trader":
            email = os.getenv("USER_EMAIL", "")
            if "@" in email:
                user_name = email.split("@")[0].replace(".", " ").title()
        
        if 4 <= hour < 11: greet = parent.translator.get("dash_greet_morning")
        elif 11 <= hour < 15: greet = parent.translator.get("dash_greet_afternoon")
        elif 15 <= hour < 19: greet = parent.translator.get("dash_greet_evening")
        else: greet = parent.translator.get("dash_greet_night")
        
        full_greet = parent.translator.get("dash_greet_user").format(greet=greet, user=user_name)
        
        # Wrapper for centering Greeting + Badge
        greet_wrapper = ctk.CTkFrame(greeting_row, fg_color="transparent")
        greet_wrapper.place(relx=0.5, rely=0.5, anchor="center", x=-110)

        parent.lbl_greeting = ctk.CTkLabel(greet_wrapper, text=full_greet, 
                                         font=("Segoe UI Bold", 20), text_color=theme["accent_success"])
        parent.lbl_greeting.pack(side="left")

        # Add User Level Badge
        parent.badge_frame = DashboardView._create_user_badge(greet_wrapper, parent, theme)
        parent.badge_frame.pack(side="left", padx=(10, 0))

        # Async AI Gender Check
        def _ai_gender_check():
            def update_safe():
                try:
                    if not hasattr(parent, 'lbl_greeting') or not parent.lbl_greeting.winfo_exists(): return
                    final_name = f"{user_name}"
                    new_text = parent.translator.get("dash_greet_user").format(greet=greet, user=final_name)
                    parent.lbl_greeting.configure(text=new_text)
                except: pass

            # Thread Safety: Move existence check and update to Main Thread
            if hasattr(parent, 'safe_ui_update'):
                parent.safe_ui_update(update_safe)
            else:
                parent.after(100, update_safe)

        threading.Thread(target=_ai_gender_check, daemon=True).start()

        # --- COMPACT STATUS ROW ---
        status_row = ctk.CTkFrame(page, fg_color="transparent", height=35)
        status_row.pack(fill="x", pady=(0, 5))
        status_row.pack_propagate(False)

        status_center = ctk.CTkFrame(status_row, fg_color="transparent")
        status_center.place(relx=0.5, rely=0.5, anchor="center", x=-110)
        
        _report(70, "Synchronizing Status Nodes...")
        parent.card_net = DashboardView._create_status_bar(status_center, "🌐", parent.translator.get("badge_internet"), parent.translator.get("status_online"), theme)
        parent.card_tg = DashboardView._create_status_bar(status_center, "📨", parent.translator.get("badge_telegram"), parent.translator.get("status_disconnected"), theme)
        parent.card_mt5 = DashboardView._create_status_bar(status_center, "📈", parent.translator.get("badge_mt5"), parent.translator.get("status_offline"), theme)

        # --- AI WELLNESS TOAST ---
        _report(80, "Awakening AI Wellness...")
        wellness_frame = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=15, height=45, border_width=1, border_color="#30363d")
        wellness_frame.pack(fill="x", pady=(0, 15), padx=10)
        wellness_frame.pack_propagate(False)
        
        wellness_msgs = [
            parent.translator.get("dash_ai_msg1").format(user=user_name),
            parent.translator.get("dash_ai_msg2").format(user=user_name),
            parent.translator.get("dash_ai_msg3").format(user=user_name),
            parent.translator.get("dash_ai_msg4").format(user=user_name),
            parent.translator.get("dash_ai_msg5").format(user=user_name)
        ]
        
        ctk.CTkLabel(wellness_frame, text="🤖", font=("Segoe UI", 16)).pack(side="left", padx=(15, 10))
        ctk.CTkLabel(wellness_frame, text=random.choice(wellness_msgs), font=("Segoe UI", 11), text_color=theme["text_primary"]).pack(side="left")
        
        def _close_well(): wellness_frame.destroy()
        
        ctk.CTkButton(wellness_frame, text=parent.translator.get("dash_ai_yes"), width=60, height=24, font=("Segoe UI Bold", 9),
                      fg_color=theme["accent_success"], command=_close_well).pack(side="right", padx=15)
        ctk.CTkButton(wellness_frame, text=parent.translator.get("dash_ai_no"), width=60, height=24, font=("Segoe UI Bold", 9),
                      fg_color=theme["bg_tertiary"], command=_close_well).pack(side="right")

        # --- DUAL-COLOR METER ---
        DashboardView._create_dual_meter(page, parent, theme)

        # --- PREMIUM FINANCIAL CARDS ---
        _report(90, "Generating Premium Glass Cards...")
        balance_row = ctk.CTkFrame(page, fg_color="transparent", height=155)
        balance_row.pack(fill="x", pady=(0, 15))
        balance_row.pack_propagate(False)
        
        parent.card_balance = DashboardView._create_premium_card(balance_row, parent.translator.get("dash_balance"), "$0.00", theme, "blue", "card_bg_balance.png", "icon_balance.png")
        parent.card_equity = DashboardView._create_premium_card(balance_row, parent.translator.get("dash_equity"), "$0.00", theme, "cyan", "card_bg_equity.png", "icon_equity.png")
        parent.card_pnl = DashboardView._create_premium_card(balance_row, parent.translator.get("dash_live_pnl"), "$0.00", theme, "green", "card_bg_livepnl.png", "icon_livepnl.png")
        parent.card_loss = DashboardView._create_premium_card(balance_row, parent.translator.get("dash_total_pnl"), "$0.00", theme, "purple", "card_bg_totalpnl.png", "icon_totalpnl.png")

        # --- QUICK GUIDE & SYSTEM TOOLS ---
        _report(95, "Finalizing Infrastructure Gateway...")
        DashboardView._build_bottom_sections(page, parent, theme)
        
        _report(100, "Dashboard Optimized & Ready.")
        parent.log("INFO", parent.translator.get("dash_system_ready"))
        return page


    @staticmethod
    def _create_user_badge(container, parent, theme):
        """Creates a premium membership badge for the dashboard."""
        badge_holder = ctk.CTkFrame(container, fg_color="transparent")
        
        tier = "FREE"
        color = "#9CA3AF" # Gray
        label_key = "tier_free"
        cycle_suffix = ""

        if hasattr(parent, 'db_manager') and parent.db_manager:
            dm = parent.db_manager
            # Fetch profile once
            profile = dm.get_user_profile() or {}
            sub_tier = dm.get_user_tier(profile)
            is_admin = dm.is_admin()
            
            # Get cycle info using centralized logic
            cycle = dm.get_user_cycle(profile)
            cycle_text = parent.translator.get(f"cycle_{cycle.lower()}", cycle)

            if is_admin:
                color = "#FF4444"
                label_key = "tier_admin"
            elif sub_tier == "INSTITUTIONAL":
                color = "#DC143C"  # Crimson
                label_key = "tier_institutional"
                cycle_suffix = f" • {cycle_text}"
            elif sub_tier == "PLATINUM":
                color = "#00BFFF"  # Deep Sky Blue
                label_key = "tier_platinum"
                cycle_suffix = f" • {cycle_text}"
            elif sub_tier in ["GOLD", "PRO"]:
                color = "#FFD700"  # Gold
                label_key = "tier_gold"
                cycle_suffix = f" • {cycle_text}"
            else:
                color = "#9CA3AF"
                label_key = "tier_free"

        label_text = parent.translator.get(label_key) + cycle_suffix
        
        # Premium Styled Badge (Glassmorphism inspired)
        inner_frame = ctk.CTkFrame(badge_holder, fg_color="#1a1d21", border_width=1, border_color=color, corner_radius=8)
        inner_frame.pack(side="left")
        
        lbl = ctk.CTkLabel(inner_frame, text=label_text, font=("Segoe UI Black", 10), text_color=color)
        lbl.pack(padx=8, pady=2)
        
        return badge_holder

    @staticmethod
    def _create_status_bar(container, icon, title, status, theme):
        """Creates a slim, professional status indicator bar."""
        frame = ctk.CTkFrame(container, fg_color=theme["bg_secondary"], corner_radius=15, height=28)
        frame.pack(side="left", padx=8)
        
        ctk.CTkLabel(frame, text=icon, font=("Segoe UI", 12)).pack(side="left", padx=(10, 5))
        ctk.CTkLabel(frame, text=title, font=("Segoe UI Bold", 9), text_color=theme["text_secondary"]).pack(side="left", padx=(0, 5))
        
        lbl_status = ctk.CTkLabel(frame, text=f"• {status}", font=("Segoe UI Bold", 9), text_color=theme["status_error"])
        lbl_status.pack(side="left", padx=(0, 10))
        
        return lbl_status

    @staticmethod
    def _create_premium_card(container, label, value, theme, glow_type="blue", bg_filename="card_bg_glow.png", icon_filename="icon_balance.png"):
        """Ultra-premium glass card."""
        pil_bg = None
        icon_img = None
        try:
            from utils.path_helper import resource_path
            
            bg_path = resource_path(f"assets/{bg_filename}")
            if bg_path and os.path.exists(bg_path):
                pil_bg = Image.open(bg_path)
            
            icon_path = resource_path(f"assets/{icon_filename}")
            if icon_path and os.path.exists(icon_path):
                icon_img = Image.open(icon_path)
        except Exception as e:
            print(f"Premium Card Asset Error: {e}")

        glow_color = {"blue": "#3b82f6", "cyan": "#06b6d4", "green": "#10b981", "purple": "#a855f7"}.get(glow_type, "#3b82f6")

        card = ctk.CTkFrame(container, fg_color="#0b0e14", corner_radius=15, border_width=1, border_color="#30363d")
        card.pack(side="left", expand=True, fill="both", padx=6)
        card.pack_propagate(False)

        canvas = card._canvas
        card.pil_bg = pil_bg
        card.icon_pil = icon_img
        card.glow_color = glow_color
        card.current_value = value
        card.label_text = label

        def redraw(event=None):
            w = card.winfo_width(); h = card.winfo_height()
            if w < 20 or h < 20: return
            canvas.delete("all")
            if card.pil_bg:
                try:
                    res_bg = card.pil_bg.resize((w, h), Image.Resampling.LANCZOS)
                    card.bg_tk = ImageTk.PhotoImage(res_bg)
                    canvas.create_image(0, 0, image=card.bg_tk, anchor="nw")
                except: pass
            if card.icon_pil:
                try:
                    res_icon = card.icon_pil.resize((44, 44), Image.Resampling.LANCZOS)
                    card.icon_tk = ImageTk.PhotoImage(res_icon)
                    canvas.create_image(42, 42, image=card.icon_tk, anchor="center")
                except: pass
            shadow_col = "#000000"
            canvas.create_text(79, 33, text=card.label_text, font=("Segoe UI", 11), fill=shadow_col, anchor="w") 
            canvas.create_text(78, 32, text=card.label_text, font=("Segoe UI", 11), fill="#94a3b8", anchor="w") 
            canvas.create_text(80, 62, text=card.current_value, font=("Segoe UI", 26, "bold"), fill=shadow_col, anchor="w") 
            canvas.create_text(79, 61, text=card.current_value, font=("Segoe UI", 26, "bold"), fill=shadow_col, anchor="w")
            card.v_shadow_id = canvas.create_text(78, 60, text=card.current_value, font=("Segoe UI", 26, "bold"), fill=shadow_col, anchor="w")
            card.v_main_id = canvas.create_text(77, 59, text=card.current_value, font=("Segoe UI", 26, "bold"), fill="white", anchor="w")
            for i in range(4):
                dot_col = card.glow_color if i == 0 else "#2d333b"
                canvas.create_rectangle(20 + (i*10), 105, 26 + (i*10), 111, fill=dot_col, outline="")
            canvas.create_rectangle(0, h-3, w, h-1, fill=card.glow_color, outline="")

        card.bind("<Configure>", redraw)

        class CanvasValueProxy:
            def __init__(self, c_obj, can):
                self.c_obj = c_obj; self.can = can
            def configure(self, text=None, **kwargs):
                if text is not None:
                    self.c_obj.current_value = text
                    if hasattr(self.c_obj, 'v_main_id'):
                        try:
                            self.can.itemconfig(self.c_obj.v_main_id, text=text)
                            self.can.itemconfig(self.c_obj.v_shadow_id, text=text)
                        except: pass
            def winfo_exists(self): return True

        return CanvasValueProxy(card, canvas)

    @staticmethod
    def _create_dual_meter(container, parent, theme):
        """Creates a custom high-performance progress bar."""
        frame = ctk.CTkFrame(container, fg_color=theme["bg_secondary"], corner_radius=12, height=45)
        frame.pack(fill="x", pady=(0, 15))
        frame.pack_propagate(False)

        canvas = ctk.CTkCanvas(frame, bg=theme["bg_secondary"], highlightthickness=0, height=45)
        canvas.pack(fill="both", expand=True)

        class MeterProxy:
            def __init__(self, can, p, t):
                self.can = can; self.parent = p; self.theme = t
                self.val = 0.0
                self.can.bind("<Configure>", self.draw)
            def set(self, val):
                self.val = max(0, min(100, val)); self.draw()
            def draw(self, event=None):
                w = self.can.winfo_width(); h = self.can.winfo_height()
                if w < 50: return
                self.can.delete("all")
                self.can.create_rectangle(10, 10, w-10, 35, fill="#1c2128", outline="#30363d", width=1)
                fill_w = (w-20) * (self.val / 100.0)
                color = "#10b981" if self.val > 0 else "#ef4444" 
                self.can.create_rectangle(11, 11, 11 + fill_w, 34, fill=color, outline="")
                title = self.parent.translator.get("dash_daily_meter")
                self.can.create_text(w/2, 22, text=f"{title} {self.val:.0f}%", font=("Segoe UI Bold", 10), fill="white")

        proxy = MeterProxy(canvas, parent, theme)
        parent.meter = proxy
        return frame

    @staticmethod
    def _build_bottom_sections(page, parent, theme):
        """Helper to build the rest of the dashboard sections."""
        guide_frame = ctk.CTkFrame(page, fg_color="transparent")
        guide_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(guide_frame, text=parent.translator.get("dash_quick_start"), font=("Segoe UI Bold", 12)).pack(anchor="w", pady=(0, 5))
        steps_container = ctk.CTkFrame(guide_frame, fg_color=theme["bg_secondary"], corner_radius=12, border_width=1, border_color="#30363d")
        steps_container.pack(fill="x")
        # --- NEW QUICK START STEPPER ---
        from modules.ui.ui_components import QuickStartStepper, STEP_PENDING, STEP_ACTIVE, STEP_COMPLETED
        
        steps_data = [
            {"label": parent.translator.get("dash_step_tg"), "page": "telegram", "state": STEP_PENDING},
            {"label": parent.translator.get("dash_step_mt5"), "page": "mt5", "state": STEP_PENDING},
            {"label": parent.translator.get("dash_step_mode"), "page": "trading", "state": STEP_PENDING},
            {"label": parent.translator.get("dash_step_status"), "page": "dashboard", "state": STEP_COMPLETED}, # Step 4 always 'checked'
        ]
        
        parent.stepper = QuickStartStepper(steps_container, steps_data, callback=parent.show_page)
        parent.stepper.pack(fill="x", padx=10, pady=10)
        
        # Make stepper steps clickable
        def _on_step_click(page_id): parent.show_page(page_id)
        # Note: Canvas clicks are handled internally or we can wrap circles in invisible buttons.
        # For now, let's keep it simple and just show progress.

        infra_frame = ctk.CTkFrame(page, fg_color="transparent")
        infra_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(infra_frame, text=parent.translator.get("dash_infra_title"), font=FONTS["body_bold"], text_color="white").pack(anchor="w", pady=(0, 5))
        infra_grid = ctk.CTkFrame(infra_frame, fg_color="transparent")
        infra_grid.pack(fill="x")
        def go_broker(): parent.show_page("broker")
        def go_vps(): parent.show_page("vps")
        c1 = ctk.CTkFrame(infra_grid, fg_color="#1c1c16", corner_radius=12, border_width=1, border_color="#f59e0b")
        c1.pack(side="left", fill="both", expand=True, padx=(0, 10))
        c1_inner = ctk.CTkFrame(c1, fg_color="transparent")
        c1_inner.pack(padx=15, pady=12, fill="both")
        ctk.CTkLabel(c1_inner, text=parent.translator.get("dash_broker_title"), font=("Segoe UI Bold", 13), text_color="#f59e0b").pack(anchor="w")
        ctk.CTkLabel(c1_inner, text=parent.translator.get("dash_broker_desc"), font=("Segoe UI", 11), text_color="gray").pack(anchor="w", pady=(2, 8))
        ctk.CTkButton(c1_inner, text=parent.translator.get("dash_broker_btn"), height=28, fg_color="#f59e0b", hover_color="#d97706", text_color="black", command=go_broker).pack(fill="x")
        c2 = ctk.CTkFrame(infra_grid, fg_color="#0d1b2a", corner_radius=12, border_width=1, border_color="#3498db")
        c2.pack(side="left", fill="both", expand=True)
        c2_inner = ctk.CTkFrame(c2, fg_color="transparent")
        c2_inner.pack(padx=15, pady=12, fill="both")
        ctk.CTkLabel(c2_inner, text=parent.translator.get("dash_vps_title"), font=("Segoe UI Bold", 13), text_color="#3498db").pack(anchor="w")
        ctk.CTkLabel(c2_inner, text=parent.translator.get("dash_vps_desc"), font=("Segoe UI", 11), text_color="gray").pack(anchor="w", pady=(2, 8))
        ctk.CTkButton(c2_inner, text=parent.translator.get("dash_vps_btn"), height=28, fg_color="#3498db", hover_color="#2980b9", text_color="white", command=go_vps).pack(fill="x")

        btn_row = ctk.CTkFrame(page, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 15))
        parent.btn_start = ctk.CTkButton(btn_row, text=parent.translator.get("dash_start"), font=("Segoe UI Semibold", 14),
                                        fg_color=theme["btn_primary_bg"], hover_color=theme["btn_primary_hover"], height=48, corner_radius=10, command=parent.start_copier)
        parent.btn_start.pack(side="left", expand=True, fill="x", padx=(0, 10))
        CTkToolTip(parent.btn_start, parent.translator.get("hint_start"))
        parent.btn_cloud = ctk.CTkButton(btn_row, text=parent.translator.get("dash_cloud"), font=("Segoe UI Semibold", 14),
                                        fg_color="#a855f7", hover_color="#9333ea", height=48, corner_radius=10, 
                                        command=lambda: webbrowser.open(os.getenv("WEB_DASHBOARD_URL", "https://telegramcopytrade.vercel.app/webmonitor")))
        parent.btn_cloud.pack(side="left", expand=True, fill="x", padx=(0, 10))
        CTkToolTip(parent.btn_cloud, parent.translator.get("hint_cloud"))
        parent.btn_emergency = ctk.CTkButton(btn_row, text=parent.translator.get("dash_emergency"), font=("Segoe UI Semibold", 14),
                                            fg_color=theme["btn_danger_bg"], hover_color=theme["btn_danger_hover"], height=48, corner_radius=10, command=parent.emergency_close)
        parent.btn_emergency.pack(side="left", expand=True, fill="x")
        CTkToolTip(parent.btn_emergency, parent.translator.get("hint_emergency"))

        logs_header = ctk.CTkFrame(page, fg_color="transparent")
        logs_header.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(logs_header, text=parent.translator.get("dash_logs"), font=FONTS["section_header"], text_color=theme["text_secondary"]).pack(side="left")
        ctk.CTkButton(logs_header, text=parent.translator.get("dash_clear"), width=100, height=28, font=FONTS["body_small"],
                      fg_color=theme["bg_tertiary"], command=lambda: parent.clear_logs()).pack(side="right")
        parent.btn_clear = list(logs_header.winfo_children())[-1]
        CTkToolTip(parent.btn_clear, parent.translator.get("hint_clear"))
        parent.log_box = ctk.CTkTextbox(page, height=120, font=FONTS["log"], fg_color=theme["bg_secondary"], corner_radius=8, text_color=theme["text_primary"])
        parent.log_box.pack(fill="x")
