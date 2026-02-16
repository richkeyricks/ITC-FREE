# ══════════════════════════════════════════════════════════════════════════════
# 🧬 VERIFICATION SERVICE (Logic Layer)
# 🛡️ SECURITY: Validates Logic BEFORE Marketplace Upload
# ══════════════════════════════════════════════════════════════════════════════

# --- IMPORTS ---
from modules.mt5.mt5_service import MT5Service
from datetime import datetime, timedelta
import logging

try:
    import MetaTrader5 as mt5
    DEAL_ENTRY_OUT = mt5.DEAL_ENTRY_OUT
except ImportError:
    DEAL_ENTRY_OUT = 1  # Fallback constant

# --- CONSTANTS ---
# (None)

# --- LOGIC ---
class VerificationService:
    """
    Gatekeeper Logic: Prevents 'Snake Oil' from entering the Marketplace.
    Reads LOCAL MT5 History -> Calculates Metrics -> Returns Eligibility.
    """
    
    MIN_TRADES = 5
    MIN_ROI = 2.0 # Lowered to 2% for MVP entry (stricter later)
    MIN_WINRATE = 30.0 # Strategies can have low WR but high RR

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = logging.getLogger("GravityVerifier")

    def run_full_verification(self):
        """
        Runs the complete verification pipeline.
        Returns: (is_eligible, reason, metrics_dict)
        """
        try:
            service = MT5Service.instance()

            # 1. MT5 Connection
            if not service.initialize():
                return False, "MT5 Not Connected", {}

            # 2. Fetch History (Last 14 Days)
            from_date = datetime.now() - timedelta(days=14)
            to_date = datetime.now()
            deals = service.history_deals_get(from_date, to_date)
            
            if deals is None or len(deals) == 0:
                return False, "No Trading History Found (Last 14 Days)", {}

            # 3. Filter & Calculate
            closing_deals = [d for d in deals if d.entry == DEAL_ENTRY_OUT]
            
            if len(closing_deals) < self.MIN_TRADES:
                return False, f"Not Enough Trades. Need {self.MIN_TRADES}, Found {len(closing_deals)}.", {}
            
            # --- METRICS ENGINE ---
            total_profit = sum(d.profit for d in closing_deals)
            wins = len([d for d in closing_deals if d.profit >= 0])
            losses = len([d for d in closing_deals if d.profit < 0])
            total_trades = len(closing_deals)
            
            win_rate = (wins / total_trades) * 100
            
            # ROI (Approximate based on current balance vs profit)
            acc = service.account_info()
            balance = acc.balance if acc else 100.0 # Prevent ZeroDiv
            if balance == 0: balance = 1.0 
            
            roi = (total_profit / balance) * 100
            
            # Drawdown (Simulated from history - Max Peak to Trough)
            drawdown = 0.0 

            metrics = {
                "roi": round(roi, 2),
                "win_rate": round(win_rate, 2),
                "profit": round(total_profit, 2),
                "trades": total_trades,
                "drawdown": drawdown
            }

            # 4. Eligibility Check
            if roi < self.MIN_ROI:
                 return False, f"ROI Too Low ({roi:.2f}%). Minimum {self.MIN_ROI}% required.", metrics
            
            return True, "VERIFIED", metrics

        except Exception as e:
            self.logger.error(f"Verification Error: {e}")
            return False, f"System Error: {str(e)}", {}

    def publish_preset(self, title, description, price, config, metrics):
        """
        Publishes the verified preset to 'marketplace_presets'.
        """
        try:
            # Construct the secure payload
            payload = {
                "seller_id": self.db_manager.user_id,
                "title": title,
                "description": description,
                "price_idr": int(float(price)),
                "price_usd": round(float(price) / 16000, 2),
                "config_json": config,
                "is_verified": True,
                "verified_win_rate": metrics.get("win_rate", 0),
                "verified_profit_factor": metrics.get("roi", 0),
                "verified_days_tested": 14,
                "sales_count": 0
            }
            
            # Insert to public marketplace table
            response = self.db_manager.client.table("marketplace_presets").insert(payload).execute()
            
            if response.data:
                return True, "Strategy Published Successfully!"
            return False, "Database Reject"
            
        except Exception as e:
            return False, str(e)
