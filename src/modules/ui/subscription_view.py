import customtkinter as ctk
from PIL import Image
import os
import random
from modules.logic.gamification_service import GamificationService
from CTkMessagebox import CTkMessagebox
from configs.pricing_config import PRICING_MATRIX, CYCLES, TIER_ORDER

class SubscriptionView:
    """
    Premium Upgrade Screen ("The Quantum Pricing Engine").
    Features Dynamic Cycle Switcher, 4-Tier Matrix, and Scarcity Psychology.
    """
    
    # State for the Cycle Switcher
    current_cycle = "YEARLY" # Default to Yearly (Decoy)
    
    @staticmethod
    def build(parent):
        # Initialize Gamification Service
        g_service = GamificationService(parent.db_manager)
        parent.g_service = g_service 
        
        # User Data
        balance = g_service.get_user_balance()
        parent.user_coins = balance["coins"]
        parent.premium_until = balance["until"]
        
        # --- THEME ---
        BG_COLOR = "#09090b" # Zinc 950 (Vantablack-ish)
        
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else {}
        
        # Main Scrollable Container
        main_frame = ctk.CTkScrollableFrame(parent.main_container, fg_color=BG_COLOR,
                                           scrollbar_button_color=theme.get("scrollbar_button_color", "#2f80ed"),
                                           scrollbar_button_hover_color=theme.get("scrollbar_button_hover_color", "#00d2ff"))
        # REMOVED REDUNDANT PACK: main_frame.pack(fill="both", expand=True) (Handled by gui.py)

        # --- HERO HEADER ---
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(pady=(30, 20))
        
        ctk.CTkLabel(header_frame, text="QUANTUM ACCESS", 
                     font=("Segoe UI Black", 36), text_color="white").pack()
        
        ctk.CTkLabel(header_frame, text="Unlock the same tools used by Institutional Whales.", 
                     font=("Segoe UI", 16), text_color="#a1a1aa").pack(pady=(5, 0))

        # --- CYCLE SWITCHER (The Decoy Engine) ---
        switcher_frame = ctk.CTkFrame(main_frame, fg_color="#18181b", corner_radius=20, border_width=1, border_color="#27272a")
        switcher_frame.pack(pady=(0, 25))
        
        # Switcher Buttons
        parent.sub_switcher_btns = {}
        for cycle_key, cycle_data in CYCLES.items():
            is_active = (cycle_key == SubscriptionView.current_cycle)
            btn_color = "#3b82f6" if is_active else "transparent"
            text_color = "white" if is_active else "#71717a"
            
            label_text = cycle_data['label']
            if cycle_data['discount']:
                label_text += f"\n({cycle_data['discount']})"
            
            btn = ctk.CTkButton(switcher_frame, text=label_text, 
                                font=("Segoe UI Bold", 13),
                                fg_color=btn_color, hover_color="#2563eb",
                                text_color=text_color,
                                width=140, height=50, corner_radius=15,
                                command=lambda c=cycle_key: SubscriptionView._set_cycle(parent, c))
            btn.pack(side="left", padx=5, pady=5)
            parent.sub_switcher_btns[cycle_key] = btn

        # --- CARDS CONTAINER (Dynamic Grid) ---
        # Using a Frame to hold cards side-by-side. 
        # Since we have 4 cards, we might need a grid or flexible packing.
        cards_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_container.pack(pady=10) # Removed fill="x" to allow clustering in center
        
        # Store Reference for Updates
        parent.sub_cards_container = cards_container
        
        # Render Initial Cards
        SubscriptionView._render_cards(cards_container, SubscriptionView.current_cycle, parent)

        # --- FOOTER ---
        ctk.CTkLabel(main_frame, text="Secure Payment via Midtrans (QRIS, VA, CC) • Cancel Anytime", 
                     font=("Segoe UI", 12), text_color="#52525b").pack(pady=(40, 10))
                     
        # Coin Balance (Subtle)
        ctk.CTkLabel(main_frame, text=f"💎 ITC COIN BALANCE: {parent.user_coins}", 
                     font=("Segoe UI Bold", 12), text_color="#3f3f46").pack(pady=(0, 40))

        # --- FIX FOR INITIAL LAYOUT GLITCH ---
        # Force update and reset scroll to top to prevent "black void" issue
        main_frame.update_idletasks()
        parent.after(150, lambda: main_frame._parent_canvas.yview_moveto(0.0))

        return main_frame

    @staticmethod
    def _render_cards(container, cycle, parent_ctx):
        """Renders the pricing cards into the container."""
        # Clear existing
        for widget in container.winfo_children():
            widget.destroy()

        # Dynamic Render of Tiers
        for tier_key in TIER_ORDER:
            tier_data = PRICING_MATRIX[tier_key]
            
            # Skip Lifetime if not applicable (Institutional) AND Lifetime selected
            if cycle == "LIFETIME" and tier_data['prices']['LIFETIME'] is None:
                continue

            SubscriptionView.create_dynamic_card(
                container,
                tier_key,
                tier_data,
                cycle,
                parent_ctx
            )

    @staticmethod
    def _set_cycle(parent, cycle):
        """Updates cycle state and redraws cards WITHOUT reloading page (In-Place Update)"""
        SubscriptionView.current_cycle = cycle
        
        # 1. Update Buttons Visual State
        if hasattr(parent, 'sub_switcher_btns'):
            for btn_cycle, btn in parent.sub_switcher_btns.items():
                is_active = (btn_cycle == cycle)
                btn_color = "#3b82f6" if is_active else "transparent"
                text_color = "white" if is_active else "#71717a"
                btn.configure(fg_color=btn_color, text_color=text_color)
        
        # 2. Re-render Cards
        if hasattr(parent, 'sub_cards_container') and parent.sub_cards_container.winfo_exists():
            SubscriptionView._render_cards(parent.sub_cards_container, cycle, parent)

    @staticmethod
    def create_dynamic_card(parent, tier_key, data, cycle, parent_ctx):
        """Creates a card based on Matrix Data + Scarcity Logic"""
        
        # Determine Prices
        usd_price = data['prices'][cycle]
        idr_price = data['idr_prices'][cycle]
        
        price_display = "FREE"
        sub_price_display = ""
        
        if cycle == "LIFETIME" and usd_price == "CONTRACT ONLY":
             price_display = "CONTRACT"
             sub_price_display = "(Contact Sales)"
        elif usd_price != 0 and usd_price is not None:
            price_display = f"${usd_price}"
            suffix = "/mo" if cycle == "MONTHLY" else "/yr" if cycle == "YEARLY" else ""
            if cycle == "LIFETIME": suffix = ""
            price_display += suffix
            sub_price_display = f"({idr_price})"
        else:
            # Free or Contract
            if usd_price == 0:
                price_display = "FREE"
                sub_price_display = "FOREVER"
        
        # --- CARD STRUCTURE ---
        # Glow Frame - Fix: corner_radius > 0 requires a solid color to prevent crash
        # For 'transparent' (Standard), we use a very dark gray to mimic the BG but allow rounding
        glow_color = data['glow_color'] if data['glow_color'] else "#0f172a" 
        glow_radius = 22
        
        glow_frame = ctk.CTkFrame(parent, fg_color=glow_color, corner_radius=glow_radius)
        glow_frame.pack(side="left", padx=10, pady=10, fill="y")
        
        # Inner Card
        card = ctk.CTkFrame(glow_frame, fg_color="#18181b", width=260, height=580, corner_radius=20, border_width=2, border_color=data['color'])
        card.pack(padx=2, pady=2, fill="both", expand=True)
        card.pack_propagate(False) # Strict sizing
        
        # --- SCARCITY BADGE (The Genesis Protocol) ---
        if data.get('scarcity_enabled'):
            badge_text = data.get('badge_text', 'LIMITED')
            scarcity_type = data.get('scarcity_type', 'FLASH')
            
            # Randomize slots for FOMO (1-4)
            slots_left = random.randint(1, 4)
            
            badge_color = "#dc2626" if scarcity_type == "FLASH" else "#000000" # Red or Black
            text_col = "white" if scarcity_type == "FLASH" else data['color']
            
            # Fix: border_color="transparent" is not allowed if border_width > 0
            if scarcity_type == "FLASH":
                border_col = "#dc2626" # Match background for flash
                b_width = 0
            else:
                border_col = data['color']
                b_width = 1
            
            if scarcity_type == "FOUNDER":
                slots_left = 1 # Founder usually very limited
            
            badge = ctk.CTkButton(card, text=f"🔴 {badge_text}: {slots_left} LEFT", 
                                  fg_color=badge_color, hover_color=badge_color,
                                  border_width=b_width, border_color=border_col,
                                  text_color=text_col, font=("Segoe UI Bold", 10), height=24, corner_radius=12)
            badge.pack(pady=(15, 0), padx=20)
        else:
            # GHOST SPACER (Frame) to maintain vertical alignment with badge-holding cards
            ctk.CTkFrame(card, height=24, fg_color="transparent").pack(pady=(15, 0))
            
        # --- HEADER ---
        ctk.CTkLabel(card, text=data['display_name'], font=("Segoe UI Black", 20), text_color=data['color']).pack(pady=(10, 0))
        ctk.CTkLabel(card, text=data['tagline'], font=("Segoe UI Italic", 12), text_color="gray").pack(pady=(0, 15))
        
        # --- PRICE ---
        ctk.CTkLabel(card, text=price_display, font=("Segoe UI Black", 28), text_color="white").pack()
        if sub_price_display:
            ctk.CTkLabel(card, text=sub_price_display, font=("Segoe UI", 13), text_color="gray").pack(pady=(0, 10))
            
        # Divider
        ctk.CTkFrame(card, height=2, fg_color="#27272a").pack(fill="x", padx=15, pady=15)
        
        # --- FEATURES ---
        feat_frame = ctk.CTkFrame(card, fg_color="transparent")
        feat_frame.pack(fill="x", padx=15)
        
        for feat in data['features']:
            ctk.CTkLabel(feat_frame, text=feat, font=("Segoe UI", 12), text_color="#e4e4e7", anchor="w").pack(fill="x", pady=2)
            
        # Spacer
        # ctk.CTkLabel(card, text="").pack(expand=True) # REMOVED: caused alignment chaos
        
        # --- PSYCHOLOGY ---
        if data.get('reasons'):
             reason = ctk.CTkLabel(card, text=f"💡 {data['reasons']}", font=("Segoe UI Italic", 10), 
                                   text_color="#a1a1aa", wraplength=220, justify="center")
             reason.pack(padx=10, pady=(0, 10))

        # --- CTA BUTTONS (DUAL CURRENCY) ---
        cta_bg = data['cta_color']
        text_fg = "black" if cta_bg in ["#eab308", "#ffd700"] else "white"
        
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 20))

        # Main Button (IDR - Local Payment)
        btn_idr = ctk.CTkButton(btn_frame, text=data['cta'], fg_color=cta_bg, hover_color=data['color'],
                            font=("Segoe UI Bold", 13), height=40, text_color=text_fg, cursor="hand2",
                            command=lambda t=tier_key, u=usd_price, i=idr_price: SubscriptionView._handle_cta(parent_ctx, t, u, i, "IDR"))
        btn_idr.pack(fill="x", pady=(0, 5))

        # Global Button (USD - Global Mastercard/Visa)
        btn_usd = ctk.CTkButton(btn_frame, text="GLOBAL CHECKOUT (USD)", fg_color="transparent", border_width=1, border_color="#3f3f46",
                            font=("Segoe UI Bold", 11), height=30, text_color="#a1a1aa", cursor="hand2",
                            command=lambda t=tier_key, u=usd_price, i=idr_price: SubscriptionView._handle_cta(parent_ctx, t, u, i, "USD"))
        btn_usd.pack(fill="x")
        
    @staticmethod
    def _handle_cta(parent, tier, price, idr_price, currency="IDR"):
        """Processes the purchase flow without freezing the UI (Gravity Rule: UX First)"""
        import threading
        from CTkMessagebox import CTkMessagebox
        
        if tier == "STANDARD":
            CTkMessagebox(title="Already Active", message="You are currently on the Standard Plan.", icon="info")
            return
            
        if tier == "INSTITUTIONAL" and price is None:
            # Contract flow
            webbrowser.open("https://t.me/richkeyrick")
            return
            
        def run_purchase():
            try:
                user_id = getattr(parent.db_manager, 'user_id', "anonymous")
                if user_id == "anonymous":
                    parent.after(0, lambda: CTkMessagebox(title="Identity Required", message="Please login to access Matrix Tiers.", icon="warning"))
                    return
                    
                # Define Success Callback (Runs on Thread -> needs safe UI update)
                def on_payment_success():
                    # Thread-safe UI update
                    def _ui_update():
                        parent.check_pro_status() # Refresh User State
                        CTkMessagebox(title="Payment Successful", message="Welcome to the Elite. Your Pro Status is active.", icon="check")
                        parent.show_page("dashboard")
                        
                    if hasattr(parent, 'safe_ui_update'):
                        parent.safe_ui_update(_ui_update)
                    else:
                        parent.after(0, _ui_update)

                # Perform blocking network call in thread
                from modules.logic.marketplace_service import MarketplaceService
                res = MarketplaceService.initiate_purchase(
                    user_id, tier, str(price), 
                    idr_price_str=idr_price, 
                    currency=currency,
                    on_success=on_payment_success
                )
                
                # Update UI on main thread
                if res.get("redirect_url"):
                    # Open OFFICIAL Midtrans Portal in Browser for 100% Branding & Security
                    # This replaces the hardcoded local simulation 'SnapPortal'
                    import webbrowser
                    url = res["redirect_url"]
                    parent.after(0, lambda: webbrowser.open(url))
                else:
                    parent.after(0, lambda: CTkMessagebox(title="Network Error", message="Failed to reach Payment Gateway. Try again later.", icon="cancel"))
            except Exception as e:
                parent.after(0, lambda e=e: CTkMessagebox(title="System Error", message=f"Buy Flow Error: {str(e)}", icon="cancel"))

        threading.Thread(target=run_purchase, daemon=True).start()



