import os
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS
from utils.tooltips import CTkToolTip
from modules.ui.ui_helpers import UIHelpers

# --- THEME ---
# --- THEME ---
# REMOVED STATIC THEME

class TradingView:
    """
    Modular class for the Trading Rules page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Trading page and attaches it to the parent (App/GUI)."""
        # Dynamic Theme Loading
        theme = parent.theme_data if hasattr(parent, 'theme_data') else THEME_DARK
        
        page = ctk.CTkScrollableFrame(parent.main_container, fg_color="transparent")
        
        ctk.CTkLabel(page, text=parent.translator.get("trade_title"), font=("Segoe UI Semibold", 22), 
                     text_color=theme["text_primary"], anchor="w").pack(fill="x", pady=(0, 15))
        
        card = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=8)
        card.pack(fill="x")
        
        # Two column layout
        columns = ctk.CTkFrame(card, fg_color="transparent")
        columns.pack(fill="x", padx=20, pady=15)
        columns.columnconfigure((0, 1), weight=1)
        
        # Left column - Position Control
        left = ctk.CTkFrame(columns, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left, text=parent.translator.get("trade_pos_control"), font=FONTS["section_header"],
                     text_color=theme["text_secondary"]).pack(anchor="w", pady=(0, 10))
        
        parent.entry_risk = UIHelpers.create_field_compact(left, "Risk %", os.getenv("RISK_PERCENT", "1.0"), theme)
        CTkToolTip(parent.entry_risk, parent.translator.get("hint_risk_pct"))
        
        parent.entry_lot = UIHelpers.create_field_compact(left, "Fixed Lot", os.getenv("FIXED_LOT", "0.01"), theme)
        CTkToolTip(parent.entry_lot, parent.translator.get("hint_risk_lot"))
        
        parent.entry_magic = UIHelpers.create_field_compact(left, "Magic No", os.getenv("MAGIC_NUMBER", "123456"), theme)
        CTkToolTip(parent.entry_magic, parent.translator.get("hint_risk_magic"))
        
        parent.entry_suffix = UIHelpers.create_field_compact(left, "Suffix", os.getenv("SYMBOL_SUFFIX", ""), theme)
        CTkToolTip(parent.entry_suffix, parent.translator.get("hint_risk_suffix"))
        
        # Auto Execute Checkbox
        # Execution Logic Mode
        parent.execution_mode = ctk.CTkOptionMenu(left, values=["DIRECT (Turbo)", "AI-ASSISTED (Manual)", "AI-FILTER (Auto)"],
                                                fg_color=theme["bg_tertiary"], width=160,
                                                text_color=theme["text_primary"],
                                                button_color=theme["accent_primary"])
        
        # Load initial state from env (Migration logic)
        saved_mode = os.getenv("EXECUTION_MODE")
        if not saved_mode:
            # Fallback for old env: if AUTO_EXECUTE was true -> DIRECT, else AI-ASSISTED
            old_auto = str(os.getenv("AUTO_EXECUTE", "False")).lower() == "true"
            saved_mode = "DIRECT (Turbo)" if old_auto else "AI-ASSISTED (Manual)"
            
        parent.execution_mode.set(saved_mode)
        
        ctk.CTkLabel(left, text="Execution Mode:", font=FONTS["body_bold"], text_color=theme["text_primary"]).pack(anchor="w", pady=(10, 5))
        parent.execution_mode.pack(anchor="w", pady=(0, 5))
        CTkToolTip(parent.execution_mode, 
                   "DIRECT: Eksekusi instan tanpa AI\n"
                   "AI-ASSISTED: Analisa dulu, trade manual\n"
                   "AI-FILTER: Otomatis trade HANYA jika AI Valid")
        
        # Right column - SL/TP Settings  
        right = ctk.CTkFrame(columns, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right, text="🎯 SL/TP OVERRIDE", font=FONTS["section_header"],
                     text_color=theme["text_secondary"]).pack(anchor="w", pady=(0, 10))
        
        # SL/TP Mode Dropdown
        mode_frame = ctk.CTkFrame(right, fg_color="transparent")
        mode_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(mode_frame, text="Mode:", font=FONTS["body"], width=80, text_color=theme["text_primary"]).pack(side="left")
        
        parent.sltp_mode = ctk.CTkOptionMenu(mode_frame, values=["AUTO", "FALLBACK", "OVERRIDE"], 
                                            fg_color=theme["bg_tertiary"], width=140,
                                            text_color=theme["text_primary"],
                                            button_color=theme["accent_primary"])
        parent.sltp_mode.set(os.getenv("SLTP_MODE", "AUTO"))
        parent.sltp_mode.pack(side="left")
        CTkToolTip(parent.sltp_mode, 
                  "AUTO = Ikuti sinyal apa adanya (default)\n"
                  "FALLBACK = Pakai manual HANYA jika sinyal kosong\n"
                  "OVERRIDE = SELALU pakai manual, abaikan sinyal")
        
        # Symbol Type Selector
        sym_frame = ctk.CTkFrame(right, fg_color="transparent")
        sym_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(sym_frame, text="Symbol:", font=FONTS["body"], width=80, text_color=theme["text_primary"]).pack(side="left")
        
        parent.sltp_symbol_type = ctk.CTkOptionMenu(sym_frame, values=["FOREX (EURUSD)", "GOLD (XAUUSD)", "JPY (USDJPY)"], 
                                                   fg_color=theme["bg_tertiary"], width=140,
                                                   text_color=theme["text_primary"],
                                                   button_color=theme["accent_primary"],
                                                   command=parent._update_sltp_preview)
        parent.sltp_symbol_type.set("FOREX (EURUSD)")
        parent.sltp_symbol_type.pack(side="left")
        CTkToolTip(parent.sltp_symbol_type, "Pilih jenis simbol untuk preview harga yang akurat")
        
        # Entry Price
        entry_frame = ctk.CTkFrame(right, fg_color="transparent")
        entry_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(entry_frame, text="Entry:", font=FONTS["body"], width=80, text_color=theme["text_primary"]).pack(side="left")
        
        parent.entry_preview_price = ctk.CTkEntry(entry_frame, width=100, height=32, 
                                                 fg_color=theme["bg_tertiary"], placeholder_text="2000.00", text_color=theme["text_primary"])
        parent.entry_preview_price.pack(side="left")
        parent.entry_preview_price.bind("<KeyRelease>", lambda e: parent._update_sltp_preview())
        CTkToolTip(parent.entry_preview_price, "Masukkan harga entry untuk preview SL/TP")
        
        # Manual SL Pips
        sl_frame = ctk.CTkFrame(right, fg_color="transparent")
        sl_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(sl_frame, text="SL Pips:", font=FONTS["body"], width=80, text_color=theme["text_primary"]).pack(side="left")
        
        parent.entry_sl_pips = ctk.CTkEntry(sl_frame, width=60, height=32, fg_color=theme["bg_tertiary"], text_color=theme["text_primary"])
        parent.entry_sl_pips.insert(0, os.getenv("MANUAL_SL_PIPS", "50"))
        parent.entry_sl_pips.pack(side="left")
        parent.entry_sl_pips.bind("<KeyRelease>", lambda e: parent._update_sltp_preview())
        
        parent.lbl_sl_price = ctk.CTkLabel(sl_frame, text="= ?.?????", font=FONTS["body_small"], 
                                          text_color=theme["accent_danger"], width=100)
        parent.lbl_sl_price.pack(side="left", padx=5)
        
        # Manual TP Pips
        tp_frame = ctk.CTkFrame(right, fg_color="transparent")
        tp_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(tp_frame, text="TP Pips:", font=FONTS["body"], width=80, text_color=theme["text_primary"]).pack(side="left")
        
        parent.entry_tp_pips = ctk.CTkEntry(tp_frame, width=60, height=32, fg_color=theme["bg_tertiary"], text_color=theme["text_primary"])
        parent.entry_tp_pips.insert(0, os.getenv("MANUAL_TP_PIPS", "100"))
        parent.entry_tp_pips.pack(side="left")
        parent.entry_tp_pips.bind("<KeyRelease>", lambda e: parent._update_sltp_preview())
        
        parent.lbl_tp_price = ctk.CTkLabel(tp_frame, text="= ?.?????", font=FONTS["body_small"], 
                                          text_color=theme["accent_success"], width=100)
        parent.lbl_tp_price.pack(side="left", padx=5)
        
        # Warning and Hint
        ctk.CTkLabel(right, text="💡 Masukkan Entry price untuk preview SL/TP aktual",
                     font=FONTS["body_small"], text_color=theme["text_disabled"], 
                     wraplength=250, justify="left").pack(anchor="w", pady=(5, 0))
        ctk.CTkLabel(right, text="⚠️ OVERRIDE mengabaikan SL/TP sinyal!",
                     font=FONTS["body_small"], text_color=theme["accent_warning"], 
                     wraplength=250, justify="left").pack(anchor="w", pady=(2, 0))
        
        # Actions
        # --- QUICK LOAD VAULT ---
        loader_frame = ctk.CTkFrame(card, fg_color="transparent")
        loader_frame.pack(fill="x", pady=(15, 5), padx=20)
        
        ctk.CTkLabel(loader_frame, text="⚡ Quick Load:", font=FONTS["body_small"], 
                     text_color=theme["text_secondary"]).pack(side="left")
        
        parent.preset_var = ctk.StringVar(value="Select Preset...")
        parent.preset_menu = ctk.CTkOptionMenu(loader_frame, variable=parent.preset_var, values=["Loading..."], width=200,
                                              fg_color=theme["bg_secondary"], button_color=theme["accent_primary"],
                                              text_color="white")
        parent.preset_menu.pack(side="left", padx=10, expand=True, fill="x")
        
        def _quick_load():
            name = parent.preset_var.get()
            if not name or name == "Select Preset..." or name == "Loading...": return
            
            # Find data
            if hasattr(parent, 'cached_presets'):
                target = next((p for p in parent.cached_presets if p['name'] == name), None)
                if target:
                    from modules.logic.config_aggregator import ConfigAggregator
                    from CTkMessagebox import CTkMessagebox
                    if ConfigAggregator.apply_config_dict(parent, target['config_json']):
                        CTkMessagebox(title="Loaded", message=f"Applied '{name}' settings!", icon="check")
        
        ctk.CTkButton(loader_frame, text="APPLY", width=80, height=32, fg_color="#3498db", command=_quick_load).pack(side="right")

        # Trigger Refresh
        TradingView._refresh_quick_load(parent)

        btn_grid = ctk.CTkFrame(card, fg_color="transparent")
        btn_grid.pack(fill="x", pady=15, padx=20)
        
        # Local Save
        ctk.CTkButton(btn_grid, text="💾 " + parent.translator.get("settings_save"), font=FONTS["button"],
                      fg_color=theme["accent_success"], height=40, text_color="white", width=200,
                      command=parent.save_config).pack(side="left", padx=5, expand=True, fill="x")

        # Vault Save
        ctk.CTkButton(btn_grid, text="☁️ MINT / SAVE PRESET", font=FONTS["button"],
                      fg_color=theme["accent_primary"], height=40, text_color="white", width=200,
                      command=lambda: TradingView._save_preset_logic(parent)).pack(side="right", padx=5, expand=True, fill="x")
        
        return page

    @staticmethod
    def _refresh_quick_load(parent):
        """Fetches user presets and updates the Quick Load dropdown"""
        def _task():
            if hasattr(parent, 'db_manager'):
                 presets = parent.db_manager.get_user_presets()
                 parent.cached_presets = presets # Cache for quick lookup
                 names = [p['name'] for p in presets]
                 
                 def _update():
                     try:
                         if not parent.winfo_exists(): return
                         if hasattr(parent, 'preset_menu'):
                             parent.preset_menu.configure(values=names if names else ["(Empty Vault)"])
                             if names: parent.preset_var.set(names[0])
                             else: parent.preset_var.set("(Empty Vault)")
                     except: pass
                 
                 try:
                     parent.after(0, _update)
                 except: pass
        
        import threading
        threading.Thread(target=_task, daemon=True).start()

    @staticmethod
    def _save_preset_logic(parent):
        """Captures current settings and saves to Cloud Vault using Publisher Studio"""
        # Lazy import or ensure ConfigAggregator is available
        from modules.logic.config_aggregator import ConfigAggregator
        from CTkMessagebox import CTkMessagebox
        from modules.ui.publisher_dialog import PublisherDialog
        
        # 1. Open Publisher Studio
        dialog = PublisherDialog(parent)
        data = dialog.get_input()
        
        if not data: return # User cancelled
            
        # 2. Capture Logic
        cfg = ConfigAggregator.get_current_config_dict(parent)
        if not cfg:
             CTkMessagebox(title="Error", message="Failed to capture config!", icon="cancel")
             return
             
        # 3. Save to Cloud
        if hasattr(parent, 'db_manager'):
            success, msg = parent.db_manager.save_user_preset(
                name=data['name'], 
                description=data['description'], 
                config_data=cfg,
                is_public=data['is_public'],
                price=data['price']
            )
            
            if success:
                from modules.ui.leaderboard_view import LeaderboardView
                LeaderboardView.refresh_vault(parent)
                
                mode_txt = "Public Store" if data['is_public'] else "My Presets"
                CTkMessagebox(title="Mint Success", message=f"Asset '{data['name']}' minted to {mode_txt}!", icon="check")
            else:
                CTkMessagebox(title="Mint Failed", message=msg, icon="cancel")
        else:
             CTkMessagebox(title="Error", message="Database not connected!", icon="cancel")

    @staticmethod
    def update_sltp_preview(parent, *args):
        """Logic to calculate SL/TP price previews based on pips."""
        try:
            entry = float(parent.entry_preview_price.get())
            sl_pips = float(parent.entry_sl_pips.get())
            tp_pips = float(parent.entry_tp_pips.get())
            
            sym_type = parent.sltp_symbol_type.get()
            
            # Pip value calculation
            if "GOLD" in sym_type:
                pip_val = 0.1 # Real pips for Gold
            elif "JPY" in sym_type:
                pip_val = 0.01 
            else:
                pip_val = 0.0001 # Standard Forex
            
            # Simplified preview (Assume BUY for preview)
            sl_price = entry - (sl_pips * pip_val)
            tp_price = entry + (tp_pips * pip_val)
            
            fmt = "%.2f" if "GOLD" in sym_type or "JPY" in sym_type else "%.5f"
            parent.lbl_sl_price.configure(text=f"= {fmt % sl_price}")
            parent.lbl_tp_price.configure(text=f"= {fmt % tp_price}")
            
        except:
            parent.lbl_sl_price.configure(text="= ?.?????")
            parent.lbl_tp_price.configure(text="= ?.?????")
