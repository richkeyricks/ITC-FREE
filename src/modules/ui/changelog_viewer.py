# src/modules/ui/changelog_viewer.py
"""
Changelog Viewer Module - Modular UI Component
Handles displaying version history in a beautiful popup.

Follows Gravity Dev Rules:
- Single Responsibility Principle (SRP)
- Separation of Concerns (SoC)
- Clean, Maintainable Code
"""
import customtkinter as ctk


from constants.changelog_data import CHANGELOG_DATA


# --- STYLES ---
STYLES = {
    "bg_primary": "#0d1117",
    "accent_primary": "#0088cc",
    "card_bg": "#21262d",
    "card_border": "#30363d",
    "text_primary": "#e6edf3",
    "text_secondary": "#8b949e",
    "btn_bg": "#21262d",
    "btn_hover": "#30363d",
}


class ChangelogViewer:
    """
    Singleton Changelog Popup Viewer.
    
    Usage:
        from modules.ui.changelog_viewer import ChangelogViewer
        ChangelogViewer.show(parent_window)
    """
    _window = None
    
    @classmethod
    def show(cls, parent):
        """Opens the changelog popup. If already open, brings it to front."""
        # --- SINGLETON CHECK ---
        if cls._window is not None and cls._window.winfo_exists():
            cls._window.lift()
            cls._window.focus_force()
            return
        
        # --- CREATE WINDOW ---
        cls._window = ctk.CTkToplevel(parent)
        cls._window.title("📋 Changelog")
        cls._window.geometry("500x600")
        cls._window.configure(fg_color=STYLES["bg_primary"])
        cls._window.resizable(False, False)
        cls._window.attributes('-topmost', True)
        cls._window.protocol("WM_DELETE_WINDOW", cls._on_close)
        
        # --- HEADER ---
        header = ctk.CTkFrame(cls._window, fg_color=STYLES["accent_primary"], height=80, corner_radius=0)
        header.pack(side="top", fill="x")
        
        ctk.CTkLabel(header, text="📋 CHANGELOG", font=("Segoe UI Bold", 24), 
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        # --- FOOTER (Pack Bottom First) ---
        footer = ctk.CTkFrame(cls._window, fg_color="transparent", height=50)
        footer.pack(side="bottom", fill="x", padx=15, pady=10)
        
        ctk.CTkButton(footer, text="✖ Tutup", width=120, height=36,
                      fg_color=STYLES["btn_bg"], hover_color=STYLES["btn_hover"],
                      command=cls._on_close).pack(side="right")
        
        # --- CONTENT (Scrollable) ---
        content = ctk.CTkScrollableFrame(cls._window, fg_color="transparent")
        content.pack(side="top", fill="both", expand=True, padx=15, pady=5)
        
        # --- RENDER DATA ---
        cls._render_versions(content)
    
    @classmethod
    def _render_versions(cls, container):
        """Renders all version cards into the container."""
        for v in CHANGELOG_DATA:
            # Card
            card = ctk.CTkFrame(container, fg_color=STYLES["card_bg"], corner_radius=10,
                                border_width=1, border_color=STYLES["card_border"])
            card.pack(fill="x", pady=8)
            
            # Header Row
            header_row = ctk.CTkFrame(card, fg_color="transparent")
            header_row.pack(fill="x", padx=15, pady=(12, 5))
            
            # Badge
            ctk.CTkLabel(header_row, text=v.get("version", "v?"), font=("Segoe UI Bold", 13),
                         fg_color=v.get("color", "#00d4ff"), text_color="white",
                         corner_radius=6, height=24, width=70).pack(side="left")
            
            # Date
            ctk.CTkLabel(header_row, text=v.get("date", ""), font=("Segoe UI", 11),
                         text_color=STYLES["text_secondary"]).pack(side="right")
            
            # Updates
            for update in v.get("updates", []):
                ctk.CTkLabel(card, text=f"• {update}", font=("Segoe UI", 11),
                             text_color=STYLES["text_primary"], anchor="w").pack(fill="x", padx=15, pady=2)
            
            # Spacer
            ctk.CTkFrame(card, fg_color="transparent", height=5).pack()
    
    @classmethod
    def _on_close(cls):
        """Handles window close and resets singleton."""
        if cls._window is not None:
            cls._window.destroy()
            cls._window = None
