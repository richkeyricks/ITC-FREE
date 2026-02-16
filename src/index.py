import os
import re
# import MetaTrader5 as mt5 # REMOVED: Direct use unsafe
from modules.mt5.mt5_service import MT5Service # ADDED: Thread-safe Service
import csv
from datetime import datetime
import hashlib
import requests
import json
# import google.generativeai as genai # REMOVED: Unused and breaks Slim Build
from groq import Groq
import time
import threading
from pyrogram import Client, filters
from dotenv import load_dotenv
from modules.logic.bridge_controller import BridgeController

# --- SYNCHRONIZATION ---
cache_lock = threading.Lock()
LAST_SIGNAL_SOURCE = "Manual/System"

# --- CLOUD INTEGRATION ---
from modules.db.supabase_client import SupabaseManager
db_manager = SupabaseManager()

# --- CONFIGURATION ---
load_dotenv()
import socket

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# --- GLOBAL STATE FOR UI ---
is_telegram_active = False 
is_telegram_validated = False # True if test connection passed or session exists
is_telegram_failed = False    # True if a live test just failed

def get_mt5_status_deep():
    """
    3-State MT5 Check: 
    Result: 0=RED (Offline), 1=YELLOW (Standby/No Account), 2=GREEN (Logged In)
    """
    service = MT5Service.instance()
    
    # 1. Check Terminal Connectivity (Thread-Safe)
    if not service.initialize():
        return 0
        
    t_info = service.get_terminal_info()
    if not t_info or not t_info.connected:
        return 0 # Terminal might be open but disconnected from MT5 network
        
    # 2. Check Account Info
    a_info = service.get_account_info()
    if not a_info:
        return 1 # Standby: Terminal is OK, but no account logged in
        
    return 2 # Fully Connected & Logged In

def check_telegram_session():
    """Checks if Telegram session file exists (Authorized)"""
    # Check common locations for itc_copier_session
    possible = [
        "itc_copier_session.session",
        "src/itc_copier_session.session",
        os.path.join(os.path.dirname(__file__), "itc_copier_session.session")
    ]
    for p in possible:
        if os.path.exists(p): return True
    return False

def get_mt5_status():
    """Checks if MT5 is initialized and connected to a terminal."""
    # Legacy fallback for older code, but uses deep check
    return get_mt5_status_deep() == 2

def get_account_meta():
    """Gets balance, equity, and historical loss/profit if MT5 is ready."""
    service = MT5Service.instance()
    if not service.initialize():
        return {"balance": 0.0, "equity": 0.0, "profit": 0.0, "total_pl": 0.0}
    
    acc = service.get_account_info()
    if acc:
        # Calculate historical P/L (Total Gain/Loss)
        from_date = datetime(2020, 1, 1)
        to_date = datetime.now()
        deals = service.history_deals_get(from_date, to_date)
        total_pl = sum([d.profit for d in deals]) if deals else 0.0
        
        # --- GOD MODE METRIC ADDITION ---
        last_trade_pair = "N/A"
        last_trade_type = "N/A"
        last_trade_lot = 0.0
        last_trade_profit = 0.0
        
        if deals:
            # Sort by time desc to get actual last deal
            sorted_deals = sorted(deals, key=lambda x: x.time, reverse=True)
            for d in sorted_deals:
                if d.entry == service.DEAL_ENTRY_OUT: # Only closing deals count as "history"
                    last_trade_pair = d.symbol
                    last_trade_type = "BUY" if d.type == service.DEAL_TYPE_BUY else "SELL"
                    last_trade_lot = d.volume
                    last_trade_profit = d.profit
                    break
                    
        # --- ADVANCED METRICS (Derived) ---
        total_deals = 0
        total_volume = 0.0
        wins = 0
        losses = 0
        total_win_val = 0.0
        total_loss_val = 0.0
        
        if deals:
            closing_deals = [d for d in deals if d.entry == service.DEAL_ENTRY_OUT]
            total_deals = len(closing_deals)
            for d in closing_deals:
                total_volume += d.volume
                if d.profit >= 0:
                    wins += 1
                    total_win_val += d.profit
                else:
                    losses += 1
                    total_loss_val += d.profit
        
        win_rate = (wins / total_deals * 100) if total_deals > 0 else 0.0
        avg_win = (total_win_val / wins) if wins > 0 else 0.0
        avg_loss = (total_loss_val / losses) if losses > 0 else 0.0
        
        # Drawdown Calculation (Current)
        drawdown_pct = 0.0
        if acc.balance > 0:
            drawdown_pct = ((acc.balance - acc.equity) / acc.balance) * 100
                    
        return {
            "balance": acc.balance, 
            "equity": acc.equity, 
            "profit": acc.profit,      # Live P/L
            "total_pl": total_pl,      # Historical P/L
            "margin_level": acc.margin_level,
            "margin_free": acc.margin_free,
            "last_trade_pair": last_trade_pair,
            "last_trade_type": last_trade_type,
            "last_trade_lot": last_trade_lot,
            "last_trade_profit": last_trade_profit,
            "signal_source": LAST_SIGNAL_SOURCE,
            "Broker": acc.company,
            "Account": str(acc.login),
            
            # Derived Metrics
            "win_rate": round(win_rate, 2),
            "total_deals": total_deals,
            "total_volume": round(total_volume, 2),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "drawdown_pct": round(drawdown_pct, 2)
        }
    return {
        "balance": 0.0, "equity": 0.0, "profit": 0.0, "total_pl": 0.0,
        "margin_level": 0.0, "margin_free": 0.0,
        "last_trade_pair": "N/A", "last_trade_type": "N/A", 
        "last_trade_lot": 0.0, "last_trade_profit": 0.0, 
        "signal_source": "Offline",
        "Broker": "Offline",
        "Account": "0",
        "win_rate": 0.0, "total_deals": 0, "total_volume": 0.0,
        "avg_win": 0.0, "avg_loss": 0.0, "drawdown_pct": 0.0
    }

