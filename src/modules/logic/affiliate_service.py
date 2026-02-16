# ══════════════════════════════════════════════════════════════════════════════
# 🦠 AFFILIATE SERVICE (Logic Layer)
# 🎯 ROLE: Viral Engine. Generates Codes, Links Users, Calculates Commissions.
# ══════════════════════════════════════════════════════════════════════════════

import random
import string
import logging

class AffiliateService:
    """
    Manages the Viral Affiliate System.
    - Generates unique codes
    - Binds users recursively (upline)
    - Processes 10% payouts
    """
    
    COMMISSION_RATE = 0.10 # 10% Flat

    def __init__(self, db_manager):
        self.db = db_manager
        self.logger = logging.getLogger("GravityAffiliate")

    def generate_my_code(self):
        """Generates a unique 6-char code for the current user if not exists"""
        try:
            user_id = self.db.user_id
            if user_id == "anonymous": return None
            
            # 1. Check existing
            res = self.db.client.table("affiliate_codes").select("code").eq("user_id", user_id).execute()
            if res.data:
                return res.data[0]["code"]
                
            # 2. Generate New Unique
            new_code = self._create_unique_code()
            self.db.client.table("affiliate_codes").insert({"code": new_code, "user_id": user_id}).execute()
            return new_code
            
        except Exception as e:
            self.logger.error(f"Affiliate Code Error: {e}")
            return None

    def _create_unique_code(self):
        """Reliable unique code generator"""
        for _ in range(10): # Retry limit
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # Check collisions (Optimistic)
            try:
                res = self.db.client.table("affiliate_codes").select("code").eq("code", code).execute()
                if not res.data:
                    return code
            except: pass
        return "ERROR_CODE"

    def bind_referral(self, code):
        """
        Links current user to a Referrer (Upline).
        Must be called ONCE during SignUp or First Login.
        """
        try:
            referee_id = self.db.user_id
            if not code or referee_id == "anonymous": return False, "Invalid Context"
            
            # 1. Find Referrer ID from Code
            res = self.db.client.table("affiliate_codes").select("user_id").eq("code", code).maybe_single().execute()
            if not res.data: return False, "Invalid Referral Code"
            
            referrer_id = res.data["user_id"]
            
            # 2. Prevent Self-Referral
            if referrer_id == referee_id:
                return False, "Cannot refer yourself"

            # 3. Create Link
            # Unique Constraint on referee_id ensures one upline only
            self.db.client.table("affiliate_referrals").insert({
                "referrer_id": referrer_id,
                "referee_id": referee_id
            }).execute()
            
            return True, "Referral Linked Successfully"
            
        except Exception as e:
            if "duplicate key" in str(e):
                return False, "Already has a referrer"
            return False, str(e)

    def payout_commission(self, order_id, purchase_amount, buyer_id):
        """
        Triggered after a successful Marketplace Purchase.
        Finds the Buyer's Upline and credits 10%.
        """
        try:
            # 1. Find Upline
            res = self.db.client.table("affiliate_referrals").select("referrer_id").eq("referee_id", buyer_id).maybe_single().execute()
            if not res.data:
                print(f"// No Upline for Buyer {buyer_id}. Skipping Commission.")
                return 
                
            referrer_id = res.data["referrer_id"]
            commission = float(purchase_amount) * self.COMMISSION_RATE
            
            # 2. Record Commission Ledger
            self.db.client.table("affiliate_commissions").insert({
                "referrer_id": referrer_id,
                "source_order_id": order_id,
                "amount_commission": commission,
                "base_amount": float(purchase_amount),
                "status": "PENDING"
            }).execute()
            
            # 3. Credit Pending Balance (Atomic RPC preferred, but simplified here)
            # Fetch current
            w_res = self.db.client.table("user_wallets").select("balance_pending, total_earned").eq("user_id", referrer_id).maybe_single().execute()
            if w_res.data:
                curr_pending = float(w_res.data.get("balance_pending", 0))
                curr_total = float(w_res.data.get("total_earned", 0))
                
                self.db.client.table("user_wallets").update({
                    "balance_pending": curr_pending + commission,
                    "total_earned": curr_total + commission
                }).eq("user_id", referrer_id).execute()
                
            print(f"// Affiliate: Credited Rp {commission} to {referrer_id}")
            
        except Exception as e:
            print(f"// Commission Error: {e}")

    def get_my_stats(self):
        """Returns {code, referral_count, total_earned}"""
        try:
            user_id = self.db.user_id
            
            # Code
            c_res = self.db.client.table("affiliate_codes").select("code").eq("user_id", user_id).execute()
            code = c_res.data[0]["code"] if c_res.data else "Generate Now"
            
            # Count
            r_res = self.db.client.table("affiliate_referrals").select("*", count="exact", head=True).eq("referrer_id", user_id).execute()
            count = r_res.count or 0
            
            # Earnings (Sum Commission)
            # Optimized: Just sum from wallet 'total_earned' might include generic sales
            # More Accurate: Sum 'affiliate_commissions'
            # For MVP, we use Wallet Total as proxy if they are pure affiliate, 
            # OR we can query commissions table. Let's query commissions for accuracy.
            comm_res = self.db.client.table("affiliate_commissions").select("amount_commission").eq("referrer_id", user_id).execute()
            total_comm = sum(float(x["amount_commission"]) for x in comm_res.data) if comm_res.data else 0.0
            
            return {
                "code": code,
                "count": count,
                "earnings": total_comm,
                "tier_info": self._calculate_tier(count)
            }
        except:
            return {
                "code": "--", "count": 0, "earnings": 0,
                "tier_info": {"name": "Starter", "rate": "10%", "next": 10, "color": "#aaaaaa"}
            }

    def _calculate_tier(self, count):
        """Helper to determine tier based on referral count"""
        if count >= 100:
            return {"name": "INSTITUTIONAL", "rate": "25%", "next": None, "color": "#00FFAA"}
        elif count >= 50:
            return {"name": "PLATINUM", "rate": "20%", "next": 100, "color": "#E5E4E2"}
        elif count >= 10:
            return {"name": "GOLD MEMBER", "rate": "15%", "next": 50, "color": "#FFD700"}
        else:
            return {"name": "STARTER", "rate": "10%", "next": 10, "color": "#aaaaaa"}
