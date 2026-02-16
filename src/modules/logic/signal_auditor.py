import os
import json
import time
import threading
from modules.mt5.mt5_service import MT5Service
from datetime import datetime, timedelta
from modules.db.supabase_client import SupabaseManager

DATA_FILE = "data/signals_sent.json"
LOCK = threading.Lock()

class SignalAuditor:
    """
    The 'Middleman' that records signals and verifies their outcome.
    Generates the 'Win Rate' and 'Performance' stats for the Institutional Broadcast.
    """
    _db = SupabaseManager()

    @staticmethod
    def _load_ledger():
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def _save_ledger(data):
        with LOCK:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)

    @staticmethod
    def log_signal(signal_data):
        """
        Records a new signal to the ledger.
        """
        ledger = SignalAuditor._load_ledger()
        
        new_entry = {
            "id": int(time.time() * 1000), # Unique ID
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": signal_data.get("symbol"),
            "type": signal_data.get("type"),
            "entry": float(signal_data.get("entry", 0)),
            "sl": float(signal_data.get("sl", 0)),
            "tp1": float(signal_data.get("tp1", 0)),
            "tp2": float(signal_data.get("tp2", 0)),
            "tp3": float(signal_data.get("tp3", 0)),
            "status": "PENDING", # PENDING, WIN, LOSS, EXPIRED
            "outcome_pips": 0,
            "outcome_time": None
        }
        
        ledger.append(new_entry)
        SignalAuditor._save_ledger(ledger)
        print(f"// Auditor: Signal logged {new_entry['symbol']} {new_entry['type']}")
        
        # --- CLOUD SYNC ---
        if SignalAuditor._db:
             threading.Thread(target=lambda: SignalAuditor._db.push_audit_entry(new_entry), daemon=True).start()

    @staticmethod
    def get_performance_stats():
        """
        Calculates Win Rate, Total Signals, Streak, etc.
        """
        ledger = SignalAuditor._load_ledger()
        
        # Filter completed trades
        completed = [s for s in ledger if s["status"] in ["WIN", "LOSS"]]
        total = len(completed)
        wins = len([s for s in completed if s["status"] == "WIN"])
        
        win_rate = round((wins / total * 100), 1) if total > 0 else 0
        
        # Calculate Streak (Last N wins)
        streak = 0
        for s in reversed(completed):
            if s["status"] == "WIN": streak += 1
            else: break
            
        return {
            "total_signals": len(ledger),
            "completed_signals": total,
            "wins": wins,
            "losses": total - wins,
            "win_rate": f"{win_rate}%",
            "win_streak": streak,
            "rating": "⭐⭐⭐⭐" if win_rate > 70 else "⭐⭐⭐" if win_rate > 50 else "⭐⭐"
        }

    @staticmethod
    def audit_loop():
        """
        Background Worker: Checks active signals against current price.
        Should be run in a separate thread.
        """
        service = MT5Service.instance()
        if not service.initialize(): 
            return

        ledger = SignalAuditor._load_ledger()
        dirty = False
        
        for signal in ledger:
            if signal["status"] != "PENDING":
                continue
                
            symbol = signal["symbol"]
            info = service.symbol_info_tick(symbol)
            if not info: continue
            
            # Simple Logic: 
            # BUY: If Bid >= TP -> WIN. If Bid <= SL -> LOSS.
            # SELL: If Ask <= TP -> WIN. If Ask >= SL -> LOSS.
            
            # (Using Bid for TP sell, Ask for SL sell usually, but simplified here for estimates)
            curr_bid = info.bid
            curr_ask = info.ask
            
            if signal["type"] == "BUY":
                if curr_bid >= signal["tp1"]:
                    signal["status"] = "WIN"
                    signal["outcome_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    dirty = True
                elif curr_bid <= signal["sl"]:
                    signal["status"] = "LOSS"
                    signal["outcome_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    dirty = True
            
            elif signal["type"] == "SELL":
                 if curr_ask <= signal["tp1"]:
                    signal["status"] = "WIN"
                    signal["outcome_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    dirty = True
                 elif curr_ask >= signal["sl"]:
                    signal["status"] = "LOSS"
                    signal["outcome_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    dirty = True
                    
            # Expiry check (24 hours)
            sig_time = datetime.strptime(signal["timestamp"], "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - sig_time).total_seconds() > 86400:
                signal["status"] = "EXPIRED"
                dirty = True

        if dirty:
            SignalAuditor._save_ledger(ledger)
            
            # Update each dirty signal to cloud (Simple Batch-ish for loop)
            if SignalAuditor._db:
                for sig in ledger:
                    if sig["status"] != "PENDING":
                        threading.Thread(target=lambda s=sig: SignalAuditor._db.push_audit_entry(s), daemon=True).start()

# NOTE: audit_loop should be started explicitly from app, not auto-started on import.
# To start manually: threading.Thread(target=SignalAuditor.audit_loop, daemon=True).start()
