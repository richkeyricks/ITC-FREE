import os
import sys
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from modules.db.supabase_client import SupabaseManager

class MockTranslator:
    def get(self, key, default=None):
        data = {
            "cycle_monthly": "MONTHLY",
            "cycle_yearly": "YEARLY",
            "cycle_lifetime": "LIFETIME",
            "tier_free": "FREE",
            "tier_gold": "GOLD PRO",
            "tier_platinum": "PLATINUM VIP",
            "tier_institutional": "INSTITUTIONAL",
            "tier_admin": "ELITE ADMIN"
        }
        return data.get(key, default or key)

class MockParent:
    def __init__(self, dm):
        self.db_manager = dm
        self.translator = MockTranslator()

def test_logic():
    print("=== SUBSCRIPTION CYCLE VERIFICATION ===")
    dm = SupabaseManager()
    
    # Mock profiles
    profiles = [
        {"name": "Monthly User", "subscription_tier": "GOLD", "premium_until": (datetime.now() + timedelta(days=30)).isoformat()},
        {"name": "Yearly User", "subscription_tier": "PLATINUM", "premium_until": (datetime.now() + timedelta(days=365)).isoformat()},
        {"name": "Lifetime User", "subscription_tier": "INSTITUTIONAL", "premium_until": (datetime.now() + timedelta(days=5000)).isoformat()},
        {"name": "Standard User", "subscription_tier": "STANDARD", "premium_until": None},
    ]

    for p in profiles:
        try:
            print(f"Testing Profile: {p['name']}")
            # Use instance methods
            cycle = dm.get_user_cycle(p)
            tier = dm.get_user_tier(p)
            print(f"   Tier Detected: {tier}")
            print(f"   Cycle Detected: {cycle}")
            
            # Simulate Dashboard logic
            parent = MockParent(dm)
            cycle_text = parent.translator.get(f"cycle_{cycle.lower()}")
            label_key = f"tier_{tier.lower()}"
            if tier == "GOLD": label_key = "tier_gold" # Match specific mapping
            
            display = parent.translator.get(label_key)
            if tier != "STANDARD":
                display += f" • {cycle_text}"
                
            print(f"   => Badge Result: {display}")
        except Exception as e:
            import traceback
            print(f"   !! ERROR: {e}")
            traceback.print_exc()
        print("-" * 50)

if __name__ == "__main__":
    test_logic()
