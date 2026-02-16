# ══════════════════════════════════════════════════════════════════════════════
# 📤 UPLOAD PRESET VIEW (UI Layer)
# 🛡️ FLOW: Verify -> Details -> Publish
# ══════════════════════════════════════════════════════════════════════════════

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import threading
from modules.logic.verification_service import VerificationService
from modules.logic.config_aggregator import ConfigAggregator

class UploadPresetView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#101014")
        self.controller = controller
        self.verifier = VerificationService(controller.db_manager)
        
        self._setup_ui()
        
    def _setup_ui(self):
        # --- HEADER ---
        ctk.CTkLabel(self, text="PUBLISH STRATEGY (MARKETPLACE)", 
                     font=("Roboto", 24, "bold"), text_color="#00FFAA").pack(pady=20)

        # --- WIZARD CONTAINER ---
        self.frm_wizard = ctk.CTkFrame(self, fg_color="#1A1A20", corner_radius=15, width=600)
        self.frm_wizard.pack(pady=10, padx=20, fill="both", expand=True)
        
        # --- STEP 1: VERIFICATION ---
        self.step_verify = ctk.CTkFrame(self.frm_wizard, fg_color="transparent")
        self.step_verify.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(self.step_verify, text="STEP 1: PROOF OF PROFIT", 
                     font=("Roboto", 18, "bold"), text_color="white").pack(pady=10)
        
        ctk.CTkLabel(self.step_verify, text="We analyze your local MT5 history to ensure\nstrategies are profitable (>2% ROI) before listing.",
                     font=("Roboto", 12), text_color="gray").pack(pady=5)
                     
        self.btn_verify = ctk.CTkButton(self.step_verify, text="🧬 RUN DIAGNOSTIC SCAN", 
                                        fg_color="#3B8ED0", height=50, 
                                        font=("Roboto", 14, "bold"),
                                        command=self.run_verification)
        self.btn_verify.pack(pady=30)
        
        self.lbl_status = ctk.CTkLabel(self.step_verify, text="", font=("Consolas", 12))
        self.lbl_status.pack(pady=10)

        # --- STEP 2: DETAILS FORM (Effective Hidden) ---
        self.step_details = ctk.CTkFrame(self.frm_wizard, fg_color="transparent")
        
        ctk.CTkLabel(self.step_details, text="STEP 2: STRATEGY DETAILS", 
                     font=("Roboto", 18, "bold"), text_color="white").pack(pady=10)
                     
        self.entry_title = ctk.CTkEntry(self.step_details, placeholder_text="Strategy Name (e.g. Gold Scalper X)", width=400)
        self.entry_title.pack(pady=10)
        
        self.entry_desc = ctk.CTkTextbox(self.step_details, height=100, width=400)
        self.entry_desc.insert("0.0", "Describe your logic, TF, and Pairs...")
        self.entry_desc.pack(pady=10)
        
        self.entry_price = ctk.CTkEntry(self.step_details, placeholder_text="Price (USD) - 0 for Free", width=400)
        self.entry_price.pack(pady=10)
        
        self.btn_publish = ctk.CTkButton(self.step_details, text="🚀 PUBLISH TO MARKET", 
                                         fg_color="#00AA66", height=40, font=("Roboto", 14, "bold"),
                                         command=self.submit_preset)
        self.btn_publish.pack(pady=20)
        
    def run_verification(self):
        self.btn_verify.configure(state="disabled", text="SCANNING DB...")
        self.lbl_status.configure(text="Scanning MT5 History...", text_color="white")
        
        def _task():
            success, msg, metrics = self.verifier.run_full_verification()
            self.controller.safe_ui_update(self._on_verify_complete, success, msg, metrics)
            
        threading.Thread(target=_task, daemon=True).start()

    def _on_verify_complete(self, success, msg, metrics):
        if not self.winfo_exists(): return
        self.btn_verify.configure(state="normal", text="🧬 RUN DIAGNOSTIC SCAN")
        
        if success:
            self.lbl_status.configure(text=f"✅ VERIFIED! ROI: {metrics['roi']}% | WR: {metrics['win_rate']}%", text_color="#00FFAA")
            # Switch to Step 2
            self.step_verify.pack_forget()
            self.step_details.pack(fill="both", expand=True, padx=20, pady=20)
            self.verified_metrics = metrics
        else:
            self.lbl_status.configure(text=f"❌ FAILED: {msg}", text_color="#FF3333")
            CTkMessagebox(title="Verification Failed", message=msg, icon="cancel")

    def submit_preset(self):
        title = self.entry_title.get()
        desc = self.entry_desc.get("0.0", "end").strip()
        price = self.entry_price.get()
        
        if not title or not price:
            CTkMessagebox(title="Error", message="Title and Price are required.", icon="warning")
            return

        # Fetch Current Config as JSON
        # Assuming ConfigAggregator can dump current state
        config_data = ConfigAggregator.get_current_config(self.controller)
        
        success, msg = self.verifier.publish_preset(title, desc, price, config_data, self.verified_metrics)
        
        if success:
            CTkMessagebox(title="Success", message="Strategy Listed on Marketplace!", icon="check")
            # Close / Return
            if hasattr(self.controller, 'start_modal'): # If modal
                self.destroy()
            else:
                self.controller.show_page("dashboard")
        else:
            CTkMessagebox(title="Error", message=f"Publish Failed: {msg}", icon="cancel")