def get_env_list():
    """Refreshes and returns all current env variables with safety fallbacks"""
    load_dotenv(override=True)
    
    def safe_int(val, default=0):
        try:
            if not val: return default
            # Handle comma-separated or dirty strings
            return int(str(val).split(',')[0].strip())
        except: return default

    def safe_float(val, default=0.0):
        try:
            if not val: return default
            return float(str(val).strip())
        except: return default

    return {
        "TG_API_ID": os.getenv("TG_API_ID", ""),
        "TG_API_HASH": os.getenv("TG_API_HASH", ""),
        "TG_CHANNELS": [int(x.strip()) for x in os.getenv("TG_CHANNELS", "").split(",") if x.strip() and x.strip().isdigit()],
        "MT5_LOGIN": safe_int(os.getenv("MT5_LOGIN")),
        "MT5_PASSWORD": os.getenv("MT5_PASSWORD", ""),
        "MT5_SERVER": os.getenv("MT5_SERVER", ""),
        "RISK_PERCENT": safe_float(os.getenv("RISK_PERCENT"), 1.0),
        "FIXED_LOT": safe_float(os.getenv("FIXED_LOT"), 0.0),
        "MAGIC_NUMBER": safe_int(os.getenv("MAGIC_NUMBER"), 123456),
        "SYMBOL_SUFFIX": os.getenv("SYMBOL_SUFFIX", ""),
        "EXECUTION_MODE": os.getenv("EXECUTION_MODE", "AI-ASSISTED (Manual)"),
        "DAILY_LOSS_LIMIT": safe_float(os.getenv("DAILY_LOSS_LIMIT"), 5.0),
        "TRADE_START_HOUR": safe_int(os.getenv("TRADE_START_HOUR"), 0),
        "TRADE_END_HOUR": safe_int(os.getenv("TRADE_END_HOUR"), 24),
        "USE_AI": str(os.getenv("USE_AI", "False")).lower() == "true",
        "AI_PROVIDER": os.getenv("AI_PROVIDER", "Groq"),
        "AI_API_KEY": os.getenv("AI_API_KEY", ""),
        "OR_MODEL": os.getenv("OR_MODEL", "google/gemini-flash-1.5-exp:free"),
        "REPORT_BOT_TOKEN": os.getenv("REPORT_BOT_TOKEN", ""),
        "REPORT_CHAT_ID": os.getenv("REPORT_CHAT_ID", ""),
        "SERPER_API_KEY": os.getenv("SERPER_API_KEY", ""),
        "SESSION_NAME": "itc_session"
    }

