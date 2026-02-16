# ══════════════════════════════════════════════════════════════════════════════
# 🕹️ GAMIFICATION SERVICE (Logic Layer)
# 🎯 ROLE: Manages ITC Coins, Temporal Upgrades, and Rewards.
# ══════════════════════════════════════════════════════════════════════════════

import logging
from datetime import datetime, timedelta

class GamificationService:
    """
    Handles internal economy:
    - ITC Coin management
    - Temporary 1-hour Premium Boosts
    - Achievement checking
    """

    COST_UPGRADE_VIP = 5000  # High cost as requested
    COST_UPGRADE_PRO = 2000

    def __init__(self, db_manager):
        self.db = db_manager
        self.logger = logging.getLogger("GravityGamification")

    def get_user_balance(self):
        """Fetches itc_coins and premium_until from profile"""
        try:
            user_id = self.db.user_id
            if user_id == "anonymous": return {"coins": 0, "until": None}
            
            res = self.db.client.table("user_profiles")\
                .select("itc_coins, premium_until")\
                .eq("hwid", user_id)\
                .maybe_single()\
                .execute()
                
            if res.data:
                return {
                    "coins": res.data.get("itc_coins", 0),
                    "until": res.data.get("premium_until")
                }
            return {"coins": 0, "until": None}
        except Exception as e:
            self.logger.error(f"Balance Fetch Error: {e}")
            return {"coins": 0, "until": None}

    def buy_boost(self, tier):
        """
        Grants 1 hour of premium access.
        tier: 'PRO' or 'VIP'
        """
        try:
            user_id = self.db.user_id
            if user_id == "anonymous": return False, "Login required"

            cost = self.COST_UPGRADE_VIP if tier == 'VIP' else self.COST_UPGRADE_PRO
            
            # 1. Check Balance
            balance_data = self.get_user_balance()
            if balance_data["coins"] < cost:
                return False, f"Insufficient ITC Coins (Need {cost})"

            # 2. Calculate Expiry
            new_expiry = datetime.now() + timedelta(hours=1)
            
            # 3. Deduct & Grant
            self.db.client.table("user_profiles").update({
                "itc_coins": balance_data["coins"] - cost,
                "premium_until": new_expiry.isoformat(),
                "subscription_tier": tier if tier == 'VIP' else 'PRO' # Temporary tier change
            }).eq("hwid", user_id).execute()

            return True, f"Successfully boosted to {tier} for 1 hour!"

        except Exception as e:
            self.logger.error(f"Boost Purchase Error: {e}")
            return False, str(e)

    @staticmethod
    def is_premium_active(profile_data):
        """Helper to determine if temporal premium is still valid"""
        until_str = profile_data.get("premium_until")
        if not until_str: return False
        
        try:
            expiry = datetime.fromisoformat(until_str.replace('Z', '+00:00'))
            return datetime.now().astimezone() < expiry
        except:
            return False
