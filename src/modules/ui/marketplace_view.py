import threading
import webbrowser
import customtkinter as ctk
from utils.currency import format_currency
from PIL import Image
from ui_theme import THEME_DARK, FONTS as LEGACY_FONTS
from ui_theme_modern import get_theme as get_modern_theme, FONTS as MODERN_FONTS
from utils.tooltips import CTkToolTip
from modules.logic.marketplace_service import MarketplaceService

# --- HELPER ---
def get_current_theme_data(parent):
    if hasattr(parent, 'selected_theme') and parent.selected_theme in ["light", "neutral"]:
        return get_modern_theme(parent.selected_theme), MODERN_FONTS
    return THEME_DARK, LEGACY_FONTS

class MarketplaceView:
    """
    The ITC Mall: Combined Signal Discovery & Strategy Storefront.
    Refactored from SignalHubView to support Hybrid commerce.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Marketplace page with Tabs."""
        theme, fonts = get_current_theme_data(parent)
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        # Header
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        info_col = ctk.CTkFrame(header, fg_color="transparent")
        info_col.pack(side="top", anchor="center") # Centered Header
        
        title_row = ctk.CTkFrame(info_col, fg_color="transparent")
        title_row.pack(anchor="center") # Centered Title Row
        
        # Main Title
        ctk.CTkLabel(title_row, text="🛍️ ITC MARKETPLACE", 
                     font=fonts.get("header_large", ("Segoe UI Bold", 24)), text_color=theme["accent_primary"]).pack(side="top", anchor="center")
        
        # Subtitle
        ctk.CTkLabel(info_col, text="Browse Premium Trading Signals & Verified High-ROI Strategies", 
                     font=fonts["body_small"], text_color=theme["text_secondary"]).pack(side="top", anchor="center")
        
        # --- CUSTOM NAVIGATION (Centered) ---
        nav_frame = ctk.CTkFrame(page, fg_color="transparent")
        nav_frame.pack(pady=(25, 15), anchor="center") # Strictly Centered (No Fill)
        
        # Helper for big nav buttons
        def create_nav_btn(text, cmd):
            return ctk.CTkButton(nav_frame, text=text, 
                                 font=("Segoe UI Bold", 13), 
                                 height=42, width=160, # Taller and wider buttons
                                 corner_radius=8,
                                 border_width=1,
                                 fg_color="transparent", 
                                 text_color=theme["text_secondary"],
                                 border_color=theme["border_default"],
                                 hover_color=theme["bg_secondary"],
                                 command=cmd)
        
        # Content Container
        content_frame = ctk.CTkFrame(page, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Create Scrollable Frames (Hidden by default)
        sb_col = theme.get("scrollbar_button_color", theme["accent_primary"])
        sb_hov = theme.get("scrollbar_button_hover_color", theme["accent_primary_hover"])
        
        parent.signal_scroll = ctk.CTkScrollableFrame(content_frame, fg_color="transparent", scrollbar_button_color=sb_col, scrollbar_button_hover_color=sb_hov)
        parent.strategy_scroll = ctk.CTkScrollableFrame(content_frame, fg_color="transparent", scrollbar_button_color=sb_col, scrollbar_button_hover_color=sb_hov)
        parent.vault_scroll = ctk.CTkScrollableFrame(content_frame, fg_color="transparent", scrollbar_button_color=sb_col, scrollbar_button_hover_color=sb_hov)

        # Tab Switching Logic
        def switch_tab(target):
            # Reset all buttons
            for k, btn in parent.market_btns.items():
                if k == target:
                    btn.configure(fg_color=theme["accent_primary"], text_color="white", border_color=theme["accent_primary"])
                else:
                    btn.configure(fg_color="transparent", text_color=theme["text_secondary"], border_color=theme["border_default"])
            
            # Hide all contents
            parent.signal_scroll.pack_forget()
            parent.strategy_scroll.pack_forget()
            parent.vault_scroll.pack_forget()
            
            # Show target
            if target == "signals":
                parent.signal_scroll.pack(fill="both", expand=True)
            elif target == "strategies":
                parent.strategy_scroll.pack(fill="both", expand=True)
            elif target == "presets":
                parent.vault_scroll.pack(fill="both", expand=True)
                MarketplaceView._fetch_and_render_vault(parent)
                
            parent.current_market_tab = target

        # Register switcher to parent for external access
        parent.market_switch_to = switch_tab

        # Create Buttons
        parent.market_btns = {}
        
        parent.market_btns["signals"] = create_nav_btn("🛰️ SIGNALS", lambda: switch_tab("signals"))
        parent.market_btns["signals"].pack(side="left", padx=(0, 10))
        
        parent.market_btns["strategies"] = create_nav_btn("🧠 STRATEGIES", lambda: switch_tab("strategies"))
        parent.market_btns["strategies"].pack(side="left", padx=10)
        
        parent.market_btns["presets"] = create_nav_btn("🔐 MY PRESETS", lambda: switch_tab("presets"))
        parent.market_btns["presets"].pack(side="left", padx=10)
        
        # Initialize
        switch_tab("signals")
        
        # Footer / Partnership Card
        footer = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=12, height=60, border_width=1, border_color=theme["border_default"])
        footer.pack(fill="x", pady=(15, 0))
        footer.pack_propagate(False)
        
        ctk.CTkLabel(footer, text="Open your own store? Connect with the ITC Merchant Network.", 
                     font=fonts.get("body_bold", ("Segoe UI Bold", 11)), text_color=theme["text_secondary"]).pack(side="left", padx=20)
        
        ctk.CTkButton(footer, text="MERCHANT PORTAL 💎", font=("Segoe UI Bold", 11), width=160, height=32,
                      fg_color="#1f6feb", command=lambda: parent.show_page("merchant")).pack(side="right", padx=10)
        
        # Sell/Publish Button
        ctk.CTkButton(footer, text="SELL STRATEGY 🚀", font=("Segoe UI Bold", 11), width=160, height=32,
                      fg_color="#d4af37", text_color="black", hover_color="#b5952f",
                      command=lambda: MarketplaceView.open_publisher_modal(parent)).pack(side="right", padx=10)
        
        # Initial Data Fetch
        MarketplaceView.refresh_signals(parent)
        MarketplaceView.refresh_strategies(parent)
        
        return page

    @staticmethod
    def refresh_signals(parent):
        """Fetches and renders signal cards."""
        def _task():
            if not hasattr(parent, 'db_manager'): return
            lang_filter = parent.translator.lang_code
            channels = parent.db_manager.get_verified_channels(lang_filter)
            
            def update_ui():
                if not parent.signal_scroll.winfo_exists(): return
                theme, fonts = get_current_theme_data(parent)
                for widget in parent.signal_scroll.winfo_children(): widget.destroy()
                if not channels:
                    ctk.CTkLabel(parent.signal_scroll, text="No channels found.", font=fonts["body_small"], text_color=theme["text_secondary"]).pack(pady=50)
                    return
                for c in channels:
                    MarketplaceView._create_channel_card(parent, parent.signal_scroll, c)
            
            parent.safe_ui_update(update_ui)
        threading.Thread(target=_task, daemon=True).start()

    @staticmethod
    def refresh_strategies(parent):
        """Fetches and renders strategy (preset) cards."""
        def _task():
            strategies = MarketplaceService.get_verified_strategies()
            
            def update_ui():
                if not parent.strategy_scroll.winfo_exists(): return
                theme, fonts = get_current_theme_data(parent)
                for widget in parent.strategy_scroll.winfo_children(): widget.destroy()
                if not strategies:
                    ctk.CTkLabel(parent.strategy_scroll, text="No strategies listed yet. Check back soon!", font=fonts["body_small"], text_color=theme["text_secondary"]).pack(pady=50)
                    return
                for s in strategies:
                    MarketplaceView._create_strategy_card(parent, parent.strategy_scroll, s)
            
            parent.safe_ui_update(update_ui)
        threading.Thread(target=_task, daemon=True).start()

    @staticmethod
    def _create_channel_card(parent, container, data):
        """Creates a premium card for a signal channel (Refined Layout)."""
        theme, fonts = get_current_theme_data(parent)
        card = ctk.CTkFrame(container, fg_color=theme["card_bg"], corner_radius=12, border_width=1, border_color=theme["border_default"])
        card.pack(fill="x", pady=6, padx=5) # Added side padding for scrollbar clearance
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=25, pady=20, fill="both") # More internal breathing room
        
        # Grid Layout for Precision
        inner.grid_columnconfigure(0, weight=1) # Info
        inner.grid_columnconfigure(1, weight=0) # Button (Fixed)

        # Left: Info
        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew")
        
        # Title with better spacing
        name_lbl = ctk.CTkLabel(left, text=data['name'], font=fonts.get("header_large", ("Segoe UI Bold", 18)), 
                                text_color=theme["accent_primary"] if data.get("is_featured") else theme["text_primary"], anchor="w")
        name_lbl.pack(anchor="w", pady=(0, 5))
        
        desc = data.get("description_id") if parent.translator.lang_code == "ID" else data.get("description_en")
        ctk.CTkLabel(left, text=desc, font=fonts["body_small"], text_color=theme["text_secondary"], 
                     anchor="w", justify="left", wraplength=600).pack(fill="x")

        # Right Side (Action) - Strictly Aligned via Grid
        right = ctk.CTkFrame(inner, fg_color="transparent", width=160)
        right.grid(row=0, column=1, sticky="e", padx=(20, 0))
        right.pack_propagate(False) # Force width
        
        ctk.CTkButton(right, text="CONNECT 🛰️", font=fonts.get("button", ("Segoe UI Bold", 12)), height=40, width=140, 
                      fg_color=theme["btn_primary_bg"], 
                      command=lambda: webbrowser.open(data["link"])).pack(pady=5)


    @staticmethod
    def _on_buy_mock(parent, data):
        """Simulates a purchase flow for mock items."""
        from CTkMessagebox import CTkMessagebox
        if data.get("price", 0) > 0:
             msg = CTkMessagebox(title="Purchase Confirmation", 
                           message=f"Proceed to buy '{data['title']}' for {format_currency(data['price'])}?\n\n(This is a simulated transaction for Premium Demo)",
                           icon="question", option_1="Confirm Purchase", option_2="Cancel", fade_in_duration=0)
             if msg.get() == "Confirm Purchase":
                 parent.trigger_toast("Purchase Successful!", "Strategy installed to My Presets.")
        else:
             parent.trigger_toast("Installation Complete", f"'{data['title']}' added to your portfolio.")

    @staticmethod
    def _create_strategy_card(parent, container, data):
        """Creates a professional card for an executable strategy preset."""
        theme, fonts = get_current_theme_data(parent)
        card = ctk.CTkFrame(container, fg_color=theme["card_bg"], corner_radius=12, border_width=1, border_color=theme["border_default"])
        card.pack(fill="x", pady=8)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=20, pady=15, fill="both")
        
        # Grid Layout
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=0)

        # Left: Info
        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(left, text=data['title'].upper(), font=fonts.get("header_large", ("Segoe UI Bold", 16)), 
                     text_color="white", anchor="w").pack(anchor="w")
        
        ctk.CTkLabel(left, text=data['description'], font=fonts["body_small"], text_color=theme["text_secondary"], 
                     anchor="w", justify="left", wraplength=450).pack(fill="x", pady=(2, 8))
        
        # Metrics Row
        m_row = ctk.CTkFrame(left, fg_color="transparent")
        m_row.pack(fill="x")
        
        # Win Rate Badge
        wr = data.get('verified_win_rate', 0)
        wr_color = "#3fb950" if wr > 60 else "#d29922"
        ctk.CTkLabel(m_row, text=f" WR: {wr}% ", font=("Segoe UI Bold", 10), fg_color=wr_color, text_color="white", corner_radius=4).pack(side="left", padx=(0, 10))
        
        # Profit Factor
        pf = data.get('verified_profit_factor', 1.0)
        ctk.CTkLabel(m_row, text=f" PF: {pf:.2f} ", font=("Segoe UI Bold", 10), fg_color="#1f6feb", text_color="white", corner_radius=4).pack(side="left")
        
        ctk.CTkLabel(left, text="✅ SECURE AUDIT: VERIFIED", font=("Segoe UI Bold", 9), text_color="#3fb950").pack(anchor="w", pady=(5, 0))

        # Right Side (Action) - Grid Aligned
        right = ctk.CTkFrame(inner, fg_color="transparent", width=160)
        right.grid(row=0, column=1, sticky="e", padx=(10, 0))
        right.pack_propagate(False)
        
        price = data.get('price', 0)
        
        # Currency Localization (Centralized)
        price_text = format_currency(price) if price > 0 else "FREE"
            
        ctk.CTkLabel(right, text=price_text, font=("Segoe UI Bold", 18), text_color="white").pack(pady=(0, 5))
        
        # Check if already owned
        is_owned = False 
        
        btn_txt = "INSTALL ⬇️" if price == 0 else "BUY NOW 💳"
        btn_color = theme["accent_primary"] if price == 0 else "#10b981"
        
        # Point to Mock Handler
        ctk.CTkButton(right, text=btn_txt, font=("Segoe UI Bold", 12), height=32, width=120, 
                      fg_color=btn_color, text_color="white",
                      command=lambda: MarketplaceView._on_buy_mock(parent, data)).pack(side="right") # Mock Action

    @staticmethod
    def _handle_purchase(parent, data):
        """Simulates or triggers actual purchase."""
        from CTkMessagebox import CTkMessagebox
        msg = f"Purchase '{data['title']}' for {format_currency(data['price'])}?"
        confirm = CTkMessagebox(title="Confirm Order", message=msg, icon="question", option_1="Yes", option_2="No")
        
        if confirm.get() == "Yes":
            success, res = MarketplaceService.install_to_vault(parent.db_manager.user_id, data)
            if success:
                MarketplaceView._handle_install_success(parent, res)
            else:
                CTkMessagebox(title="Error", message=res, icon="cancel")

    @staticmethod
    def _handle_install(parent, data):
        """Installs the already purchased strategy."""
        from CTkMessagebox import CTkMessagebox
        success, res = MarketplaceService.install_to_vault(parent.db_manager.user_id, data)
        if success:
            MarketplaceView._handle_install_success(parent, "Strategy installed successfully!")
        else:
            CTkMessagebox(title="Error", message=res, icon="cancel")

    @staticmethod
    def _handle_install_success(parent, message):
        """Centralized success handler for installs/purchases."""
        from CTkMessagebox import CTkMessagebox
        from modules.ui.trading_view import TradingView
        
        # Refresh UI
        TradingView._refresh_quick_load(parent)
        MarketplaceView._fetch_and_render_vault(parent)
        MarketplaceView.refresh_strategies(parent)
        
        # Switch to Presets tab (Using new custom switcher)
        if hasattr(parent, 'market_switch_to'):
            parent.market_switch_to("presets")
            
        CTkMessagebox(title="Success", message=message, icon="check")

    @staticmethod
    def _fetch_and_render_vault(parent):
        """Fetches user's private strategies and renders them in the Presets tab."""
        if not hasattr(parent, 'vault_scroll'): return
        for w in parent.vault_scroll.winfo_children(): w.destroy()
        
        theme = parent.get_theme_data()
        
        # --- PRESETS HEADER ---
        h = ctk.CTkFrame(parent.vault_scroll, fg_color="transparent")
        h.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(h, text="🔐 My Personal Preset Library", font=("Segoe UI Bold", 16), 
                     text_color=theme["accent_primary"]).pack(side="left", padx=10)
        
        # --- PRESET LIST ---
        presets = parent.db_manager.get_user_presets()
        
        if not presets:
            ctk.CTkLabel(parent.vault_scroll, text="Your preset library is empty.\nSave a strategy or buy one from the marketplace to see it here.", 
                        text_color="gray", font=("Segoe UI", 12)).pack(pady=60)
            return

        for p in presets:
            row = ctk.CTkFrame(parent.vault_scroll, fg_color=theme["bg_secondary"], corner_radius=12, 
                               border_color=theme["border_default"], border_width=1)
            row.pack(fill="x", pady=6, padx=5)
            
            # Icon
            ctk.CTkLabel(row, text="💾", font=("Segoe UI", 28)).pack(side="left", padx=20, pady=15)
            
            # Info
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, pady=10)
            ctk.CTkLabel(info, text=p['name'], font=("Segoe UI Bold", 15), text_color="white", anchor="w").pack(fill="x")
            date_str = p.get('created_at', 'Recently')[:10]
            ctk.CTkLabel(info, text=f"Installed: {date_str} | ID: {str(p['id'])[:8]}", 
                        font=("Segoe UI", 11), text_color=theme["text_secondary"], anchor="w").pack(fill="x")
            
            # Actions
            act = ctk.CTkFrame(row, fg_color="transparent")
            act.pack(side="right", padx=15)
            
            def load_strat(data=p.get('config_json', {})):
                from modules.logic.config_aggregator import ConfigAggregator
                from CTkMessagebox import CTkMessagebox
                if ConfigAggregator.apply_config_dict(parent, data):
                    CTkMessagebox(title="Loaded", message="Strategy loaded into Main Settings!", icon="check")
                else:
                    CTkMessagebox(title="Error", message="Failed to load settings.", icon="cancel")

            def delete_strat(pid=p['id']):
                from CTkMessagebox import CTkMessagebox
                confirm = CTkMessagebox(title="Delete?", message="Remove this strategy from your library?", icon="warning", option_1="Yes", option_2="No")
                if confirm.get() == "Yes":
                    if parent.db_manager.delete_user_preset(pid):
                        MarketplaceView._fetch_and_render_vault(parent)
            
            ctk.CTkButton(act, text="⚡ LOAD", width=80, height=32, font=("Segoe UI Bold", 11),
                        fg_color="#10b981", hover_color="#059669", command=load_strat).pack(side="left", padx=3)
            ctk.CTkButton(act, text="🗑️", width=35, height=32, fg_color="#ef4444", hover_color="#dc2626", 
                        command=delete_strat).pack(side="left", padx=3)

    @staticmethod
    def open_publisher_modal(parent):
        """Shows the popup to publish a strategy."""
        
        # Modal Setup
        modal = ctk.CTkToplevel(parent)
        modal.title("Publish Strategy - Proof of Profit")
        modal.geometry("500x650")
        modal.transient(parent)
        modal.grab_set()
        
        theme, fonts = get_current_theme_data(parent)
        modal.configure(fg_color=theme["bg_primary"])
        
        # Header
        ctk.CTkLabel(modal, text="🚀 Publish to Gravity Market", font=("Segoe UI Bold", 20), text_color=theme["accent_primary"]).pack(pady=(20, 5))
        ctk.CTkLabel(modal, text="Your strategy will be verified against local history.", font=fonts["body_small"], text_color=theme["text_secondary"]).pack(pady=(0, 20))
        
        # Form
        entry_title = ctk.CTkEntry(modal, placeholder_text="Strategy Name (e.g. Gold Scalper V1)", width=400, height=40)
        entry_title.pack(pady=10)
        
        entry_desc = ctk.CTkTextbox(modal, width=400, height=100)
        entry_desc.insert("0.0", "Description & Risk Warning...")
        entry_desc.pack(pady=10)
        
        entry_price = ctk.CTkEntry(modal, placeholder_text="Price in IDR (e.g. 150000)", width=400, height=40)
        entry_price.pack(pady=10)
        
        # Config Selector (Simplified: Just dumping current active config)
        ctk.CTkLabel(modal, text="* Will use CURRENT ACTIVE settings as the product.", text_color="#f85149", font=("Segoe UI", 11)).pack(pady=5)
        
        # Progress Log
        lbl_status = ctk.CTkLabel(modal, text="Ready to Verify...", text_color=theme["text_secondary"])
        lbl_status.pack(pady=10)
        
        def _run_publish():
            title = entry_title.get()
            desc = entry_desc.get("0.0", "end").strip()
            price = entry_price.get()
            
            if not title or not price:
                lbl_status.configure(text="❌ Title and Price are required!", text_color="#f85149")
                return
            
            lbl_status.configure(text="⏳ Verifying Profitability (Proof of Profit)...", text_color="#d29922")
            btn_pub.configure(state="disabled")
            
            def _thread():
                from modules.logic.config_aggregator import ConfigAggregator
                current_config = ConfigAggregator.collect_config(parent)
                
                success, msg, metrics = MarketplaceService.publish_strategy_flow(title, desc, price, current_config)
                
                if success:
                    parent.safe_ui_update(lambda: lbl_status.configure(text=f"✅ SUCCESS! ROI: {metrics.get('roi')}%", text_color="#3fb950"))
                    parent.safe_ui_update(lambda: MarketplaceView.refresh_strategies(parent))
                    parent.after(2000, modal.destroy)
                else:
                    parent.safe_ui_update(lambda: lbl_status.configure(text=f"❌ {msg}", text_color="#f85149"))
                    parent.safe_ui_update(lambda: btn_pub.configure(state="normal"))
            
            threading.Thread(target=_thread, daemon=True).start()

        btn_pub = ctk.CTkButton(modal, text="VERIFY & PUBLISH", width=400, height=50, fg_color="#10b981", hover_color="#059669", font=("Segoe UI Bold", 14), command=_run_publish)
        btn_pub.pack(pady=10)
