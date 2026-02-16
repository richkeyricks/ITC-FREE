import customtkinter as ctk
import time
import webbrowser
from ui_theme import THEME_DARK, FONTS

class ToastNotification(ctk.CTkToplevel):
    """
    Non-intrusive Toast Notification for Real-time Success events.
    Floats in bottom-right corner and auto-dismisses.
    """
    def __init__(self, parent, title, message, url_action=None, icon_name="info", btn_text="Check Details", color_theme="green"):
        super().__init__(parent)
        self.parent = parent
        self.url_action = url_action

        
        # Window Setup
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="transparent")
        
        # Theme
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        
        # Theme Colors
        colors = {
            "green": "#3fb950", "red": "#f85149", "blue": "#3b82f6", "gold": "#d29922"
        }
        border_col = colors.get(color_theme, "#3fb950")
        
        # Container
        self.container = ctk.CTkFrame(self, fg_color=theme["bg_secondary"], corner_radius=12,
                                     border_width=1, border_color=border_col)
        self.container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Content
        # Row 1: Icon + Title
        row1 = ctk.CTkFrame(self.container, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=(10, 0))
        
        icons = {
            "check": "✅", "warning": "⚠️", "info": "ℹ️", "money": "💰", "lock": "🛑", "trophy": "🏆"
        }
        icon_char = icons.get(icon_name, "🔔")
        
        ctk.CTkLabel(row1, text=icon_char, font=("Segoe UI Emoji", 18)).pack(side="left")
        ctk.CTkLabel(row1, text=title, font=("Segoe UI", 12, "bold"), 
                     text_color=theme["text_primary"]).pack(side="left", padx=10)
        
        # Close Button
        ctk.CTkButton(row1, text="×", width=20, height=20, fg_color="transparent", 
                      text_color=theme["text_secondary"], hover_color=theme["bg_tertiary"],
                      command=self._dismiss).pack(side="right")
        
        # Row 2: Message
        ctk.CTkLabel(self.container, text=message, font=("Segoe UI", 12),
                     text_color=theme["text_secondary"], wraplength=250, justify="left").pack(anchor="w", padx=15, pady=(5, 10))
        
        # Row 3: Action Button (Optional)
        if url_action:
            btn = ctk.CTkButton(self.container, text=btn_text, height=28,
                               font=("Segoe UI", 11, "bold"),
                               fg_color=border_col, hover_color=border_col,
                               text_color="white", corner_radius=6,
                               command=self._on_click)
            btn.pack(fill="x", padx=15, pady=(0, 10))
            
        # Animation & Placement
        self._animate_in()
        
        # Auto-Dismiss Timer
        self._dismiss_job = self.after(5000, self._animate_out)

    def _animate_in(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        window_width = 300
        window_height = 130 if self.url_action else 90
        
        target_x = screen_width - window_width - 20
        target_y = screen_height - window_height - 60 # Above taskbar
        
        self.geometry(f"{window_width}x{window_height}+{target_x}+{target_y}")
        
        # Simple Fade In (Alpha)
        self.attributes("-alpha", 0.0)
        for i in range(11):
            self.attributes("-alpha", i * 0.1)
            self.update()
            time.sleep(0.02)
            
    def _animate_out(self):
        try:
            for i in range(10, -1, -1):
                self.attributes("-alpha", i * 0.1)
                self.update()
                time.sleep(0.02)
            self.destroy()
        except:
            pass # Widget might already be destroyed
            
    def _dismiss(self):
        if hasattr(self, '_dismiss_job'):
            self.after_cancel(self._dismiss_job)
        self._animate_out()
        
    def _on_click(self):
        if self.url_action:
            webbrowser.open(self.url_action)
        self._dismiss()
