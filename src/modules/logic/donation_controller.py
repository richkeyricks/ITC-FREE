# ══════════════════════════════════════════════════════════════════════════════
# 💝 DONATION CONTROLLER (LOGIC LAYER)
# 🎯 ROLE: Bridges UI with Payment Service for Donations.
# ══════════════════════════════════════════════════════════════════════════════

import uuid
from modules.logic.payment_service import PaymentService
from CTkMessagebox import CTkMessagebox

class DonationController:
    """
    Handles the donation flow:
    1. Initiates Midtrans transaction.
    2. Monitors status.
    3. Updates database and UI on success.
    """

    def __init__(self, parent_app):
        self.app = parent_app
        self.payment_service = PaymentService(parent_app.db_manager)

    def initiate_donation(self, amount, message=""):
        """
        Starts the donation process with Midtrans Snap.
        """
        if amount < 1000:
            CTkMessagebox(title="Nominal Terlalu Kecil", message="Minimal donasi adalah Rp 1.000", icon="warning")
            return

        # Use a fake preset_id for donation
        donation_id = f"DONATE-{uuid.uuid4().hex[:6].upper()}"
        
        # We wrap the success callback
        def on_success():
            self.app.db_manager.process_donation_success(amount, message)
            self.app.safe_ui_update(lambda: CTkMessagebox(
                title="Donasi Berhasil! 👑", 
                message=f"Terima kasih atas kontribusi Anda sebesar Rp {amount:,}!\nNama Anda akan diperbarui di Leaderboard jika mencapai ambang batas.",
                icon="check"
            ))
            # Refresh leaderboard if user is on that page
            if hasattr(self.app, 'current_page') and self.app.current_page == "donation":
                 self.app.show_page("donation")

        # Call PaymentService
        # Note: PaymentService currently expects preset_id and preset_name for Marketplace.
        # We pass "DONATION" as preset_id to identify it.
        success, res = self.payment_service.create_transaction(
            preset_id=donation_id,
            preset_name="Community Donation",
            amount=amount,
            on_success=on_success
        )

        if success:
            # Open browser for payment
            self.payment_service.open_payment_browser(res["redirect_url"])
            return True
        else:
            CTkMessagebox(title="Gagal", message=f"Gagal membuat transaksi: {res}", icon="cancel")
            return False

    def get_hall_of_fame(self, min_amount=50000):
        """Fetches consolidated leaderboard from DB"""
        return self.app.db_manager.get_hall_of_fame(min_amount)
