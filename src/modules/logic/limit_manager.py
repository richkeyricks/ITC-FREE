
# --- IMPORTS ---
from modules.mt5.mt5_service import MT5Service
from datetime import datetime, timedelta
import logging

# --- CONSTANTS ---
# (None)

# --- LOGIC ---
class LimitManager:
    """
    The Gatekeeper for Free Tier Limitations.
    Enforces the "Double Trap" Strategy:
    1. Max 3 Trades per Day
    2. Max $10 Profit per Day
    
    Account Logic:
    - REAL: STRICT LIMITS
    - DEMO: UNLIMITED (The "Hook")
    """
    
    MAX_TRADES = 3
    MAX_PROFIT = 10.0
    
    @staticmethod
    def _get_start_of_day():
        """Returns 00:00 of the current day."""
        now = datetime.now()
        return datetime(now.year, now.month, now.day, 0, 0, 0)

    @staticmethod
    def get_daily_stats():
        """
        Fetches current daily usage stats.
        Returns: {
            "account_type": "REAL" | "DEMO",
            "trades_count": int,
            "profit_accumulated": float,
            "is_locked": bool,
            "lock_reason": str | None
        }
        """
        service = MT5Service.instance()
        if not service.initialize():
            return {
                "account_type": "UNKNOWN",
                "trades_count": 0, "profit_accumulated": 0.0,
                "is_locked": True, "lock_reason": "MT5 Disconnected"
            }
            
        account_info = service.account_info()
        if not account_info:
             return {
                "account_type": "UNKNOWN",
                "trades_count": 0, "profit_accumulated": 0.0,
                "is_locked": True, "lock_reason": "Account Info Unavailable"
            }
            
        # 1. Check Account Type
        # mt5.ACCOUNT_TRADE_MODE_DEMO = 0, CONTEST = 1, REAL = 2
        is_demo = account_info.trade_mode == service.ACCOUNT_TRADE_MODE_DEMO
        acc_type = "DEMO" if is_demo else "REAL"
        
        # 2. Fetch History (Today)
        from_date = LimitManager._get_start_of_day()
        to_date = datetime.now() + timedelta(days=1) # Ensure we cover everything
        
        deals = service.history_deals_get(from_date, to_date)
        
        trades_count = 0
        profit_accumulated = 0.0
        
        if deals:
            for deal in deals:
                # ENTRY_OUT means a closed trade (Realized P/L)
                if deal.entry == service.DEAL_ENTRY_OUT:
                    trades_count += 1
                    # Only POSITIVE profit counts towards the limit Cap
                    if deal.profit > 0:
                        profit_accumulated += deal.profit
                        
        # 3. Determine Lock Status
        is_locked = False
        lock_reason = None
        
        if acc_type == "REAL":
            if trades_count >= LimitManager.MAX_TRADES:
                is_locked = True
                lock_reason = f"Daily Limit: Max {LimitManager.MAX_TRADES} Trades Reached."
            elif profit_accumulated >= LimitManager.MAX_PROFIT:
                is_locked = True
                lock_reason = f"Daily Limit: Max ${LimitManager.MAX_PROFIT} Profit Reached."
                
        return {
            "account_type": acc_type,
            "trades_count": trades_count,
            "profit_accumulated": profit_accumulated,
            "is_locked": is_locked,
            "lock_reason": lock_reason
        }

    @staticmethod
    def check_limit_strict():
        """
        Simple boolean check for logic controllers.
        Returns: (is_allowed: bool, message: str)
        """
        stats = LimitManager.get_daily_stats()
        
        if stats["is_locked"]:
            return False, stats["lock_reason"]
            
        return True, "OK"
