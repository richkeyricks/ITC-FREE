import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from ui_theme import THEME_DARK, FONTS

class PublisherDialog(ctk.CTkToplevel):
    """
    Publisher Studio Modal Dialog.
    Allows user to Mint Assets with full metadata (Name, Desc, Price, Visibility).
    """
    def __init__(self, parent, title="Publisher Studio"):
        super().__init__(parent)
        self.output_data = None
        
        # Theme
        theme = THEME_DARK
        self.configure(fg_color=theme["bg_secondary"])
        
        # Window Setup
        self.title(title)
        self.geometry("420x650") # Taller to prevent button clipping
        self.resizable(False, False)
        self.grab_set() # Modal behavior
        self.attributes("-topmost", True)
        
        # Center Window
        try:
            x = parent.winfo_x() + (parent.winfo_width()//2) - 210
            y = parent.winfo_y() + (parent.winfo_height()//2) - 325
            self.geometry(f"+{x}+{y}")
        except: pass

        # --- UI LAYOUT ---
        # 1. Header (Premium Gradient effect simulation via color)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(25, 10))
        
        ctk.CTkLabel(header_frame, text="💎 MINT DIGITAL ASSET", font=("Segoe UI Bold", 20), text_color=theme["accent_primary"]).pack()
        ctk.CTkLabel(header_frame, text="Create your signature trading preset.", font=("Segoe UI", 12), text_color=theme["text_secondary"]).pack()

        # 2. Actions (Packed FIRST to stick to bottom)
        self.btn_row = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_row.pack(side="bottom", fill="x", padx=30, pady=30)
        
        ctk.CTkButton(self.btn_row, text="CANCEL", fg_color="transparent", border_width=1, border_color=theme["text_disabled"], 
                     text_color=theme["text_secondary"], width=100, height=40, hover_color=theme["bg_tertiary"],
                     command=self.destroy).pack(side="left", padx=(0, 10))
        
        self.btn_mint = ctk.CTkButton(self.btn_row, text="SAVE TO VAULT", fg_color=theme["accent_primary"], hover_color=theme["accent_primary_hover"], 
                     width=240, height=40, font=("Segoe UI Bold", 13), text_color="white",
                     command=self._submit)
        self.btn_mint.pack(side="right")

        # 3. Form Container (Expands to fill remaining space)
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Preset Name", font=FONTS["body_bold"], text_color=theme["text_primary"]).pack(anchor="w", pady=(5, 2))
        self.entry_name = ctk.CTkEntry(form_frame, placeholder_text="e.g. Gold Scalper V1", width=360, height=40,
                                      fg_color=theme["bg_tertiary"], border_color=theme["border_default"], text_color="white")
        self.entry_name.pack(pady=(0, 10))
        
        # Description
        ctk.CTkLabel(form_frame, text="Description", font=FONTS["body_bold"], text_color=theme["text_primary"]).pack(anchor="w", pady=(5, 2))
        self.entry_desc = ctk.CTkTextbox(form_frame, width=360, height=100, 
                                        fg_color=theme["bg_tertiary"], border_color=theme["border_default"], text_color="white")
        self.entry_desc.insert("0.0", "Strategy logic, Timeframe, Risk profile...")
        self.entry_desc.pack(pady=(0, 15))
        
        # 4. Mode Selection (Premium Segmented)
        ctk.CTkLabel(form_frame, text="Distribution Mode", font=FONTS["body_bold"], text_color=theme["text_primary"]).pack(anchor="w", pady=(5, 2))
        self.mode_var = ctk.StringVar(value="PRIVATE")
        
        self.seg_mode = ctk.CTkSegmentedButton(form_frame, values=["PRIVATE VAULT", "PUBLIC STORE"], 
                                              command=self._toggle_mode, variable=self.mode_var, width=360, height=35,
                                              selected_color=theme["accent_primary"], unselected_color=theme["bg_tertiary"],
                                              selected_hover_color=theme["accent_primary_hover"], font=FONTS["body_bold"])
        self.seg_mode.pack(pady=(0, 10))

        # 5. Monetization (Hidden by default)
        self.price_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.price_frame, text="Asset Price ($)", font=FONTS["body_bold"], text_color=theme["accent_success"]).pack(anchor="w", pady=(5, 2))
        self.entry_price = ctk.CTkEntry(self.price_frame, placeholder_text="0 (Free)", width=360, height=40,
                                       fg_color=theme["bg_tertiary"], border_color=theme["accent_success"], text_color="white")
        self.entry_price.insert(0, "0")
        self.entry_price.pack()
        
        ctk.CTkLabel(self.price_frame, text="* 20% Platform Fee applies to sales.", font=("Segoe UI", 10), text_color=theme["text_disabled"]).pack(anchor="w", pady=2)
    
    def _toggle_mode(self, val):
        if val == "PUBLIC STORE":
            self.price_frame.pack(pady=5, fill="x")
            self.btn_mint.configure(text="PUBLISH PROJECT")
        else:
            self.price_frame.pack_forget()
            self.btn_mint.configure(text="SAVE TO VAULT")
            
    def _submit(self):
        name = self.entry_name.get().strip()
        desc = self.entry_desc.get("0.0", "end").strip()
        is_public = self.mode_var.get() == "PUBLIC STORE"
        
        # Validation
        if not name or len(name) < 3:
            CTkMessagebox(title="Validation Error", message="Name matches criteria (Min 3 chars).", icon="warning")
            return
            
        try:
            price = float(self.entry_price.get())
        except:
            price = 0.0

        self.output_data = {
            "name": name,
            "description": desc,
            "is_public": is_public,
            "price": price
        }
        self.destroy()

    def get_input(self):
        """Block until window closed, then return data"""
        self.wait_window()
        return self.output_data
