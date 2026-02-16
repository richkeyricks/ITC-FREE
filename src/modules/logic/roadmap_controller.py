# ══════════════════════════════════════════════════════════════════════════════
# 🗺️ ROADMAP CONTROLLER (LOGIC LAYER)
# 🎯 ROLE: Governance rules for the Council.
# ══════════════════════════════════════════════════════════════════════════════

from CTkMessagebox import CTkMessagebox

class RoadmapController:
    """
    Manages the Project Roadmap (Council).
    Enforces rules:
    - Tier 1 (Voter): >50k Donation
    - Tier 2 (Architect): >500k Donation
    """

    def __init__(self, parent_app):
        self.app = parent_app
        self.db = parent_app.db_manager

    def get_user_tier_status(self):
        """Returns (is_voter, is_architect, current_total)"""
        total = self.db.get_user_total_donation()
        return (total >= 50000, total >= 500000, total)

    def fetch_items(self):
        """Fetches items for the UI"""
        return self.db.get_roadmap_items()

    def vote_item(self, item_id):
        """Handles voting logic"""
        is_voter, _, total = self.get_user_tier_status()
        
        if not is_voter:
            CTkMessagebox(title="Akses Ditolak", 
                          message=f"🔒 Maaf, Voting hanya untuk Elite Backer (Min. Donasi Rp 50.000).\nTotal Donasi Anda: Rp {int(total):,}", 
                          icon="cancel")
            return False

        success, msg = self.db.vote_roadmap_item(item_id)
        if success:
            # Silent success or toast could go here
            return True
        else:
            if msg == "Already voted":
                CTkMessagebox(title="Info", message="Anda sudah memberikan suara untuk fitur ini.", icon="info")
            else:
                CTkMessagebox(title="Error", message=f"Gagal voting: {msg}", icon="cancel")
            return False

    def submit_proposal(self, title, description):
        """Handles new proposal submission"""
        _, is_architect, total = self.get_user_tier_status()
        
        if not is_architect:
            CTkMessagebox(title="Akses Ditolak", 
                          message=f"🔒 Fitur Proposal Khusus 'The Architect' (Min. Donasi Rp 500.000).\nTotal Donasi Anda: Rp {int(total):,}", 
                          icon="cancel")
            return False

        if len(title) < 5 or len(description) < 10:
            CTkMessagebox(title="Error", message="Judul atau Deskripsi terlalu pendek.", icon="warning")
            return False

        success = self.db.submit_roadmap_proposal(title, description)
        if success:
            CTkMessagebox(title="Sukses", message="Proposal berhasil diajukan! Menunggu voting komunitas.", icon="check")
            return True
        else:
            CTkMessagebox(title="Error", message="Gagal mengajukan proposal.", icon="cancel")
            return False
