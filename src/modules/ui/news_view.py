import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS
import threading
import datetime
from modules.logic.smart_fill import SmartFill
from index import get_env_list

class NewsView:
    """
    Intelligence Terminal Module
    Tabs: Breaking News | Economic Calendar | Technical Insight
    Features: Reader Mode, Back Button, Serper Integration
    """
    
    print("// DEBUG: RELOADED NEWS VIEW V9")
    
    @staticmethod
    def build(parent):
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        
        # Main Page Container
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        
        # --- TIER CHECK ---
        tier = "STANDARD"
        if hasattr(parent, 'db_manager') and parent.db_manager:
            tier = parent.db_manager.get_user_tier().upper()

        if tier not in ["PLATINUM", "INSTITUTIONAL"]:
            NewsView._build_lock_screen(page, parent, theme)
            return page
        # ------------------

        page.grid_rowconfigure(0, weight=0) # Header
        page.grid_rowconfigure(1, weight=1) # Tabview
        page.grid_rowconfigure(2, weight=0) # Status/Telemetry
        
        # 1. Header
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        
        ctk.CTkLabel(header, text="Intelligence Terminal", font=("Segoe UI Semibold", 22), 
                     text_color=theme["text_primary"]).pack(side="left")
                   # Refresh Button
        parent.refresh_btn = ctk.CTkButton(header, text="🔄 Refresh", width=100, 
                                          command=lambda: NewsView.refresh_data(parent, force=True),
                                          fg_color=theme["bg_tertiary"], hover_color=theme["accent_primary"])
        parent.refresh_btn.pack(side="right") # Changed from grid to pack to match original layout, assuming header is the parent.

        # Status/Telemetry Label
        parent.status_label = ctk.CTkLabel(page, text="Status: Ready", font=("Segoe UI", 10), text_color=theme["text_secondary"])
        parent.status_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)


        # 2. Main Tab View (Custom Segmented Control)
        # Replaced standard TabView for better aesthetics
        parent.news_tabs = ctk.CTkFrame(page, fg_color="transparent")
        parent.news_tabs.grid(row=1, column=0, sticky="nsew")
        parent.news_tabs.grid_columnconfigure(0, weight=1)
        parent.news_tabs.grid_rowconfigure(1, weight=1) # Content Area
        
        # Navigation Bar
        nav_container = ctk.CTkFrame(parent.news_tabs, fg_color="transparent")
        nav_container.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        nav_container.grid_columnconfigure(0, weight=1)
        
        # Tabs - HIGHER AESTHETICS (Floating Pills)
        parent.tab_buttons = ctk.CTkSegmentedButton(
            nav_container,
            values=["Breaking News", "Economic Calendar", "Market Technicals", "AI Analysis"],
            command=lambda value: NewsView._on_tab_change(parent, value),
            font=("Segoe UI", 13, "bold"),
            height=38,
            selected_color=theme["accent_primary"],
            selected_hover_color=theme["accent_secondary"],
            unselected_color=theme["bg_tertiary"],
            unselected_hover_color=theme["bg_secondary"],
            text_color=theme["text_primary"],
            corner_radius=20 # Pill shape
        )
        # Center the menu
        parent.tab_buttons.grid(row=0, column=0, sticky="n")
        parent.tab_buttons.set("Breaking News") # Set default

        # Content Areas
        parent.breaking_frame = ctk.CTkFrame(parent.news_tabs, fg_color="transparent")
        parent.calendar_frame = ctk.CTkFrame(parent.news_tabs, fg_color="transparent")
        parent.technicals_frame = ctk.CTkFrame(parent.news_tabs, fg_color="transparent")
        parent.analysis_frame = ctk.CTkFrame(parent.news_tabs, fg_color="transparent") # New Analysis Frame
        
        # Initialize Views
        NewsView.build_breaking_tab(parent, parent.breaking_frame, theme)
        NewsView.build_calendar_tab(parent, parent.calendar_frame, theme)
        NewsView.build_technicals_tab(parent, parent.technicals_frame, theme)
        NewsView.build_analysis_tab(parent, parent.analysis_frame, theme) # Build Analysis Tab
        
        # Show initial
        parent.breaking_frame.grid(row=1, column=0, sticky="nsew") # Use grid for content frames

        # 3. Reader Mode Overlay (Hidden by Default)
        parent.reader_frame = ctk.CTkFrame(page, fg_color=theme["bg_primary"], corner_radius=0)
        # We will .place() this over the whole page when active
        
        # Initial Data Fetch
        parent.after(1000, lambda: NewsView.refresh_data(parent))
        
        return page

    @staticmethod
    def _build_lock_screen(page, parent, theme):
        """Renders a Premium Lock Screen for non-VIP users"""
        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)
        
        container = ctk.CTkFrame(page, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # 1. Lock Icon (Emoji or Text since we don't have asset guaranteed)
        ctk.CTkLabel(container, text="🔒", font=("Segoe UI", 80)).pack(pady=(0, 20))
        
        # 2. Title
        title_text = parent.translator.get("lock_title_intelligence") if hasattr(parent, 'translator') else "INTELLIGENCE TERMINAL LOCKED"
        ctk.CTkLabel(container, text=title_text, 
                     font=("Segoe UI", 24, "bold"), 
                     text_color=theme["accent_primary"]).pack(pady=(0, 10))
                     
        # 3. Subtitle / Description
        msg = parent.translator.get("lock_msg_intelligence") if hasattr(parent, 'translator') else "This feature is exclusive to Platinum & Institutional Members."
        ctk.CTkLabel(container, text=msg, 
                     font=("Segoe UI", 14), 
                     text_color=theme["text_secondary"],
                     justify="left").pack(pady=(0, 30))
        
        # 4. Premium Badge / Divider
        divider = ctk.CTkFrame(container, height=2, width=200, fg_color=theme["bg_tertiary"])
        divider.pack(pady=(0, 30))
        
        # 5. Call to Action Button
        btn_text = parent.translator.get("btn_upgrade_platinum") if hasattr(parent, 'translator') else "UPGRADE TO PLATINUM 💎"
        
        def open_upgrade():
             # Navigate to subscription page
             if hasattr(parent, 'show_page'):
                 parent.show_page("subscription") 
             
        ctk.CTkButton(container, text=btn_text, 
                      font=("Segoe UI", 13, "bold"),
                      height=40, width=220,
                      fg_color=theme["accent_primary"], 
                      hover_color=theme["accent_secondary"],
                      image=None, 
                      command=open_upgrade).pack()
        
        # 6. Secondary Help
        ctk.CTkLabel(container, text="Contact support for Institutional access", 
                     font=("Segoe UI", 11), 
                     text_color=theme["text_secondary"]).pack(pady=(20, 0))

    @staticmethod
    def build_breaking_tab(parent, tab_frame, theme):
        tab_frame.grid_columnconfigure(0, weight=1)
        tab_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable List
        parent.news_list = ctk.CTkScrollableFrame(tab_frame, fg_color="transparent")
        parent.news_list.grid(row=0, column=0, sticky="nsew")
        
        # Loading Placeholder
        ctk.CTkLabel(parent.news_list, text="Fetching Top Financial Stories...", 
                     text_color=theme["text_secondary"]).pack(pady=20)

    @staticmethod
    def _on_tab_change(parent, value):
        parent.breaking_frame.grid_forget()
        parent.calendar_frame.grid_forget()
        parent.technicals_frame.grid_forget()
        parent.analysis_frame.grid_forget()
        
        if value == "Breaking News":
            parent.breaking_frame.grid(row=1, column=0, sticky="nsew")
        elif value == "Economic Calendar":
            parent.calendar_frame.grid(row=1, column=0, sticky="nsew")
        elif value == "Market Technicals":
            parent.technicals_frame.grid(row=1, column=0, sticky="nsew")
            # Only refresh if empty
            if not parent.tech_grid.winfo_children() or len(parent.tech_grid.winfo_children()) < 2:
                NewsView.refresh_technicals(parent)
        elif value == "AI Analysis":
            parent.analysis_frame.grid(row=1, column=0, sticky="nsew")
            # Persistent check: Only refresh if no result cards exist
            has_cards = any(isinstance(w, ctk.CTkFrame) for w in parent.predictions_container.winfo_children() if w.winfo_name() != "loading_lbl")
            if not has_cards:
                NewsView.refresh_analysis(parent)

    @staticmethod
    def build_analysis_tab(parent, frame, theme):
        """Builds the AI Analysis Dashboard (SkyNET Predictions)"""
        # Header
        header = ctk.CTkFrame(frame, fg_color=theme["bg_secondary"], corner_radius=8, height=40)
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header, 
            text="SkyNET Market Intelligence (AI Prediction)", 
            font=("Segoe UI", 13, "bold"), 
            text_color=theme["accent_primary"]
        ).pack(side="left", padx=15, pady=10)
        
        # Refresh Button
        ctk.CTkButton(
            header,
            text="Run Analysis",
            width=100,
            height=28,
            fg_color=theme["accent_primary"],
            hover_color=theme["accent_secondary"],
            font=("Segoe UI", 11, "bold"),
            command=lambda: NewsView.refresh_analysis(parent)
        ).pack(side="right", padx=10, pady=5)
        
        # Scrollable Container for Predictions
        parent.predictions_container = ctk.CTkScrollableFrame(
            frame,
            fg_color="transparent",
            scrollbar_button_color=theme["accent_primary"],
            scrollbar_button_hover_color=theme["accent_secondary"]
        )
        parent.predictions_container.pack(fill="both", expand=True)

    @staticmethod
    def refresh_analysis(parent):
        """Triggers AI Analysis of Calendar Events (Sequential Loading)"""
        # Clear existing
        if hasattr(parent, 'predictions_container'):
             for widget in parent.predictions_container.winfo_children():
                widget.destroy()
            
        # Loading State
        loading_lbl = ctk.CTkLabel(parent.predictions_container, text="SkyNET is scanning market data...", text_color="#A0A0A0")
        loading_lbl.pack(pady=20)
        parent.update_idletasks()
        
        def _run_sequential():
            try:
                from modules.logic.smart_fill import SmartFill
                from index import get_env_list
                env = get_env_list()
                
                # 1. Fetch Events (XML or Serper Fallback)
                events = SmartFill._fetch_calendar_events(env)
                
                # Helper for Safe UI Updates
                def safe_configure(widget, **kwargs):
                    try:
                        if widget.winfo_exists():
                            widget.configure(**kwargs)
                    except: pass
                
                if not events:
                    print(f"// [DEBUG] No events returned from SmartFill.")
                    parent.after(0, lambda: safe_configure(loading_lbl, text="No events found in data feed."))
                    return

                # Filter High Impact
                print(f"// [DEBUG] Filtering {len(events)} events for High/Medium impact...")
                high_impact = [e for e in events if e.get("impact") in ["High", "Medium"]]
                print(f"// [DEBUG] Found {len(high_impact)} High/Medium impact events.")
                
                if not high_impact:
                    parent.after(0, lambda: safe_configure(loading_lbl, text="No significant upcoming events found."))
                    return
                
                # Limit to top 5
                targets = high_impact[:5]
                print(f"// [DEBUG] Analyzing top {len(targets)} targets.")
                
                # Update Text
                parent.after(0, lambda: safe_configure(loading_lbl, text=f"Analyzing {len(targets)} key events..."))
                
                # 2. Sequential Analysis Loop
                success_count = 0
                for i, event in enumerate(targets):
                    # Update Loading Status
                    parent.after(0, lambda idx=i+1, total=len(targets): safe_configure(loading_lbl, text=f"Analyzing {event.get('currency')} event {idx}/{total}..."))
                    
                    # Analyze Single Event
                    prediction = SmartFill.analyze_single_event(env, event)
                    
                    if prediction:
                        success_count += 1
                        # Append Card Immediately
                        try: parent.after(0, lambda p=prediction: NewsView._create_prediction_card(parent, p))
                        except: pass
                    
                    # Sequential throttling
                    import time
                    time.sleep(0.05)

                if success_count == 0:
                    parent.after(0, lambda: safe_configure(loading_lbl, text="SkyNET could not determine clear bias for these events."))
                    return

                # Final Cleanup
                try: parent.after(0, lambda: loading_lbl.destroy())
                except: pass

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"// [BUG] Analysis Error: {e}")
                try: parent.after(0, lambda: safe_configure(loading_lbl, text=f"System Error: {e}"))
                except: pass
                
        import threading
        threading.Thread(target=_run_sequential, daemon=True).start()

    @staticmethod
    def _display_predictions(parent, predictions, loading_lbl):
        """Deprecated in favor of sequential loading, but kept for compatibility logic if needed"""
        pass

    @staticmethod
    def _create_prediction_card(parent, pred):
        """Renders a premium AI prediction card for an economic event"""
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        card = ctk.CTkFrame(parent.predictions_container, fg_color=theme["bg_secondary"], corner_radius=10, border_width=1, border_color=theme["border_default"])
        card.pack(fill="x", pady=8, padx=10)
        
        # Meta Row: SkyNET Insight Branding
        meta = ctk.CTkFrame(card, fg_color="transparent", height=20)
        meta.pack(fill="x", padx=15, pady=(8, 2))
        ctk.CTkLabel(meta, text="🤖 SKYNET INSIGHT", font=("Segoe UI", 10, "bold"), text_color="#A0A0A0").pack(side="left")
        
        # Main Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(0, 5))
        
        # Field mapping (AI returns 'event' from analyze_single_event)
        event_name = pred.get("event", pred.get("event_ids", "Economic Event"))
        currency = pred.get("currency", "---")
        bias = pred.get("bias", "NEUTRAL").upper()
        
        # Color Tokens
        bias_color = "#3fb950" if "BULLISH" in bias else "#f85149" if "BEARISH" in bias else "#d29922"
        
        ctk.CTkLabel(header, text=f"{currency} - {event_name}", font=("Segoe UI", 13, "bold"), text_color=theme["text_primary"]).pack(side="left")
        
        # Bias Badge
        badge = ctk.CTkFrame(header, fg_color=bias_color, corner_radius=4)
        badge.pack(side="right")
        ctk.CTkLabel(badge, text=f" {bias} ", font=("Segoe UI", 11, "bold"), text_color="white").pack(padx=8, pady=2)
        
        # Middle: Reasoning
        reason = pred.get("reason", pred.get("reasoning", "Analyzing market sentiment..."))
        ctk.CTkLabel(card, text=reason, font=("Segoe UI", 12), text_color=theme["text_secondary"], wraplength=500, justify="left", anchor="w").pack(fill="x", padx=15, pady=(5, 10))
        
        # Footer: Metadata (Time/Impact)
        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=15, pady=(0, 10))
        
        impact = pred.get("impact", "High")
        time_val = pred.get("time", "---")
        conf = pred.get("confidence", "Medium")
        source = pred.get("source", "ForexFactory")
        
        footer_text = f"🕒 {time_val}  |  🔥 Impact: {impact}  |  🎯 Confidence: {conf}  |  🌐 Source: {source}"
        ctk.CTkLabel(footer, text=footer_text, font=("Segoe UI", 10), text_color="#707070").pack(side="left")
        
        # Bottom: Confidence
        conf = pred.get("confidence", "50%")
        bot = ctk.CTkFrame(card, fg_color="transparent")
        bot.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(bot, text=f"Confidence: {conf}", font=("Segoe UI", 10, "italic"), text_color=theme["text_secondary"]).pack(side="right")
    
    @staticmethod
    def build_calendar_tab(parent, tab_frame, theme):
        tab_frame.grid_columnconfigure(0, weight=1)
        # Minimal Calendar Header
        # Grid Header for Alignment
        header = ctk.CTkFrame(tab_frame, height=40, fg_color=theme["bg_tertiary"])
        header.pack(fill="x", padx=5, pady=5)
        
        # Fixed Weights for strict alignment (MUST MATCH ROW CONFIG)
        # 0:Date, 1:Time, 2:Currency, 3:Event, 4:Impact, 5:Forecast
        lang = parent.env.get("APP_LANG", "EN").upper()
        if lang == "ID":
            # Tgl | USA | WIB | Cur | Peristiwa | Dampak | Fcst | Prev | Brief | [Spacer]
            header.grid_columnconfigure(0, weight=0, minsize=80) 
            header.grid_columnconfigure(1, weight=0, minsize=60) 
            header.grid_columnconfigure(2, weight=0, minsize=70) 
            header.grid_columnconfigure(3, weight=0, minsize=50) 
            header.grid_columnconfigure(4, weight=0, minsize=200)
            header.grid_columnconfigure(5, weight=0, minsize=80) 
            header.grid_columnconfigure(6, weight=0, minsize=60) 
            header.grid_columnconfigure(7, weight=0, minsize=60) 
            header.grid_columnconfigure(8, weight=0, minsize=100)
            header.grid_columnconfigure(9, weight=1) # Spacer
            headers = ["Tgl", "USA", "WIB", "Cur", "Peristiwa", "Dampak", "Fcst", "Prev", "Brief"]
        else:
            # Date | Time | Cur | Event | Impact | Fcst | Prev | Brief | [Spacer]
            header.grid_columnconfigure(0, weight=0, minsize=90) 
            header.grid_columnconfigure(1, weight=0, minsize=70) 
            header.grid_columnconfigure(2, weight=0, minsize=60) 
            header.grid_columnconfigure(3, weight=0, minsize=250)
            header.grid_columnconfigure(4, weight=0, minsize=80) 
            header.grid_columnconfigure(5, weight=0, minsize=70) 
            header.grid_columnconfigure(6, weight=0, minsize=70) 
            header.grid_columnconfigure(7, weight=0, minsize=110)
            header.grid_columnconfigure(8, weight=1) # Spacer
            headers = ["Date", "Time", "Cur", "Event", "Impact", "Fcst", "Prev", "Brief"]
        
        # Interactive Headers
        parent.cal_header_buttons = []
        for idx, h in enumerate(headers):
            # Center Impact header to match row
            align = "w" if h != "Dampak" and h != "Impact" else "ew" 
            
            # Use Flat Buttons that look like labels
            btn = ctk.CTkButton(header, text=h, font=("Segoe UI", 12, "bold"),
                                fg_color="transparent", hover_color=theme["bg_secondary"],
                                text_color=theme["text_primary"], width=10, height=30,
                                anchor=align,
                                command=lambda c=h: NewsView.handle_header_sort(parent, c))
            btn.grid(row=0, column=idx, sticky=align, padx=5)
            parent.cal_header_buttons.append((btn, h))

        parent.cal_list = ctk.CTkScrollableFrame(tab_frame, fg_color="transparent")
        parent.cal_list.pack(fill="both", expand=True, padx=5, pady=5)

    @staticmethod
    def build_technicals_tab(parent, tab_frame, theme):
        # Grid of Cards for Major Pairs
        parent.tech_grid = ctk.CTkScrollableFrame(tab_frame, fg_color="transparent")
        parent.tech_grid.pack(fill="both", expand=True)
        
        # Initial Placeholder
        ctk.CTkLabel(parent.tech_grid, text="Analyzing Market Structure...", 
                     text_color=theme["text_secondary"]).pack(pady=20)

    @staticmethod
    def refresh_data(parent, force=False):
        """Fetches fresh news and calendar data"""
        threading.Thread(target=lambda: NewsView._fetch_news_worker(parent, force), daemon=True).start()

    @staticmethod
    def refresh_technicals(parent):
        """Fetches market technicals incrementally to prevent UI freeze"""
        threading.Thread(target=lambda: NewsView._fetch_technicals_worker(parent), daemon=True).start()

    @staticmethod
    def _fetch_news_worker(parent, force=False):
        from index import get_env_list
        env = get_env_list()
        
        # 1. Calendar Aggregation (High-Density)
        data_cal = SmartFill.get_calendar_events(env, force_refresh=force)
        parent.cal_events_data = data_cal # Persist for sorting
        
        # UI Update Status
        def update_status():
            try:
                cooldown = SmartFill._get_refresh_cooldown("ForexFactory")
                if cooldown > 0:
                    parent.status_label.configure(text=f"Status: Safe Mode (Live Refresh in {cooldown}s)", text_color="#f0883e")
                else:
                    parent.status_label.configure(text=f"Status: Live Data (Synchronized)", text_color="#2ea44f")
            except: pass
            
        parent.after(0, update_status)

        # 2. Fetch Breaking News (Market Stories)
        data_news = SmartFill._fetch_serper_news("FOREX", env, raw_query="finance news forex trading bloomberg reuters", return_json=True)
        
        # Update UI Table & News List
        if hasattr(parent, 'safe_ui_update'):
            parent.safe_ui_update(lambda: NewsView.update_ui(parent, data_news, data_cal))

    @staticmethod
    def _fetch_technicals_worker(parent):
        """Incremental MT5 Technical Scanner"""
        from index import get_env_list
        from modules.mt5.mt5_service import MT5Service
        from modules.chart.chart_data import ChartDataManager
        
        # Clear existing entries
        parent.after(0, lambda: [w.destroy() for w in parent.tech_grid.winfo_children()])
        
        try:
            visible = MT5Service.instance().get_visible_symbols()
            pairs = visible[:50] if visible else ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD", "USDJPY"]
        except:
            pairs = ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD", "USDJPY"]

        # Card layout constants
        cols = 3
        current_row_frame = None
        
        for idx, symbol in enumerate(pairs):
            try:
                # Fetch Single Technical Summary
                summary = ChartDataManager.get_technical_summary(symbol)
                summary['symbol'] = symbol
                
                # UI Update: Append Single Card
                def add_card(s=summary, i=idx):
                    nonlocal current_row_frame
                    theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
                    
                    if i % cols == 0:
                        current_row_frame = ctk.CTkFrame(parent.tech_grid, fg_color="transparent")
                        current_row_frame.pack(fill="x", pady=5)
                    
                    # Create Card
                    card = ctk.CTkFrame(current_row_frame, fg_color=theme["bg_secondary"], corner_radius=10)
                    card.pack(side="left", fill="both", expand=True, padx=5)
                    
                    # Render Content
                    ctk.CTkLabel(card, text=s['symbol'], font=("Segoe UI", 16, "bold"), text_color=theme["accent_primary"]).pack(pady=(10,5))
                    
                    trend = s.get("TREND", "Neutral").upper()
                    is_bull = any(x in trend for x in ["BULL", "BUY", "UP", "STRONG BUY"])
                    is_bear = any(x in trend for x in ["BEAR", "SELL", "DOWN", "STRONG SELL"])
                    trend_color = theme["success"] if is_bull else (theme["danger"] if is_bear else theme["text_secondary"])
                    
                    ctk.CTkLabel(card, text=trend, font=("Segoe UI", 12, "bold"), text_color=trend_color).pack()
                    
                    info = ctk.CTkFrame(card, fg_color="transparent")
                    info.pack(pady=10)
                    ctk.CTkLabel(info, text=f"RSI: {s.get('RSI', '50')}", font=("Consolas", 11)).pack()
                    
                    ema_val = s.get('EMA_CROSS', '-')
                    ema_color = theme["success"] if ">" in ema_val else (theme["danger"] if "<" in ema_val else theme["text_secondary"])
                    ctk.CTkLabel(info, text=f"EMA: {ema_val}", font=("Consolas", 11), text_color=ema_color).pack()
                
                parent.after(0, add_card)
                import time
                time.sleep(0.01) # Small throttle
                
            except: continue

    @staticmethod
    def update_ui(parent, news_items, cal_events):
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        
        # --- A. BREAKING NEWS (Rich Cards) ---
        if news_items is not None:
            for widget in parent.news_list.winfo_children(): widget.destroy()
            
            if isinstance(news_items, list) and news_items:
                for item in news_items:
                    card = ctk.CTkFrame(parent.news_list, fg_color=theme["bg_secondary"], corner_radius=8)
                    card.pack(fill="x", pady=6, padx=8)
                    
                    # Title & Meta
                    header_frame = ctk.CTkFrame(card, fg_color="transparent")
                    header_frame.pack(fill="x", padx=10, pady=(10, 0))
                    
                    title = item.get('title', 'Unknown Title')
                    source = item.get('source', 'Google News')
                    time_ago = item.get('date', 'Just now')
                    
                    ctk.CTkLabel(header_frame, text=title, font=("Segoe UI Semibold", 14), 
                                 text_color=theme["text_primary"], anchor="w", wraplength=600).pack(fill="x")
                    
                    meta_text = f"{source} • {time_ago}"
                    ctk.CTkLabel(header_frame, text=meta_text, font=("Segoe UI", 11), 
                                 text_color=theme["text_secondary"], anchor="w").pack(fill="x")
                    
                    # Snippet
                    snippet = item.get('snippet', '')
                    if snippet:
                        ctk.CTkLabel(card, text=snippet[:180]+"...", font=("Segoe UI", 12), text_color=theme["text_secondary"], 
                                     anchor="w", justify="left", wraplength=650).pack(fill="x", padx=10, pady=5)
                    
                    # Interactivity (Click to read)
                    url = item.get('link', '')
                    if url:
                        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
                        
                        ctk.CTkButton(btn_frame, text="📖 Read Analysis", width=120, height=28,
                                      fg_color="transparent", border_width=1, border_color=theme["accent_primary"],
                                      text_color=theme["accent_primary"], hover_color=theme["bg_tertiary"],
                                      command=lambda u=url: NewsView.open_reader(parent, "Fetching full analysis...", u)).pack(side="left")

        else:
            ctk.CTkLabel(parent.news_list, text="No breaking news found.", text_color=theme["text_secondary"]).pack(pady=20)


        # --- B. CALENDAR (Structured Table with Grid) ---
        for widget in parent.cal_list.winfo_children(): widget.destroy()
        
        if isinstance(cal_events, list) and cal_events:
            # Header logic is static, but rows need grid
            for idx, event in enumerate(cal_events):
                row = ctk.CTkFrame(parent.cal_list, fg_color="transparent")
                row.pack(fill="x", pady=2)
                
                # Localization Check
                lang = parent.env.get("APP_LANG", "EN").upper()
                
                # Grid Layout for Row (MUST MATCH HEADER WEIGHTS EXACTLY)
                if lang == "ID":
                    # MATCH HEADER EXACTLY (Fixed Weights + Spacer)
                    row.grid_columnconfigure(0, weight=0, minsize=80) 
                    row.grid_columnconfigure(1, weight=0, minsize=60) 
                    row.grid_columnconfigure(2, weight=0, minsize=70) 
                    row.grid_columnconfigure(3, weight=0, minsize=50) 
                    row.grid_columnconfigure(4, weight=0, minsize=200) 
                    row.grid_columnconfigure(5, weight=0, minsize=80) 
                    row.grid_columnconfigure(6, weight=0, minsize=60) 
                    row.grid_columnconfigure(7, weight=0, minsize=60) 
                    row.grid_columnconfigure(8, weight=0, minsize=100)
                    row.grid_columnconfigure(9, weight=1) # Spacer
                else:
                    # MATCH HEADER EXACTLY (Fixed Weights + Spacer)
                    row.grid_columnconfigure(0, weight=0, minsize=90) 
                    row.grid_columnconfigure(1, weight=0, minsize=70)
                    row.grid_columnconfigure(2, weight=0, minsize=60)
                    row.grid_columnconfigure(3, weight=0, minsize=250) 
                    row.grid_columnconfigure(4, weight=0, minsize=80)
                    row.grid_columnconfigure(5, weight=0, minsize=70)
                    row.grid_columnconfigure(6, weight=0, minsize=70) 
                    row.grid_columnconfigure(7, weight=0, minsize=110)
                    row.grid_columnconfigure(8, weight=1) # Spacer
                
                # Data Extraction
                date_str = event.get("date", "Today")
                time_str = event.get("time", "All Day")
                curr_str = event.get("currency", "ALL")
                event_str = event.get("event", "Event")
                impact_str = event.get("impact", "Low").upper()
                forecast_str = event.get("forecast", "-")
                
                # Colors
                imp_color = theme["danger"] if "HIGH" in impact_str else (theme["warning"] if "MEDIUM" in impact_str else theme["success"])
                date_color = theme["accent_secondary"] if "Tomorrow" in date_str else theme["text_secondary"]
                
                # Widgets 
                # Widgets 
                if lang == "ID":
                    ctk.CTkLabel(row, text=date_str, font=("Segoe UI", 11), text_color=date_color).grid(row=0, column=0, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=time_str, font=("Consolas", 11), text_color=theme["text_secondary"]).grid(row=0, column=1, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=event.get("time_local", "WIB"), font=("Consolas", 12, "bold"), text_color=theme["text_primary"]).grid(row=0, column=2, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=curr_str, font=("Segoe UI", 12, "bold"), text_color=imp_color).grid(row=0, column=3, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=event_str, font=("Segoe UI", 12), text_color=theme["text_primary"], anchor="w", wraplength=200, justify="left").grid(row=0, column=4, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=impact_str, font=("Segoe UI", 10, "bold"), text_color=imp_color, anchor="center").grid(row=0, column=5, sticky="ew", padx=5)
                    ctk.CTkLabel(row, text=forecast_str, font=("Segoe UI", 12), text_color=theme["text_secondary"]).grid(row=0, column=6, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=event.get("previous", "-"), font=("Segoe UI", 12), text_color="#7F8C8D").grid(row=0, column=7, sticky="w", padx=5)
                    # BRIEFING BUTTON
                    ctk.CTkButton(row, text="🔍 Briefing", width=80, height=24, font=("Segoe UI", 10, "bold"),
                                  fg_color="transparent", border_width=1, border_color="#D4AF37", text_color="#D4AF37",
                                  hover_color=theme["bg_tertiary"], command=lambda e=event: NewsView.handle_briefing(parent, e)).grid(row=0, column=8, sticky="w", padx=5)
                else:
                    ctk.CTkLabel(row, text=date_str, font=("Segoe UI", 11), text_color=date_color).grid(row=0, column=0, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=time_str, font=("Consolas", 12), text_color=theme["text_primary"]).grid(row=0, column=1, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=curr_str, font=("Segoe UI", 12, "bold"), text_color=imp_color).grid(row=0, column=2, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=event_str, font=("Segoe UI", 12), text_color=theme["text_primary"], anchor="w", wraplength=250, justify="left").grid(row=0, column=3, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=impact_str, font=("Segoe UI", 10, "bold"), text_color=imp_color, anchor="center").grid(row=0, column=4, sticky="ew", padx=5)
                    ctk.CTkLabel(row, text=forecast_str, font=("Segoe UI", 12), text_color=theme["text_secondary"]).grid(row=0, column=5, sticky="w", padx=5)
                    ctk.CTkLabel(row, text=event.get("previous", "-"), font=("Segoe UI", 12), text_color="#7F8C8D").grid(row=0, column=6, sticky="w", padx=5)
                    # BRIEFING BUTTON
                    ctk.CTkButton(row, text="🔍 Tactical Brief", width=100, height=24, font=("Segoe UI", 10, "bold"),
                                  fg_color="transparent", border_width=1, border_color="#D4AF37", text_color="#D4AF37",
                                  hover_color=theme["bg_tertiary"], command=lambda e=event: NewsView.handle_briefing(parent, e)).grid(row=0, column=7, sticky="w", padx=5)
                
                # Separator
                ctk.CTkFrame(parent.cal_list, height=1, fg_color=theme["bg_tertiary"]).pack(fill="x")
        else:
             ctk.CTkLabel(parent.cal_list, text="No events detected for today/tomorrow (Check Connectivity).", text_color=theme["text_secondary"]).pack(pady=20)


        # --- C. TECHNICALS (Cards) ---
        # Note: Technicals are now handled incrementally by _fetch_technicals_worker for better performance.
        pass

    @staticmethod
    def handle_briefing(parent, event):
        """Strategic AI Briefing for a specific Economic Event"""
        event_name = event.get("event", "Economic Event")
        currency = event.get("currency", "USD")
        impact = event.get("impact", "Low")
        
        # Open reader immediately with status
        NewsView.open_reader(parent, f"SkyNET is drafting a tactical briefing for {event_name}...", "")
        
        def run_analysis():
            try:
                from index import execute_ai_waterfall
                prompt = (
                    f"Act as an Elite Hedge Fund Trader. Provide a TACTICAL BRIEFING for this event:\n"
                    f"EVENT: {event_name}\n"
                    f"CURRENCY: {currency}\n"
                    f"IMPACT: {impact}\n\n"
                    f"Requirements:\n"
                    f"1. Tactical Scenario (If Actual > Forecast, If Actual < Forecast).\n"
                    f"2. Execution Zones (Order types and suggested ranges).\n"
                    f"3. Risk Warning (Volatility pips expectation).\n"
                    f"Keep it professional, high-end, and concise (Markdown format)."
                )
                
                result = execute_ai_waterfall(
                    feature_key="EVENT_ANALYSIS",
                    prompt=prompt,
                    system_context="You are a senior hedge fund trader providing high-end tactical briefings.",
                    user_api_key=parent.env.get("AI_API_KEY", ""),
                    user_provider=parent.env.get("AI_PROVIDER", "Groq")
                )
                
                # Update Reader on Main Thread
                def update_content():
                    if hasattr(parent, 'reader_content'):
                        parent.reader_content.configure(state="normal")
                        parent.reader_content.delete("1.0", "end")
                        parent.reader_content.insert("0.0", f"SKYNET TACTICAL BRIEFING\n\n{result}")
                        parent.reader_content.configure(state="disabled")
                
                if hasattr(parent, 'safe_ui_update'):
                    parent.safe_ui_update(update_content)
                else:
                    update_content()
            except Exception as e:
                print(f"// Briefing AI Error: {e}")
        
        threading.Thread(target=run_analysis, daemon=True).start()

    @staticmethod
    def handle_header_sort(parent, column_name):
        """Interactive sorting logic (Client-side)"""
        if not hasattr(parent, 'cal_events_data') or not parent.cal_events_data:
            return

        # Mapping UI names to data keys
        mapping = {
            "Date": "_sort_key", "Tgl": "_sort_key",
            "Time": "time", "USA": "time_usa", "WIB": "time_local",
            "Cur": "currency", "Peristiwa": "event", "Event": "event",
            "Impact": "impact", "Dampak": "impact", "Fcst": "forecast"
        }
        
        # Strip indicator if present
        pure_name = column_name.split(" ")[0]
        target_key = mapping.get(pure_name, "date")
        
        # Toggle Sort Direction
        if not hasattr(parent, 'last_sort_col') or parent.last_sort_col != pure_name:
            parent.reverse_sort = False
        else:
            parent.reverse_sort = not parent.reverse_sort
            
        parent.last_sort_col = pure_name
        
        # Perform Sort
        parent.cal_events_data.sort(key=lambda x: str(x.get(target_key, "")).lower(), reverse=parent.reverse_sort)
        
        # Refresh Headers to show ▲/▼
        NewsView._refresh_headers(parent)
        
        # Refresh UI (Thread safe)
        if hasattr(parent, 'safe_ui_update'):
            parent.safe_ui_update(lambda: NewsView.update_ui(parent, None, parent.cal_events_data))
        else:
            NewsView.update_ui(parent, None, parent.cal_events_data)

    @staticmethod
    def _refresh_headers(parent):
        """Redraw headers with Sort Indicators"""
        if not hasattr(parent, 'cal_header_buttons'): return
        
        for btn, name in parent.cal_header_buttons:
            pure_name = name.split(" ")[0]
            display_name = pure_name
            if hasattr(parent, 'last_sort_col') and parent.last_sort_col == pure_name:
                display_name += " ▼" if parent.reverse_sort else " ▲"
            btn.configure(text=display_name)

    @staticmethod
    def open_reader(parent, content, url=""):
        """Displays full article or AI analysis in a premium overlay"""
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        
        # Clear frame
        for widget in parent.reader_frame.winfo_children(): widget.destroy()
        
        # Show Frame
        parent.reader_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Header
        header = ctk.CTkFrame(parent.reader_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(header, text="⬅ BACK", width=80, fg_color="transparent", border_width=1,
                      text_color=theme["text_primary"], border_color=theme["border_default"],
                      command=lambda: parent.reader_frame.place_forget()).pack(side="left", padx=10, pady=10)
                      
        ctk.CTkLabel(header, text="SkyNET Reader", font=("Segoe UI Semibold", 16)).pack(side="left", padx=20)
        
        # Open in Browser
        if url:
            ctk.CTkButton(header, text="🌐 View Article Source", width=140, height=30,
                          fg_color=theme["accent_secondary"], hover_color=theme["accent_primary"],
                          command=lambda: __import__('webbrowser').open(url)).pack(side="right", padx=10)
        
        # Content
        parent.reader_content = ctk.CTkTextbox(parent.reader_frame, font=("Segoe UI", 14), wrap="word",
                                             fg_color="transparent", text_color=theme["text_primary"])
        parent.reader_content.pack(fill="both", expand=True, padx=40, pady=20)
        
        parent.reader_content.insert("0.0", f"NEWS INSIGHT (AI SUMMARIZED)\n\n{content}\n\n[Context generated by SkyNET AI]")
        parent.reader_content.configure(state="disabled")

        # --- Deep Reader: Async Fetch Full Content ---
        if url and "http" in url:
            def fetch_and_update():
                try:
                    import requests
                    from bs4 import BeautifulSoup
                    
                    # Update status - Make it very visible
                    def show_loading():
                         parent.reader_content.configure(state="normal")
                         parent.reader_content.insert("end", "\n\n" + "="*40 + "\n🔄 ACCESSING SOURCE SYSTEM: " + url + "\n⏳ EXTRACTING INTELLIGENCE...\n" + "="*40)
                         parent.reader_content.configure(state="disabled")
                         parent.reader_content.see("end") # Auto-scroll
                    
                    parent.after(100, show_loading)
                    
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                    res = requests.get(url, headers=headers, timeout=5)
                    
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.content, 'html.parser')
                        paragraphs = soup.find_all('p')
                        full_text = "\n\n".join([p.get_text() for p in paragraphs if len(p.get_text()) > 50])
                        
                        if len(full_text) > 500:
                             display_text = full_text[:3000] + ("..." if len(full_text) > 3000 else "")
                             
                             def update_text():
                                 parent.reader_content.configure(state="normal")
                                 current_text = parent.reader_content.get("1.0", "end")
                                 clean_text = current_text.replace("\n\n" + "="*40 + "\n🔄 ACCESSING SOURCE SYSTEM: " + url + "\n⏳ EXTRACTING INTELLIGENCE...\n" + "="*40, "")
                                 parent.reader_content.delete("1.0", "end")
                                 parent.reader_content.insert("0.0", clean_text)
                                 parent.reader_content.insert("end", f"\n\n---\n\n📰 FULL ARTICLE SOURCE:\n\n{display_text}")
                                 parent.reader_content.configure(state="disabled")
                             
                             parent.after(0, update_text)
                        else:
                            raise Exception("Content too short")
                    else:
                        raise Exception(f"HTTP {res.status_code}")
                        
                except Exception as e:
                    error_msg = str(e)
                    def show_error():
                        parent.reader_content.configure(state="normal")
                        parent.reader_content.insert("end", f"\n\n[⚠️ Could not fetch full article: {error_msg}]")
                        parent.reader_content.configure(state="disabled")
                    parent.after(0, show_error)

            threading.Thread(target=fetch_and_update, daemon=True).start()