def log_trade(data):
    file_path = "trade_history.csv"
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def check_equity_guard(cfg):
    """Returns False if daily loss limit is reached"""
    service = MT5Service.instance()
    acc = service.get_account_info()
    if not acc: return True
    balance = acc.balance
    equity = acc.equity
    drawdown = ((balance - equity) / balance) * 100
    if drawdown >= cfg["DAILY_LOSS_LIMIT"]:
        print(f"// EQUITY GUARD: Maximum drawdown reached ({drawdown:.2f}%)")
        return False
    return True

def check_time_filter(cfg):
    """Returns True if within allowed hours"""
    current_hour = datetime.now().hour
    if cfg["TRADE_START_HOUR"] <= current_hour < cfg["TRADE_END_HOUR"]:
        return True
    print(f"// TIME FILTER: Outside trading hours ({current_hour}:00)")
    return False

def send_telegram_report(cfg, message):
    """Sends notification to user via secondary reporting bot"""
    if not cfg["REPORT_BOT_TOKEN"] or not cfg["REPORT_CHAT_ID"]:
        return
    url = f"https://api.telegram.org/bot{cfg['REPORT_BOT_TOKEN']}/sendMessage"
    payload = {"chat_id": cfg["REPORT_CHAT_ID"], "text": message}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"// Reporting Error: {e}")

def execute_trade(signal):
    cfg = get_env_list()
    service = MT5Service.instance() # USE SERVICE
    
    # --- Guard Checks ---
    if not check_time_filter(cfg): return
    if not check_equity_guard(cfg): return

    # --- Tier Limit Check (5x for Standard) ---
    limit = db_manager.get_trade_limit()
    current_count = db_manager.get_daily_trade_count()
    if current_count >= limit:
        tier = db_manager.get_user_tier()
        print(f"// Trade Limit Reached: {current_count}/{limit} for {tier}")
        if tier == "STANDARD":
            send_telegram_report(cfg, f"🔒 ITC LIMIT REACHED!\nAnda sudah mencapai batas harian {limit} trade (Level {tier}).\n🚀 Upgrade ke GOLD untuk trading UNLIMITED!")
        return

    # Use Service for Init
    if not service.initialize(login=cfg["MT5_LOGIN"], password=cfg["MT5_PASSWORD"], server=cfg["MT5_SERVER"]):
        print(f"// MT5 Initialize failed: {service.last_error()}")
        # --- RECONNECTION LOGIC ---
        time.sleep(1)
        if not service.initialize(login=cfg["MT5_LOGIN"], password=cfg["MT5_PASSWORD"], server=cfg["MT5_SERVER"]):
            print("// MT5 Reconnection failed.")
            return

    full_symbol = signal["symbol"] + cfg["SYMBOL_SUFFIX"]
    symbol_info = service.symbol_info(full_symbol)
    
    if symbol_info is None:
        print(f"// Symbol {full_symbol} not found.")
        return

    # --- LOT CALCULATION ---
    if cfg["FIXED_LOT"] > 0:
        lot = cfg["FIXED_LOT"]
    else:
        # Dynamic Risk Calculation
        account_info = service.get_account_info()
        balance = account_info.balance
        risk_money = balance * (cfg["RISK_PERCENT"] / 100)
        
        sl_points = abs(signal["entry"] - signal["sl"]) / symbol_info.point
        if sl_points == 0: sl_points = 100
        
        # Simple lot calculation based on sl distance
        lot = risk_money / (sl_points * 0.1) 
        lot = max(0.01, round(lot, 2))

    order_type = service.ORDER_TYPE_BUY if signal["type"] == "BUY" else service.ORDER_TYPE_SELL
    price = service.symbol_info_tick(full_symbol).ask if signal["type"] == "BUY" else service.symbol_info_tick(full_symbol).bid

    request = {
        "action": service.TRADE_ACTION_DEAL,
        "symbol": full_symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": signal["sl"],
        "tp": signal["tp"],
        "magic": cfg["MAGIC_NUMBER"],
        "comment": "ITC +AI Automated",
        "type_time": service.ORDER_TIME_GTC,
        "type_filling": service.ORDER_FILLING_IOC if (symbol_info.filling_mode & 1) else service.ORDER_FILLING_FOK if (symbol_info.filling_mode & 2) else service.ORDER_FILLING_RETURN,
    }

    result = service.order_send(request)
    if result.retcode != service.TRADE_RETCODE_DONE:
        print(f"// Trade Error: {result.comment}")
    else:
        print(f"// Trade Executed: {full_symbol} {signal['type']} at {price}")
        log_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": full_symbol,
            "type": signal["type"],
            "lot": lot,
            "entry": price,
            "sl": signal["sl"],
            "tp": signal["tp"],
            "result": "EXECUTED"
        }
        log_trade(log_data)
        db_manager.push_trade(log_data)
        send_telegram_report(cfg, f"🚀 ITC Trade Executed!\n{full_symbol} {signal['type']} @ {price}")

