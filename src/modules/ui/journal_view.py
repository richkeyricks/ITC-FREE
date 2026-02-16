# src/modules/ui/journal_view.py
"""
Journal View Module - Modular UI Component
A dedicated page for System History and Technical Journal.
Replaces the limited popup with a premium integrated experience.

Follows Gravity Dev Rules:
- Modular UI
- Separation of Concerns
- Centralized Styling
"""
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS, RADIUS, SPACING
from constants.changelog_data import CHANGELOG_DATA

class JournalView:
    """
    Modular Journal Page for STC +AI.
    Features a chronologically ordered list of updates with detailed explanations.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Journal View page"""
        frame = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        # --- HEADER ---
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header, text="📝 SYSTEM JOURNAL", 
                     font=("Segoe UI Bold", 24), text_color=THEME_DARK["text_primary"]).pack(side="left")
        ctk.CTkLabel(header, text="Chronicle of Technical Advancements & Security Patches", 
                     font=("Segoe UI", 12), text_color=THEME_DARK["text_secondary"]).pack(side="left", padx=15, pady=(5, 0))

        # --- CONTENT AREA (Split Layout) ---
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True)

        # 1. Left Sidebar (Version Timeline)
        sidebar = ctk.CTkScrollableFrame(content, width=280, fg_color=THEME_DARK["bg_secondary"],
                                         border_width=1, border_color=THEME_DARK["border_default"],
                                         corner_radius=15)
        sidebar.pack(side="left", fill="y", padx=(0, 20))
        
        # 2. Right View (Detailed Content)
        detail_container = ctk.CTkFrame(content, fg_color=THEME_DARK["bg_secondary"], 
                                         corner_radius=15, border_width=1, border_color=THEME_DARK["border_default"])
        detail_container.pack(side="right", fill="both", expand=True)
        
        # State for detail view
        detail_state = {"current_v": None}

        def _show_version_detail(version_obj):
            """Updates the right panel with version details"""
            for w in detail_container.winfo_children(): w.destroy()
            detail_state["current_v"] = version_obj
            
            # Header Detail
            h = ctk.CTkFrame(detail_container, fg_color="transparent")
            h.pack(fill="x", padx=30, pady=(30, 20))
            
            # Badge & Title
            badge = ctk.CTkLabel(h, text=version_obj['version'], font=("Segoe UI Bold", 14),
                                 fg_color=version_obj.get('color', THEME_DARK["accent_primary"]),
                                 text_color="white", corner_radius=8, height=30, width=90)
            badge.pack(side="left")
            
            ctk.CTkLabel(h, text=version_obj.get('title', 'System Update'), 
                         font=("Segoe UI Bold", 22), text_color="white").pack(side="left", padx=15)
            
            ctk.CTkLabel(h, text=version_obj['date'], font=("Segoe UI", 12), 
                         text_color=THEME_DARK["text_secondary"]).pack(side="right")
            
            # Divider
            ctk.CTkFrame(detail_container, height=1, fg_color=THEME_DARK["border_default"]).pack(fill="x", padx=30)
            
            # Inner Scrollable for text
            txt_scroll = ctk.CTkScrollableFrame(detail_container, fg_color="transparent")
            txt_scroll.pack(fill="both", expand=True, padx=20, pady=10)
            
            # Description (Informatif Area)
            ctk.CTkLabel(txt_scroll, text="TECHNICAL OVERVIEW", font=("Segoe UI Bold", 12),
                         text_color=THEME_DARK["accent_primary"], anchor="w").pack(fill="x", padx=10, pady=(10, 5))
            
            desc_lbl = ctk.CTkLabel(txt_scroll, text=version_obj.get('details', 'No detailed overview provided for this version.'),
                                    font=("Segoe UI", 13), text_color=THEME_DARK["text_primary"],
                                    wraplength=550, justify="left", anchor="nw")
            desc_lbl.pack(fill="x", padx=10, pady=(0, 20))
            
            # Key Updates (Bullet Points)
            ctk.CTkLabel(txt_scroll, text="KEY IMPROVEMENTS", font=("Segoe UI Bold", 12),
                         text_color=THEME_DARK["accent_success"], anchor="w").pack(fill="x", padx=10, pady=(10, 5))
            
            for upd in version_obj.get('updates', []):
                row = ctk.CTkFrame(txt_scroll, fg_color="transparent")
                row.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(row, text="•", font=("Segoe UI Bold", 14), text_color=THEME_DARK["accent_primary"]).pack(side="left")
                ctk.CTkLabel(row, text=upd, font=("Segoe UI", 12), text_color=THEME_DARK["text_primary"],
                             wraplength=500, justify="left", anchor="w").pack(side="left", padx=10)

        # --- RENDER TIMELINE ---
        for entry in CHANGELOG_DATA:
            btn = ctk.CTkFrame(sidebar, fg_color="transparent", corner_radius=10, height=80)
            btn.pack(fill="x", pady=5, padx=5)
            btn.pack_propagate(False)
            
            # Indicator Dot
            dot = ctk.CTkLabel(btn, text="●", text_color=entry.get('color', THEME_DARK["accent_primary"]), font=("Segoe UI", 18))
            dot.place(x=15, rely=0.5, anchor="center")
            
            # Version Text
            ctk.CTkLabel(btn, text=entry['version'], font=("Segoe UI Bold", 13), 
                         text_color="white").place(x=40, y=20)
            
            # Title Snippet
            ctk.CTkLabel(btn, text=entry.get('title', 'Update'), font=("Segoe UI", 11), 
                         text_color=THEME_DARK["text_secondary"]).place(x=40, y=42)

            # Interactive binding
            def on_enter(e, b=btn): b.configure(fg_color=THEME_DARK["bg_tertiary"])
            def on_leave(e, b=btn): 
                if detail_state["current_v"] != entry: # Don't un-highlight if active
                    b.configure(fg_color="transparent")
            def on_click(e, v=entry, b=btn):
                # Reset others
                for child in sidebar.winfo_children(): 
                    if isinstance(child, ctk.CTkFrame): child.configure(fg_color="transparent")
                b.configure(fg_color=THEME_DARK["bg_tertiary"])
                _show_version_detail(v)

            for w in [btn, dot]:
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)
                w.bind("<Button-1>", on_click)
                w.configure(cursor="hand2")

        # Initial Load: Latest Version
        if CHANGELOG_DATA:
            _show_version_detail(CHANGELOG_DATA[0])
            # Highlight first button
            for child in sidebar.winfo_children():
                 if isinstance(child, ctk.CTkFrame):
                     child.configure(fg_color=THEME_DARK["bg_tertiary"])
                     break

        return frame
