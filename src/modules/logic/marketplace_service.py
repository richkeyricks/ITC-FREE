import logging
import threading
from modules.db.supabase_client import SupabaseManager
from modules.logic.verification_service import VerificationService

class MarketplaceService:
    """
    Logic for the Gravity Marketplace. 
    Handles strategy discovery and transaction flows.
    """
    
    _db = SupabaseManager()
    
    @classmethod
    def get_verified_strategies(cls):
        """Fetches all public & verified strategies (with Mock Fallback)."""
        # 1. Try Real DB (Marketplace Presets)
        if cls._db.client:
            try:
                res = cls._db.client.table("marketplace_presets") \
                    .select("*") \
                    .eq("is_verified", True) \
                    .order("verified_win_rate", desc=True) \
                    .execute()
                if res.data:
                    return res.data
            except Exception as e:
                logging.error(f"// Marketplace Real-DB Error: {e}")
        
        # 2. Fallback to Manager's Mock Data (User Presets/System Mocks)
        # This ensures the UI is NEVER empty during demos/offline
        return cls._db.get_marketplace_presets()

    @classmethod
    def check_ownership(cls, user_id, preset_id):
        """Checks if a user already owns a specific strategy."""
        if not cls._db.client: return False
        
        try:
            res = cls._db.client.table("marketplace_orders") \
                .select("order_id") \
                .eq("buyer_id", user_id) \
                .eq("preset_id", preset_id) \
                .eq("status", "COMPLETED") \
                .execute()
            return len(res.data) > 0
        except:
            return False

    @classmethod
    def initiate_purchase(cls, user_id, tier, price_usd, idr_price_str=None, currency="IDR", on_success=None):
        """
        Starts the purchase flow securely using PaymentService.
        """
        from modules.logic.payment_service import PaymentService
        
        # Initialize Payment Service with our DB instance
        pay_service = PaymentService(cls._db)
        
        # Determine Amount & Currency
        final_currency = str(currency).upper()
        
        if final_currency == "USD":
            # Strip formatting from USD price
            final_amount = float(str(price_usd).replace("$", "").replace(",", "").strip())
        else:
            # Fallback to IDR (Default)
            if idr_price_str and "Rp" in idr_price_str:
                try:
                    # Convert "Rp 450.000" -> 450000
                    final_amount = float(idr_price_str.replace("Rp", "").replace(".", "").strip())
                except:
                    final_amount = float(str(price_usd).replace(",", "")) # Fallback
            else:
                final_amount = float(str(price_usd).replace(",", ""))
        
        # Use PaymentService to handle the complex logic (DB Sync + Midtrans + Monitoring)
        success, result = pay_service.create_transaction(
            preset_id=tier, # Using Tier as ID for subscription
            preset_name=f"ITC {tier} Membership",
            amount=final_amount,
            currency=final_currency,
            on_success=on_success
        )
        
        if success:
             return {
                "token": result.get("token"),
                "redirect_url": result.get("redirect_url"),
                "status": "success"
            }
        
        logging.error(f"// Payment Init Failed: {result}")
        return {
            "token": None,
            "redirect_url": None,
            "status": "error"
        }

    @classmethod
    def install_to_vault(cls, user_id, preset_data):
        """Copies a purchased strategy into the user's personal vault."""
        if not cls._db.client: return False, "DB Connection Lost"
        
        try:
            # 1. Prepare data (sanitize to match user_presets schema)
            vault_payload = {
                "user_id": user_id,
                "name": f"[STORE] {preset_data['title']}",
                "description": preset_data.get('description', ''),
                "config_json": preset_data.get('config_data', preset_data.get('config_json', {})),
                "is_public": False
            }
            
            # 2. Insert into user_presets
            res = cls._db.client.table("user_presets").insert(vault_payload).execute()
            
            if res.data:
                return True, "Installation successful! Check 'Trading Rules' menu."
            return False, "Failed to clone preset to vault."
            
        except Exception as e:
            return False, str(e)

    @classmethod
    def publish_strategy_flow(cls, title, desc, price, config_json):
        """
        Orchestrates the Verification/Selling flow.
        1. Runs Local Verification
        2. If passed, uploads to Marketplace
        """
        verifier = VerificationService(cls._db)
        
        # 1. Verify
        is_valid, reason, metrics = verifier.run_full_verification()
        
        if not is_valid:
            return False, f"Verification Failed: {reason}", metrics
        
        # 2. Publish
        success, msg = verifier.publish_preset(title, desc, price, config_json, metrics)
        
        return success, msg, metrics
