import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class StrictChatPopup(ctk.CTkToplevel):
    """
    A custom popup that CANNOT be closed until the user replies (for DMs).
    Follows Gravity Dev Rules: Modular & SoC.
    """
    def __init__(self, parent, title, message, msg_id, db_manager, is_strict=True):
        super().__init__(parent)
        self.db_manager = db_manager
        self.msg_id = msg_id
        
        # Window Config
        self.title(title)
        self.geometry("400x500")
        self.resizable(False, False)
        self.attributes('-topmost', True)
        
        # Remove Title Bar if Strict (No X button)
        if is_strict:
            self.overrideredirect(True)
            self.protocol("WM_DELETE_WINDOW", lambda: None)
            
        # Center Window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 500) // 2
        self.geometry(f"+{x}+{y}")
        
        # UI Elements
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) 
        
        # Header
        header = ctk.CTkFrame(self, fg_color="#dc3545" if is_strict else "#0d6efd", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        
        lbl_title = ctk.CTkLabel(header, text=title, font=("Segoe UI Bold", 16), text_color="white")
        lbl_title.pack(pady=15)
        
        # Message Body
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        lbl_msg = ctk.CTkLabel(body, text=message, font=("Segoe UI", 14), wraplength=360, justify="left")
        lbl_msg.pack(fill="x")
        
        # Reply Section
        reply_frame = ctk.CTkFrame(self, fg_color="transparent")
        reply_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        ctk.CTkLabel(reply_frame, text="Your Reply:", font=("Consolas", 12)).pack(anchor="w", pady=(0, 5))
        
        self.txt_reply = ctk.CTkTextbox(reply_frame, height=100, font=("Consolas", 12))
        self.txt_reply.pack(fill="x", pady=(0, 10))
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        
        def _send_reply():
            reply = self.txt_reply.get("0.0", "end").strip()
            if not reply:
                CTkMessagebox(title="Required", message="Please type a reply to continue.", icon="warning")
                return
            
            success, error_msg = self.db_manager.reply_to_admin(reply, original_msg_id=self.msg_id)
            if success:
                self.db_manager.mark_message_read(self.msg_id)
                self.destroy()
                CTkMessagebox(title="Sent", message="Reply sent! You can now continue.", icon="check")
            else:
                CTkMessagebox(title="Error", message=f"Failed to send reply: {error_msg}", icon="cancel")

        self.btn_send = ctk.CTkButton(btn_frame, text="SEND REPLY & CLOSE", fg_color="#198754", 
                                      hover_color="#157347", font=("Segoe UI Bold", 12), height=40,
                                      command=_send_reply)
        self.btn_send.pack(fill="x")
        
        if not is_strict:
            self.btn_send.configure(text="SEND REPLY (OPTIONAL)")
            ctk.CTkButton(btn_frame, text="CLOSE", fg_color="transparent", border_width=1, 
                          text_color="gray", command=self.destroy).pack(fill="x", pady=(10, 0))