# --- BROADCASTER STATE ---
broadcast_cache = set()

def monitor_trades():
    """Background loop to manage open trades and Broadcast signals to Telegram (VIP)"""
    service = MT5Service.instance() # Use Service
    while True:
        try:
            if service.initialize():
                positions = service.get_positions()
                if positions is None:
                    time.sleep(1)
                    continue
                
                # 📡 SPC VIP Broadcaster: Detect new trades to send to Telegram
                is_broadcaster_on = os.getenv("SPC_MODE") == "BROADCAST"
                if is_broadcaster_on and os.getenv("SPC_BOT_TOKEN"):
                    for pos in positions:
                        ticket = pos.ticket
                        
                        with cache_lock:
                            is_cached = ticket in broadcast_cache
                            
                        if not is_cached:
                            # Format as signal
                            signal_data = {
                                "symbol": pos.symbol,
                                "type": "BUY" if pos.type == service.POSITION_TYPE_BUY else "SELL",
                                "entry": pos.price_open,
                                "sl": pos.sl,
                                "tp1": pos.tp,
                            }
                            
                            # Relay via BridgeController
                            bridge_cfg = {
                                "bot_token": os.getenv("SPC_BOT_TOKEN"),
                                "chat_id": os.getenv("SPC_CHAT_ID"),
                                "template": os.getenv("SPC_TEMPLATE"),
                                "use_watermark": os.getenv("SPC_USE_WATERMARK") == "1"
                            }
                            
                            success, res = BridgeController.relay_signal(signal_data, bridge_cfg)
                            if success:
                                with cache_lock:
                                    broadcast_cache.add(ticket)
                                print(f"// MT5 Broadcaster Success: Ticket {ticket} sent to Telegram.")

                for pos in positions:
                    # Logic for BE or Partial could go here
                    pass
                
                # --- CACHE CLEANUP (Prevents Memory Leak) ---
                with cache_lock:
                    if len(broadcast_cache) > 1000:
                        # Keep only last 100 entries to prevent infinite growth
                        trimmed = set(list(broadcast_cache)[-100:])
                        broadcast_cache.clear()
                        broadcast_cache.update(trimmed)

        except Exception as e:
            print(f"// Monitor Loop Error: {e}")
        
        time.sleep(2) # Faster responsive loop

def close_all_orders():
    """Closes all open positions on the account"""
    service = MT5Service.instance()
    if not service.initialize(): return False
    positions = service.get_positions()
    if not positions: return True
    for pos in positions:
        # Close logic
        symbol = pos.symbol
        lot = pos.volume
        type = service.ORDER_TYPE_SELL if pos.type == service.ORDER_TYPE_BUY else service.ORDER_TYPE_BUY
        price = service.symbol_info_tick(symbol).bid if pos.type == service.ORDER_TYPE_BUY else service.symbol_info_tick(symbol).ask
        
        request = {
            "action": service.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": type,
            "position": pos.ticket,
            "price": price,
            "comment": "Emergency Close",
            "type_time": service.ORDER_TIME_GTC,
            "type_filling": service.ORDER_FILLING_IOC,
        }
        service.order_send(request)
    return True

def get_positions():
    """Returns list of open positions as dictionaries"""
    service = MT5Service.instance()
    if not service.initialize(): return []
    positions = service.get_positions()
    if not positions: return []
    result = []
    for pos in positions:
        result.append({
            "symbol": pos.symbol,
            "type": "BUY" if pos.type == service.POSITION_TYPE_BUY else "SELL",
            "volume": pos.volume,
            "profit": pos.profit,
            "ticket": pos.ticket,
            "comment": getattr(pos, 'comment', ''),
            "magic": getattr(pos, 'magic', 0)
        })
    return result

