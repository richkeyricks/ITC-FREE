# ══════════════════════════════════════════════════════════════════════════════
# 🏦 PAYMENT VIEW (PRESENTATION LAYER)
# 🎨 STYLE: Glowing Cyberpunk, Trust-Inducing
# ══════════════════════════════════════════════════════════════════════════════

import customtkinter as ctk
import time
import webbrowser
from CTkMessagebox import CTkMessagebox
from modules.logic.payment_service import PaymentService
from utils.currency import format_currency

class PaymentView(ctk.CTkToplevel):
    def __init__(self, parent, preset_data, payment_service=None):
        super().__init__(parent)
        self.title("SECURE PAYMENT GATEWAY - 🔒 BANKING GRADE")
        self.geometry("450x600")
        self.preset_data = preset_data
        self.payment_service = payment_service
        self.transaction_data = None
        self.is_checking = False
        self.translator = parent.translator if hasattr(parent, 'translator') else None

        # --- UI SETUP ---
        self._setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # --- AUTO TRIGGER ---
        self.after(1000, self.initiate_transaction)

    def _setup_ui(self):
        # Header (Neon)
        self.frame_main = ctk.CTkFrame(self, fg_color="#101014", corner_radius=0)
        self.frame_main.pack(fill="both", expand=True)

        self.lbl_title = ctk.CTkLabel(self.frame_main, text="PAYMENT GATEWAY", 
                                      font=("Roboto", 20, "bold"), text_color="#00FFAA")
        self.lbl_title.pack(pady=(30, 10))

        # Item Info
        self.frm_item = ctk.CTkFrame(self.frame_main, fg_color="#1A1A20", corner_radius=15, border_width=1, border_color="#333")
        self.frm_item.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.frm_item, text=f"Item: {self.preset_data.get('name', 'Unknown')}", font=("Roboto", 14)).pack(pady=5)
        ctk.CTkLabel(self.frm_item, text=f"Total: {format_currency(self.preset_data.get('price', 0))}", font=("Roboto", 18, "bold"), text_color="#FFD700").pack(pady=5)

        # Status Status
        self.lbl_status = ctk.CTkLabel(self.frame_main, text="Initializing Secure Channel...", font=("Consolas", 12), text_color="grey")
        self.lbl_status.pack(pady=20)

        # Action Buttons
        self.btn_pay = ctk.CTkButton(self.frame_main, text="OPEN PAYMENT PAGE ↗", 
                                     fg_color="#0077EE", hover_color="#0055AA", 
                                     command=self.open_browser, state="disabled")
        self.btn_pay.pack(pady=10)

        # Loading Animation/Pulse (Placeholder logic)
        self.progress = ctk.CTkProgressBar(self.frame_main, width=300, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start()

    def initiate_transaction(self):
        """Step 1: Get Token from Edge Function"""
        self.lbl_status.configure(text="🔒 Handshaking with Cloud Vault...")
        
        success, response = self.payment_service.create_transaction(
            self.preset_data.get('id'),
            self.preset_data.get('name'),
            self.preset_data.get('price')
        )

        if success:
            self.transaction_data = response
            self.lbl_status.configure(text="✅ Secure Channel Established.\nWaiting for Payment...", text_color="#00FFAA")
            self.btn_pay.configure(state="normal")
            self.progress.stop()
            self.progress.configure(mode="determinate", value=1)
            
            # Auto Open
            self.open_browser()
            
            # Start Polling
            self.start_polling(response['order_id'])
        else:
            self.lbl_status.configure(text=f"❌ FAILED: {response}", text_color="#FF5555")
            self.progress.stop()

    def open_browser(self):
        if self.transaction_data and self.transaction_data.get('redirect_url'):
            webbrowser.open(self.transaction_data['redirect_url'])

    def start_polling(self, order_id):
        self.is_checking = True
        self._poll_loop(order_id)

    def _poll_loop(self, order_id):
        if not self.is_checking: return

        # In real implementation, verify_payment queries Supabase table 'marketplace_orders'
        # status = self.payment_service.check_payment_status(order_id)
        # Using a mock sleep loop here since db connection is via db_manager
        
        # self.after(5000, lambda: self._poll_loop(order_id))
        pass 

    def on_close(self):
        self.is_checking = False
        self.destroy()
