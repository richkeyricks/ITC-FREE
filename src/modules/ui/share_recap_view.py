import customtkinter as ctk
import webbrowser
from ui_theme import THEME_DARK, FONTS
from constants.api_endpoints import WEB_BASE_URL

class ShareRecapView(ctk.CTkToplevel):
    """
    Luxury 'Session Summary' popup triggered after stopping the copier.
    Encourages viral sharing of aggregated session stats.
    """
    def __init__(self, parent, session_data):
        super().__init__(parent)
        self.parent = parent
        self.session_data = session_data
        
        # Config
        self.title("Session Complete")
        self.geometry("400x520")
        self.resizable(False, False)
        
        # Center Window
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (400/2)
        y = (hs/2) - (520/2)
        self.geometry('%dx%d+%d+%d' % (400, 520, x, y))
        
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        self.configure(fg_color=theme["bg_primary"])
        
        # --- UI CONTENT ---
        
        # Gradient/Hero Header
        hero = ctk.CTkFrame(self, height=140, fg_color="#0d1117", corner_radius=0)
        hero.pack(fill="x")
        
        ctk.CTkLabel(hero, text="✨", font=("Segoe UI Emoji", 48)).place(relx=0.5, rely=0.35, anchor="center")
        ctk.CTkLabel(hero, text="SESSION COMPLETE", font=("Segoe UI", 12, "bold"), text_color="#8b949e").place(relx=0.5, rely=0.65, anchor="center")
        
        # Main Card
        card = ctk.CTkFrame(self, fg_color=theme["bg_secondary"], corner_radius=15, border_width=1, border_color="#30363d")
        card.place(relx=0.5, rely=0.3, anchor="n", relwidth=0.85, relheight=0.55)
        
        # Profit Hero Number
        profit = session_data.get("profit", 0.0)
        color = "#3fb950" if profit >= 0 else "#f85149"
        sign = "+" if profit >= 0 else ""
        
        ctk.CTkLabel(card, text="Total Profit", font=("Segoe UI", 12), text_color="#8b949e").pack(pady=(25, 5))
        ctk.CTkLabel(card, text=f"{sign}${profit:,.2f}", font=("Outfit", 36, "bold"), text_color=color).pack(pady=(0, 20))
        
        # Divider
        ctk.CTkFrame(card, height=1, fg_color="#30363d").pack(fill="x", padx=30, pady=10)
        
        # Stats Grid
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(pady=10)
        
        self._stat(grid, "Trades", str(session_data.get("trades", 0)), 0, 0, theme)
        self._stat(grid, "Win Rate", f"{session_data.get('win_rate', 0)}%", 0, 1, theme)
        self._stat(grid, "Best Pair", session_data.get("best_pair", "N/A"), 1, 0, theme)
        self._stat(grid, "Duration", session_data.get("duration", "0h"), 1, 1, theme)

        # Viral Action Helper
        ctk.CTkLabel(self, text="The market yielded to your strategy.\nShare your dominance.", 
                     font=("Segoe UI", 10, "italic"), text_color="#8b949e", justify="center").pack(side="bottom", pady=(0, 80))

        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=30, pady=30)
        
        self.btn_share = ctk.CTkButton(btn_frame, text="Generate Viral Link 🚀", height=45,
                                      font=("Segoe UI", 13, "bold"), fg_color="#3fb950", hover_color="#2ea043",
                                      command=self._generate_link)
        self.btn_share.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(btn_frame, text="Dismiss", height=35, fg_color="transparent", 
                      font=("Segoe UI", 12), text_color="#8b949e", hover_color=theme["bg_tertiary"],
                      command=self.destroy).pack(fill="x")

    def _stat(self, parent, label, value, row, col, theme):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=row, column=col, padx=20, pady=10)
        ctk.CTkLabel(f, text=label, font=("Segoe UI", 10), text_color="#8b949e").pack()
        ctk.CTkLabel(f, text=str(value), font=("Segoe UI", 14, "bold"), text_color=theme["text_primary"]).pack()

    def _generate_link(self):
        """Generates the Vercel Viral Link"""
        import os
        user = os.getenv("USER_NAME", "Trader")
        # Sanitize spaces for URL
        user_safe = user.replace(" ", "%20")
        profit_safe = f"{self.session_data.get('profit', 0):.2f}"
        
        # Use user's Vercel Domain (or fallback to placeholder if not set)
        # In production, this should be config-driven
        base_url = WEB_BASE_URL 
        
        final_url = f"{base_url}/share/{user_safe}/{profit_safe}"
        
        self.btn_share.configure(text="Link Opened in Browser! 🌍", state="disabled")
        webbrowser.open(final_url)
        
        # Auto-dismiss after 2s
        self.after(2000, self.destroy)