def get_history_orders(limit=5):
    """Returns last N closed deals"""
    service = MT5Service.instance()
    if not service.initialize(): return []
    from_date = datetime(2020, 1, 1)
    to_date = datetime.now()
    history = service.history_deals_get(from_date, to_date)
    if not history: return []
    
    # Sort by time descending
    sorted_hist = sorted(history, key=lambda x: x.time, reverse=True)
    recent = sorted_hist[:limit]
    
    result = []
    for deal in recent:
        if deal.entry == service.DEAL_ENTRY_OUT: # Only closing deals
            result.append({
                "symbol": deal.symbol,
                "type": "BUY" if deal.type == service.DEAL_TYPE_BUY else "SELL",
                "profit": deal.profit,
                "volume": deal.volume
            })
    return result

# --- GLOBAL STATE ---
signal_cache = set()
signal_callback = None # Callback for GUI to intercept signals
app = None  # Pyrogram Client instance (initialized via create_telegram_client)

def set_signal_callback(callback):
    global signal_callback
    signal_callback = callback

def create_telegram_client(caller="APP", api_id=None, api_hash=None, channels=None):
    """
    Creates and configures the Pyrogram Client for Telegram signal reception.
    Reads TG_API_ID, TG_API_HASH, TG_CHANNELS from .env.
    Returns the configured Client or None if credentials are missing.
    """
    global app
    load_dotenv(override=True)
    
    # Debug trace
    print(f"// Telegram: create_telegram_client invoked by [{caller}]")
    
    # Prioritize provided args over ENV
    api_id = api_id if api_id is not None else os.getenv("TG_API_ID", "").strip()
    api_hash = api_hash if api_hash is not None else os.getenv("TG_API_HASH", "").strip()
    channels_raw = channels if channels is not None else os.getenv("TG_CHANNELS", "").strip()
    
    if not api_id or not api_hash:
        print("// Telegram: Missing TG_API_ID or TG_API_HASH in .env. Client not created.")
        return None
    
    try:
        api_id_int = int(api_id)
    except ValueError:
        print(f"// Telegram: Invalid TG_API_ID '{api_id}'. Must be integer.")
        return None
    
    # Parse channel list (comma-separated, supports usernames and IDs)
    channel_list = []
    if channels_raw:
        for ch in channels_raw.split(","):
            ch = ch.strip()
            if not ch:
                continue
            try:
                channel_list.append(int(ch))  # Numeric chat ID
            except ValueError:
                channel_list.append(ch)  # Username string
    
    if not channel_list:
        print("// Telegram: No channels configured in TG_CHANNELS. Client created but no filter active.")
    
    # Create Pyrogram Client
    app = Client(
        "itc_copier_session",
        api_id=api_id_int,
        api_hash=api_hash,
        workdir=os.path.dirname(os.path.abspath(__file__))
    )
    
    # Register message handler
    if channel_list:
        @app.on_message(filters.chat(channel_list))
        async def handle_new_message(client, message):
            """Processes incoming Telegram messages from monitored channels."""
            text = message.text or message.caption or ""
            if not text.strip():
                return
            
            # Deduplicate using message hash
            msg_hash = hashlib.md5(f"{message.chat.id}:{message.id}".encode()).hexdigest()
            with cache_lock:
                if msg_hash in signal_cache:
                    return
                signal_cache.add(msg_hash)
                # Cleanup cache if too large
                if len(signal_cache) > 500:
                    signal_cache.clear()
            
            print(f"// Telegram: Message received from {message.chat.title or message.chat.id}")
            
            # 1. Try Regex Parser first (fast)
            signal = parse_signal(text)
            
            # 2. Fallback to AI Parser if regex fails
            if not signal:
                try:
                    ai_key = os.getenv("AI_API_KEY") or os.getenv("MASTER_GROQ_KEY", "")
                    ai_provider = os.getenv("AI_PROVIDER", "Groq")
                    if ai_key:
                        signal = ai_parse_signal(text, ai_key, ai_provider)
                except Exception as e:
                    print(f"// AI Parse Fallback Error: {e}")
            
            if not signal:
                print(f"// Telegram: Message not recognized as trading signal.")
                return
            
            print(f"// Signal Detected: {signal['type']} {signal['symbol']} @ {signal.get('entry', 'Market')}")
            
            # 3. Route to callback (GUI) or direct execution
            if signal_callback:
                signal_callback(signal)
            else:
                # Direct execution if no GUI callback registered
                try:
                    execute_trade(signal)
                except Exception as e:
                    print(f"// Direct Execution Error: {e}")
    else:
        # No channels configured — register catch-all for debugging
        @app.on_message(filters.all)
        async def handle_all_messages(client, message):
            text = message.text or ""
            if text:
                print(f"// Telegram (Unfiltered): {message.chat.title or message.chat.id}: {text[:80]}...")
    
    print(f"// Telegram Client Created (Caller: {caller}). Monitoring {len(channel_list)} channel(s).")
    return app

