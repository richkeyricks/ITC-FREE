import os
import threading
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS as LEGACY_FONTS
from ui_theme_modern import get_theme as get_modern_theme, FONTS as MODERN_FONTS
from CTkMessagebox import CTkMessagebox

# --- HELPER ---
def get_current_theme_data(parent):
    if hasattr(parent, 'selected_theme') and parent.selected_theme in ["light", "neutral"]:
        return get_modern_theme(parent.selected_theme), MODERN_FONTS
    return THEME_DARK, LEGACY_FONTS

class SPCHubView:
    """
    Modular class for the Signal Provider CopyTrade (SPC) Hub.
    Exclusive for VIP users.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the SPC Hub page."""
        theme, fonts = get_current_theme_data(parent)
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        # Header
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header, text=parent.translator.get("spc_title"), 
                     font=fonts.get("header_large", ("Segoe UI Bold", 24)), text_color=theme["accent_warning"]).pack(anchor="w")
        ctk.CTkLabel(header, text=parent.translator.get("spc_desc"), 
                     font=fonts["body_small"], text_color=theme["text_secondary"]).pack(anchor="w")
        
        main_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        main_scroll.pack(fill="both", expand=True)

        # VIP Check Overlay
        def check_vip():
            theme, fonts = get_current_theme_data(parent)
            # Grant access if user is VIP OR Admin
            is_admin = hasattr(parent, 'db_manager') and parent.db_manager.is_admin()
            if not getattr(parent, "is_vip", False) and not is_admin:
                overlay_color = "#1a1d23" if theme["appearance_mode"] == "Dark" else "#ffffff"
                overlay = ctk.CTkFrame(page, fg_color=overlay_color)
                overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
                
                # --- PREMIUM LOCK SCREEN (Unified Design) ---
                container = ctk.CTkFrame(overlay, fg_color="transparent")
                container.place(relx=0.5, rely=0.5, anchor="center")
                
                # 1. Lock Icon
                ctk.CTkLabel(container, text="🔒", font=("Segoe UI", 80)).pack(pady=(0, 20))
                
                # 2. Title
                title_text = parent.translator.get("lock_title_spc") if hasattr(parent, 'translator') else "PLATINUM FEATURE LOCKED"
                ctk.CTkLabel(container, text=title_text, 
                             font=("Segoe UI", 24, "bold"), 
                             text_color=theme["accent_warning"]).pack(pady=(0, 10))
                
                # 3. Subtitle / Description
                msg = parent.translator.get("lock_msg_spc") if hasattr(parent, 'translator') else "This feature is exclusive to Platinum Members."
                ctk.CTkLabel(container, text=msg, 
                             font=("Segoe UI", 14), 
                             text_color=theme["text_primary"],
                             justify="left").pack(pady=(0, 30))
                
                # 4. Premium Badge / Divider
                divider = ctk.CTkFrame(container, height=2, width=200, fg_color=theme["bg_tertiary"])
                divider.pack(pady=(0, 30))
                
                # 5. Call to Action Button
                btn_text = parent.translator.get("btn_upgrade_platinum") if hasattr(parent, 'translator') else "UPGRADE TO PLATINUM 💎"
                
                def open_subs():
                    if hasattr(parent, 'show_page'):
                        parent.show_page("subscription")
                
                ctk.CTkButton(container, text=btn_text, 
                              font=("Segoe UI", 13, "bold"),
                              height=40, width=220,
                              fg_color=theme["accent_warning"],
                              hover_color="#d97706", # Amber-600
                              text_color="white" if theme["appearance_mode"] == "Dark" else "black",
                              command=open_subs).pack()

        parent.safe_ui_update(check_vip)

        # --- AI PARSING ALERT ---
        alert_box = ctk.CTkFrame(main_scroll, fg_color="#332a00", border_color="#ffcc00", border_width=1, corner_radius=8)
        alert_box.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(alert_box, text="⚠️ CRITICAL: AI PARSING REQUIRED", 
                     font=fonts["body_bold"], text_color="#ffcc00").pack(anchor="w", padx=15, pady=(10, 0))
        
        ctk.CTkLabel(alert_box, text="Untuk Format 'Institutional' & 'ICT', Anda WAJIB mengaktifkan 'AI Parsing' di Tab Telegram.\nFormat kompleks ini TIDAK BISA dibaca oleh Regex biasa.", 
                     font=fonts["body_small"], text_color=theme["text_primary"], justify="left").pack(anchor="w", padx=15, pady=(5, 10))


        # --- SETTINGS FORM ---
        form = ctk.CTkFrame(main_scroll, fg_color=theme["bg_secondary"], corner_radius=12, border_width=1, border_color=theme["border_default"])
        form.pack(fill="x", pady=10)
        
        inner = ctk.CTkFrame(form, fg_color="transparent")
        inner.pack(padx=20, pady=20, fill="both")

        # Mode Selection
        ctk.CTkLabel(inner, text=parent.translator.get("spc_mode"), font=fonts["body_bold"], text_color=theme["text_primary"]).pack(anchor="w")
        parent.combo_spc_mode = ctk.CTkComboBox(inner, values=[
            parent.translator.get("spc_mode_relay"),
            parent.translator.get("spc_mode_mt5")
        ], height=35)
        parent.combo_spc_mode.pack(fill="x", pady=(5, 15))
        parent.combo_spc_mode.set(parent.translator.get("spc_mode_relay"))

        # Bot Token
        ctk.CTkLabel(inner, text=parent.translator.get("spc_bot_token"), font=fonts["body_bold"], text_color=theme["text_primary"]).pack(anchor="w")
        parent.entry_spc_token = ctk.CTkEntry(inner, placeholder_text="123456:ABC-DEF...", height=35)
        parent.entry_spc_token.pack(fill="x", pady=(5, 15))
        parent.entry_spc_token.insert(0, os.getenv("SPC_BOT_TOKEN", ""))

        # Chat ID
        ctk.CTkLabel(inner, text=parent.translator.get("spc_chat_id"), font=fonts["body_bold"], text_color=theme["text_primary"]).pack(anchor="w")
        parent.entry_spc_chat_id = ctk.CTkEntry(inner, placeholder_text="-100123456789", height=35)
        parent.entry_spc_chat_id.pack(fill="x", pady=(5, 15))
        parent.entry_spc_chat_id.insert(0, os.getenv("SPC_CHAT_ID", ""))

        # Agency Brand Name (White Label)
        ctk.CTkLabel(inner, text="Agency Brand Name (VIP Header)", font=fonts["body_bold"], text_color=theme["text_primary"]).pack(anchor="w")
        parent.entry_spc_brand = ctk.CTkEntry(inner, placeholder_text="e.g. NAGA FX ACADEMY", height=35)
        parent.entry_spc_brand.pack(fill="x", pady=(5, 15))
        parent.entry_spc_brand.insert(0, os.getenv("SPC_BRAND_NAME", ""))

        # Watermark Toggle
        parent.check_spc_watermark = ctk.CTkCheckBox(inner, text=parent.translator.get("spc_watermark"), 
                                                   font=fonts["body"], text_color=theme["text_secondary"],
                                                   fg_color=theme["accent_primary"])
        parent.check_spc_watermark.pack(anchor="w", pady=(0, 15))
        if os.getenv("SPC_USE_WATERMARK") == "True":
            parent.check_spc_watermark.select()

        # Template Selection
        ctk.CTkLabel(inner, text=parent.translator.get("spc_template"), font=fonts["body_bold"], text_color=theme["text_primary"]).pack(anchor="w")
        parent.combo_spc_template = ctk.CTkComboBox(inner, values=["Loading..."], height=35, command=lambda e: SPCHubView._update_preview(parent))
        parent.combo_spc_template.pack(fill="x", pady=(5, 15))

        # Preview Area
        ctk.CTkLabel(inner, text=parent.translator.get("spc_preview"), font=fonts["body_bold"], text_color=theme["text_secondary"]).pack(anchor="w")
        parent.text_spc_preview = ctk.CTkTextbox(inner, height=150, font=fonts["body"], fg_color=theme["bg_primary"], text_color=theme["text_primary"], border_width=1, border_color=theme["border_default"])
        parent.text_spc_preview.pack(fill="x", pady=(5, 15))
        parent.text_spc_preview.configure(state="disabled")

        # Control Buttons
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x")
        
        parent.btn_spc_start = ctk.CTkButton(btn_row, text=parent.translator.get("spc_start"), fg_color=theme["btn_success_bg"], hover_color=theme["btn_success_hover"], 
                                             height=40, font=fonts.get("button", ("Segoe UI Bold", 13)), command=lambda: SPCHubView.toggle_bridge(parent))
        parent.btn_spc_start.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        def list_on_market():
            from modules.logic.marketplace_service import MarketplaceService
            from CTkMessagebox import CTkMessagebox
            
            title = parent.entry_spc_brand.get() or "Verified Signal"
            cid = parent.entry_spc_chat_id.get()
            
            if not cid:
                CTkMessagebox(title="Error", message="Enter Chat ID first!", icon="cancel")
                return
                
            success, msg = MarketplaceService.publish_signal_flow(title, cid, 500000) # Price Default 500k
            if success:
                CTkMessagebox(title="Quantum Success", message=msg, icon="check")
            else:
                CTkMessagebox(title="Quantum Locked", message=msg, icon="warning")

        ctk.CTkButton(btn_row, text="💎 LIST ON MARKETPLACE", fg_color="#f59e0b", hover_color="#d97706",
                      text_color="black",
                      height=40, width=150, command=list_on_market).pack(side="left")

        # Load Presets
        parent.after(500, lambda: SPCHubView._load_presets(parent))
        
        return page

    @staticmethod
    def _load_presets(parent):
        """Fetches presets from DB and updates dropdown"""
        
        # --- 10 HARDCODED VIP PRESETS ---
        vip_presets = {
            # --- TIER 1: THE "GOD MODE" TEMPLATE (Full Institutional) ---
            "01. QUANT HEDGE FUND (Titan)": """╔══════════════════════════════════════════════════════╗
║ 🚀 {BRAND_NAME} - INSTITUTIONAL SMART SIGNAL                       ║
╚══════════════════════════════════════════════════════╝

SYMBOL        : {SYMBOL}
TIMEFRAME     : {TIMEFRAME}
SESSION       : {SESSION}
SIGNAL TIME   : {SIGNAL_TIME}
SIGNAL AGE    : 0 Bars (Fresh Signal)

──────────────────────────────────────────────────────
📌 TRADE SETUP
──────────────────────────────────────────────────────
DIRECTION     : {TYPE}
ENTRY PRICE   : {ENTRY}

STOP LOSS     : {SL}   ({SL_PIPS})

TAKE PROFIT
• TP1         : {TP1}   ({TP1_PIPS})
• TP2         : {TP2}   ({TP2_PIPS})
• TP3         : {TP3}

──────────────────────────────────────────────────────
🎯 AI PROBABILITY & ACCURACY ENGINE
──────────────────────────────────────────────────────
BUY PROB      : {PROB_BUY}
SELL PROB     : {PROB_SELL}

SIGNAL POWER  : {SIGNAL_POWER}
CONFIDENCE    : {CONFIDENCE_SCORE}

TP HIT PROBABILITY (AI MODEL)
• TP1         : {PROB_TP1}
• TP2         : {PROB_TP2}
• TP3         : {PROB_TP3}

──────────────────────────────────────────────────────
🧠 SIGNAL INTELLIGENCE (WHY THIS TRADE)
──────────────────────────────────────────────────────
{ANALYSIS_REASON}

──────────────────────────────────────────────────────
📰 NEWS & FUNDAMENTAL CONTEXT
──────────────────────────────────────────────────────
UPCOMING HIGH IMPACT (≤ 2 HOURS)
{NEWS_CONTEXT}

NEWS BIAS
{NEWS_BIAS}

──────────────────────────────────────────────────────
💼 ACCOUNT & RISK SIMULATION
──────────────────────────────────────────────────────
ACCOUNT BALANCE   : {ACC_BAL}
RISK PER TRADE    : {RISK_PERCENT} ({RISK_USD})

OUTCOME SIMULATION
• TP1 HIT         : {SIM_WIN_TP1}
• TP2 HIT         : {SIM_WIN_TP2}
• STOP LOSS HIT   : {SIM_LOSS}

──────────────────────────────────────────────────────
⚠️ WORST-CASE LOSS SCENARIO
──────────────────────────────────────────────────────
CONDITION      : {WC_CONDITION}
SLIPPAGE       : {WC_SLIPPAGE}
MAX LOSS EST   : {WC_MAX_LOSS}

DAILY DD STATE : {DD_STATE}

──────────────────────────────────────────────────────
📊 HISTORICAL AI PERFORMANCE
──────────────────────────────────────────────────────
TOTAL SIGNALS      : {TOTAL_SIGNALS}
WIN / LOSS         : {WIN_LOSS_RATIO}
SUCCESS RATE      : {WIN_RATE}

LAST 30 SIGNALS
• WIN RATE         : {LAST30_WINRATE}
• AVG R:R          : {LAST30_RR}
• MAX DRAWDOWN     : {LAST30_DD}
• NET GROWTH       : {LAST30_GROWTH}

SIGNAL RATING      : {SIGNAL_RATING}

──────────────────────────────────────────────────────
✅ FINAL AI DECISION MATRIX
──────────────────────────────────────────────────────
TRADE STATUS   : {MATRIX_STATUS}
RISK LEVEL     : {MATRIX_RISK}
EXECUTION      : {MATRIX_EXEC}

AVOID TRADE IF
{MATRIX_AVOID}

──────────────────────────────────────────────────────
🔐 SYSTEM NOTE
──────────────────────────────────────────────────────
This signal is generated using multi-factor AI probability
aggregation, historical performance weighting, and
real-time market context — not single-indicator logic.

╔══════════════════════════════════════════════════════╗
║  🚀 {BRAND_NAME} - INSTITUTIONAL SMART SIGNAL                      ║
╚══════════════════════════════════════════════════════╝""",

            # --- TIER 2: HIGH FREQUENCY SCALP (For Fast Action) ---
            "02. INSTITUTIONAL SCALP (Sniper)": """⚡ **{BRAND_NAME} SNIPER ALERT - {TYPE} {SYMBOL}** ⚡
⏳ *{SIGNAL_TIME} | {SESSION}*

🎯 **ENTRY:** `{ENTRY}`
🛑 **STOP:** `{SL}` ({SL_PIPS})

✅ **TARGETS**
1️⃣ `{TP1}` ({PROB_TP1} Win Chance)
2️⃣ `{TP2}`
3️⃣ `{TP3}` (Runner)

📊 **AI CONFIDENCE:** {CONFIDENCE_SCORE}
🛡️ **RISK REWARD:** {RR_RATIO}

📝 **LOGIC:**
{ANALYSIS_REASON}

⚠️ **MATRIX:** {MATRIX_STATUS} | **RISK:** {MATRIX_RISK}""",

            # --- TIER 3: PRIVATE WEALTH (Clean/Elegant) ---
            "03. PRIVATE WEALTH (Alpha)": """🏛️ **{BRAND_NAME} PRIVATE WEALTH**
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
**{SYMBOL}** | **{TYPE}** @ **{ENTRY}**
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

📍 **EXIT PLAN**
• Target 1  : **{TP1}**
• Target 2  : **{TP2}**
• Stop Loss : **{SL}**

📉 **AI PROBABILITY MATRIX**
• Success Rate : **{PROB_TP1}**
• Drawdown Est : **{WC_MAX_LOSS}** (Worst Case)
• Signal Power : **{SIGNAL_POWER}**

💎 *Institutional data provided by {BRAND_NAME} Alpha Engine*""",

            "02. MINIMALIST (Clean)": """// ITC SIGNAL //
Symbol: {SYMBOL}
Action: {TYPE}
Entry: {ENTRY}

⛔ SL: {SL}
✅ TP1: {TP1}
✅ TP2: {TP2}
✅ TP3: {TP3}

Risk: 1% | Trade Safe.""",

            "03. SCALPER EMOJI (Fast)": """🚀🚀 **SCALP ALERT** 🚀🚀
💎 **{SYMBOL}** | **{TYPE}** NOW!
Entry: {ENTRY}

❌ STOP: {SL}
💰 TP1: {TP1}
💰 TP2: {TP2}
💰 TP3: {TP3}

⚡⚡ GAS KAN! ⚡⚡""",

            "04. ICT STRUCTURE (Smart Money)": """🏛️ **ICT MARKET STRUCTURE**
Asset: {SYMBOL}
Bias: {TYPE} (Order Block Rejection)
Zone: {ENTRY}

🛡️ Invalidation (SL): {SL}
🎯 Liquidity Run (TP1): {TP1}
🎯 FV Gap Fill (TP2): {TP2}
🎯 Structural High (TP3): {TP3}

*Institutional Flow Detected*""",

            "05. NEON CYBERPUNK": """❚█══ **CYBER SIGNAL V.2** ══█❚
│ 💠 HOST: {SYMBOL}
│ 💠 CMD: {TYPE}
│ 💠 EXE: {ENTRY}
│
│ 🛑 TERMINATE: {SL}
│ 🟢 TARGET_A: {TP1}
│ 🟢 TARGET_B: {TP2}
│ 🟢 TARGET_C: {TP3}
❚█═══════════════════════════█❚""",

            "06. CORPORATE BLUE": """🟦 **ITC PRO SIGNALS** 🟦
-----------------------------
Symbol  : {SYMBOL}
Order   : {TYPE}
Price   : {ENTRY}
-----------------------------
SL      : {SL}
-----------------------------
TP 1    : {TP1}
TP 2    : {TP2}
TP 3    : {TP3}
-----------------------------
*Professional Execution Only*""",

            "07. GOLD SPECIALIST (XAU Only)": """🏆 **GOLD KING SETUP** 🏆
XAUUSD -> {TYPE}
Area: {ENTRY}

SL: {SL} (30-50 pips)
TP1: {TP1} (Scalp)
TP2: {TP2} (Intraday)
TP3: {TP3} (Swing)

✨ *Follow The Trend* ✨""",

            "08. SMART PIPS (R:R Focus)": """📊 **TRADE OPPORTUNITY**
{SYMBOL} - {TYPE}
@ {ENTRY}

Risk  : {SL} (1R)
Reward: 
  + {TP1} (1.5R)
  + {TP2} (2.5R)
  + {TP3} (4.0R)

Recommended Risk: 1-2%""",

            "09. SWING WARRIOR (Multiday)": """🗡️ **SWING POSITION** 🗡️
Pair: {SYMBOL}
View: {TYPE} (H4/D1)
Entry: {ENTRY}

Stoploss: {SL} (Wide)
Target 1: {TP1}
Target 2: {TP2}
Target 3: {TP3} (Open)

*Hold for days. Be patient.*""",

            "10. CLASSIC TELEGRAM": """{SYMBOL} {TYPE} NOW
@{ENTRY}

SL {SL}
TP {TP1}
TP {TP2}
TP {TP3}"""
        }

        parent.spc_presets = vip_presets
        
        def update_ui():
            names = list(parent.spc_presets.keys())
            parent.combo_spc_template.configure(values=names)
            parent.combo_spc_template.set(names[0])
            SPCHubView._update_preview(parent)
        
        parent.safe_ui_update(update_ui)

    @staticmethod
    def _update_preview(parent):
        """Updates the preview text box based on selected preset"""
        preset_name = parent.combo_spc_template.get()
        template = parent.spc_presets.get(preset_name, "")
        
        sample_signal = {
            "symbol": "XAUUSD",
            "type": "BUY",
            "entry": "2025.50",
            "sl": "2020.00",
            "tp1": "2035.00",
            "tp2": "2045.00",
            "tp3": "2060.00"
        }
        
        try:
            preview = template.format(
                SYMBOL=sample_signal["symbol"],
                TYPE=sample_signal["type"],
                ENTRY=sample_signal["entry"],
                SL=sample_signal["sl"],
                TP1=sample_signal["tp1"],
                TP2=sample_signal["tp2"],
                TP3=sample_signal["tp3"]
            )
        except:
            preview = template

        parent.text_spc_preview.configure(state="normal")
        parent.text_spc_preview.delete("1.0", "end")
        parent.text_spc_preview.insert("1.0", preview)
        parent.text_spc_preview.configure(state="disabled")

    @staticmethod
    def toggle_bridge(parent):
        """Starts or stops the Signal Bridge relay"""
        if not getattr(parent, "spc_running", False):
            # Validate
            token = parent.entry_spc_token.get().strip()
            chat_id = parent.entry_spc_chat_id.get().strip()
            if not token or not chat_id:
                CTkMessagebox(title="Error", message="Please enter Bot Token and Chat ID.", icon="warning")
                return
            
            parent.spc_running = True
            parent.btn_spc_start.configure(text=parent.translator.get("spc_stop"), fg_color="#dc3545")
            
            mode_text = parent.combo_spc_mode.get()
            is_mt5_mode = mode_text == parent.translator.get("spc_mode_mt5")
            
            token = parent.entry_spc_token.get().strip()
            chat_id = parent.entry_spc_chat_id.get().strip()
            brand = parent.entry_spc_brand.get().strip()
            
            os.environ["SPC_BOT_TOKEN"] = token
            os.environ["SPC_CHAT_ID"] = chat_id
            os.environ["SPC_BRAND_NAME"] = brand # Save for persistence
            os.environ["SPC_USE_WATERMARK"] = "True" if parent.check_spc_watermark.get() else "False"
            
            # Save to .env file for restart persistence
            try:
                from dotenv import set_key
                set_key(".env", "SPC_BOT_TOKEN", token)
                set_key(".env", "SPC_CHAT_ID", chat_id)
                set_key(".env", "SPC_BRAND_NAME", brand)
                set_key(".env", "SPC_USE_WATERMARK", os.environ["SPC_USE_WATERMARK"])
            except: pass

            parent.spc_config = {
                "bot_token": token,
                "chat_id": chat_id,
                "template": parent.spc_presets.get(parent.combo_spc_template.get()),
                "use_watermark": parent.check_spc_watermark.get(),
                "brand_name": brand if brand else "INSTITUTIONAL SIGNAL" 
            }
            
            print(f"// SPC Service Started. White Label: {parent.spc_config['brand_name']}")
            os.environ["SPC_TEMPLATE"] = parent.spc_presets.get(parent.combo_spc_template.get(), "")
            os.environ["SPC_MODE"] = "BROADCAST" if is_mt5_mode else "RELAY"
            # os.environ["SPC_USE_WATERMARK"] = str(parent.check_spc_watermark.get()) # This line is now redundant due to the new logic above

            parent.log("INFO", f"💎 SPC Bridge Started: Mode={os.environ['SPC_MODE']}")
        else:
            parent.spc_running = False
            os.environ["SPC_BOT_TOKEN"] = ""
            os.environ["SPC_CHAT_ID"] = ""
            parent.btn_spc_start.configure(text=parent.translator.get("spc_start"), fg_color=theme["btn_success_bg"], hover_color=theme["btn_success_hover"])
            parent.log("INFO", "🛑 SPC Bridge Stopped.")