# --- HANDLERS & PARSERS ---

def parse_signal(text):
    """Robust Regex Parser for Trading Signals"""
    text = text.upper()
    try:
        # Improved Symbol Detection (Support symbols like XAUUSD, EURUSD.pro, GOLD)
        sym_match = re.search(r'([A-Z0-9.]{3,})', text)
        if not sym_match: return None
        symbol = sym_match.group(1)
        
        # Improved Type Detection
        is_buy = any(kw in text for kw in ["BUY", "LONG", "BULLISH"])
        is_sell = any(kw in text for kw in ["SELL", "SHORT", "BEARISH"])
        
        if is_buy and is_sell: signal_type = "BUY" if text.find("BUY") < text.find("SELL") else "SELL"
        elif is_buy: signal_type = "BUY"
        elif is_sell: signal_type = "SELL"
        else: return None
        
        # Entry
        entry_patterns = [
            r'(?:ENTRY|CMP|PRICE)[:\s\n]*([\d.]+)', 
            r'(?:AT|@)[:\s\n]*([\d.]+)',
            r'(?:BUY|SELL)\s+[A-Z0-9.]+\s+(?:@|AT)?\s*([\d.]+)'
        ]
        entry = None
        for p in entry_patterns:
            m = re.search(p, text)
            if m: 
                entry = float(m.group(1 if m.lastindex == 1 else 1)) # Handle multiple groups
                if m.lastindex >= 2 and m.group(2): entry = float(m.group(2))
                break
        
        # SL
        sl_match = re.search(r'(?:SL|STOPLOSS|STOP)[:\s\n]*([\d.]+)', text)
        sl = float(sl_match.group(1)) if sl_match else 0.0
        
        # TP (Search for TP, TP1, or Take Profit)
        tp_match = re.search(r'(?:TP1|TP|TAKEPROFIT)[:\s\n]*([\d.]+)', text)
        tp = float(tp_match.group(1)) if tp_match else 0.0
        
        if not entry or not tp or not sl:
            return None
            
        return {"symbol": symbol, "type": signal_type, "entry": entry, "tp": tp, "sl": sl}
    except Exception as e:
        print(f"// Regex Parse Error: {e}")
        return None

def call_openrouter(prompt, api_key, model_id, system_context=""):
    """Helper to call OpenRouter API"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    messages = []
    if system_context:
        messages.append({"role": "system", "content": system_context})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_id,
        "messages": messages
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

def call_cloudflare(prompt, api_key, model_id, system_context=""):
    """Helper to call Cloudflare Workers AI API"""
    cf_id = os.getenv("CLOUDFLARE_ID")
    if not cf_id or not api_key: return "Cloudflare Config Missing"
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{cf_id}/ai/run/{model_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "messages": [
            {"role": "system", "content": system_context or "You are a trading assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        return res.json().get("result", {}).get("response", "No response from CF")
    except Exception as e:
        return f"Cloudflare Error: {e}"

def call_ollama(prompt, model_id, system_context=""):
    """Helper for Local Ollama Inference"""
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    payload = {
        "model": model_id,
        "prompt": f"{system_context}\n\nUser: {prompt}" if system_context else prompt,
        "stream": False
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        return res.json().get("response", "")
    except Exception as e:
        return f"Ollama Error: {e}"

# --- MASTER SETTINGS ---
# --- MASTER WATERFALL LOGIC ---
from configs.ai_config import MASTER_GROQ_KEY, AI_WATERFALL_MATRIX

def execute_ai_waterfall(feature_key, prompt, system_context="", user_api_key="", user_provider="", image_path=None):
    """
    CORE AI ROUTER & WATERFALL
    1. Check User Bypass (If user_api_key provided, use ONLY that)
    2. Waterfall (T1 -> T2 -> T3)
    Supports Multimodal (Vision) if image_path is provided.
    """
    
    # helper for vision encoding
    def _encode_image(path):
        import base64
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode('utf-8')

    # --- PATH A: USER OVERRIDE ---
    if user_api_key and user_api_key.strip():
        try:
            if user_provider == "Gemini":
                return call_openrouter(prompt, user_api_key, "google/gemini-pro-1.5", system_context, image_path)
            elif user_provider == "Groq":
                return call_groq(prompt, user_api_key, "llama-3.3-70b-versatile", system_context, image_path)
            elif user_provider == "Cloudflare":
                return call_cloudflare(prompt, user_api_key, "@cf/meta/llama-3-8b-instruct", system_context)
            else:
                return call_openrouter(prompt, user_api_key, "auto", system_context, image_path)
        except Exception as e:
            return f"User API Error: {e}"

    # --- PATH B: SYSTEM WATERFALL ---
    matrix = AI_WATERFALL_MATRIX.get(feature_key)
    if not matrix: return "Invalid Feature Key"
    
    for tier in ["T1", "T2", "T3"]:
        cfg = matrix[tier]
        provider = cfg["provider"]
        model = cfg["model"]
        
        key = os.getenv(f"{provider}_API_KEY") or os.getenv("AI_API_KEY")
        if provider == "Groq" and tier == "T1": key = MASTER_GROQ_KEY

        if not key and provider != "Ollama": continue
        
        try:
            if provider == "Groq":
                res = call_groq(prompt, key, model, system_context, image_path)
            elif provider == "OpenRouter":
                res = call_openrouter(prompt, key, model, system_context, image_path)
            elif provider == "Cloudflare":
                res = call_cloudflare(prompt, key, model, system_context)
            elif provider == "Ollama":
                res = call_ollama(prompt, model, system_context)
            else: continue
            
            if any(err in str(res).lower() for err in ["error:", "rate_limit", "exhausted", "429"]):
                continue
            
            return res
        except:
            continue
            
    return "All AI Tiers Exhausted."

def call_groq(prompt, api_key, model_id, system_context="", image_path=None):
    """Helper to call Groq API (Supports Vision)"""
    messages = []
    if system_context:
        messages.append({"role": "system", "content": system_context})
    
    if image_path:
        import base64
        with open(image_path, "rb") as f: b64 = base64.b64encode(f.read()).decode('utf-8')
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
            ]
        })
        model_id = model_id or "llama-3.2-11b-vision-preview"
    else:
        messages.append({"role": "user", "content": prompt})
        model_id = model_id or "llama-3.1-70b-versatile"

    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_id,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Groq Error: {str(e)}"

def call_openrouter(prompt, api_key, model_id, system_context="", image_path=None):
    """Helper to call OpenRouter API (Supports Vision)"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    messages = []
    if system_context:
        messages.append({"role": "system", "content": system_context})
    
    if image_path:
        import base64
        with open(image_path, "rb") as f: b64 = base64.b64encode(f.read()).decode('utf-8')
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
            ]
        })
    else:
        messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_id or "google/gemini-flash-1.5",
        "messages": messages
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=15)
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

def ai_parse_signal(text, user_api_key="", user_provider=""):
    """Uses High-Accuracy AI to parse complex signals via Waterfall"""
    prompt = f"Extract trading signal (Symbol, Type, Entry, TP, SL) from this text and return strictly as JSON:\n\n{text}"
    content = execute_ai_waterfall("SIGNAL_PARSING", prompt, user_api_key=user_api_key, user_provider=user_provider)
        
    try:
        # Extract JSON
        json_str = re.search(r'\{.*\}', content, re.DOTALL).group(0)
        return json.loads(json_str)
    except:
        return None

def chat_with_ai(user_prompt, user_api_key="", user_provider="", system_context=""):
    """Uses Efficient AI for General conversation via Waterfall"""
    return execute_ai_waterfall("COMPANION_CHAT", user_prompt, system_context, user_api_key, user_provider)

# --- EDUCATION MODULE ---
def generate_quiz_questions(level, api_key, provider="Gemini"):
    """Generates 10 trading-related multiple choice questions using AI with STRICT difficulty scaling."""
    
    # Advanced Difficulty Persona & Context
    difficulty_guide = {
        "Pemula": """
            ROLE: Basic Instructor.
            TOPICS: Definitions of Pips, Lots, Spread, basic Candle names (Hammer, Doji), and basic MT5 usage.
            LEVEL: Grade 1 (Conceptual basics).
        """,
        "Menengah": """
            ROLE: Technical Analyst.
            TOPICS: Standard indicators (RSI Overbought/Oversold, Moving Average Crossovers), Chart Patterns (Double Top, Head & Shoulders), and basic Money Management (1% rule).
            LEVEL: Grade 5 (Applied technicals).
        """,
        "Ahli": """
            ROLE: Professional Prop Firm Trader.
            TOPICS: Market Structure (BOS, CHoCH), Supply & Demand zones, ICT/SMC basics, Liquidity hunts, and Multi-timeframe analysis.
            LEVEL: Grade 8 (Institutional logic).
        """,
        "Legenda": """
            ROLE: Institutional Quant & Master of Market Sentiment.
            TOPICS: Advanced Order flow, Fair Value Gaps (FVG) refined, Inducement traps, Hedging strategies, Correlation (DXY vs EURUSD), Macro-fundamentals (NFP/FOMC impact), and deep Trading Psychology.
            STRICT RULE: DO NOT ask about basic terms like 'What is a Lot?'. Ask about specific market behaviors and reaction logic.
            LEVEL: Grade 10 (Mastery).
        """
    }
    level_instruction = difficulty_guide.get(level, "Intermediate level trading.")

    prompt = f"""
    You are a Senior Trading Educator. Generate EXACTLY 10 highly accurate multiple choice questions for the '{level}' level.
    
    STRICT LEVEL PARAMETERS:
    {level_instruction}
    
    RESPONSE FORMAT:
    Return ONLY a raw JSON array of objects. No intro text, no markdown code blocks.
    [
        {{"q": "Technical Question?", "a": "Correct Answer", "o": ["Plausible Wrong 1", "Plausible Wrong 2", "Plausible Wrong 3"]}}
    ]
    
    LANGUAGE: Indonesian (Bahasa Indonesia).
    TONE: Professional, Technical, and Academic.
    """
    
    try:
        response = execute_ai_waterfall("QUIZ_GEN", prompt, user_api_key=api_key, user_provider=provider)
            
        # Robust Error Detection: If response starts with "Gemini Error" or "Groq Error", don't parse
        if "Error:" in response or "Exhausted!" in response:
            print(f"// QUIZ GEN FAILED: AI Provider returned error: {response}")
            return None

        # Clean response: Remove markdown blocks if present
        json_match = re.search(r'\[\s*\{.*\}\s*\]', response, re.DOTALL)
        if json_match:
            cleaned = json_match.group(0)
        else:
            cleaned = re.sub(r'```json|```', '', response).strip()
            
        data = json.loads(cleaned)
        return data[:10] # Return exactly 10
    except Exception as e:
        print(f"// QUIZ GEN PARSE ERROR: {e} | Raw Response: {response[:100]}...")
        return None

# --- BACKGROUND AUTO-LOGIN BRIDGE ---
def login_mt5_custom(login_id, password, server):
    """Bridge for background auto-login. Returns (Success, Message)"""
    # REFACTORED: Use Service
    service = MT5Service.instance()
    if not service.initialize():
        return False, "Failed to initialize MT5"
    authorized = service.login(login_id, password=password, server=server)
    if authorized:
        return True, "Login Successful"
    return False, f"Login failed: {service.last_error()}"

if __name__ == "__main__":
    client = create_telegram_client()
    if client:
        print("// ITC +AI Signal Copier Running...")
        # Start monitor thread
        threading.Thread(target=monitor_trades, daemon=True).start()
        client.run()
    else:
        print("// Error: Telegram Client not configured. Check TG_API_ID and TG_API_HASH in .env.")
