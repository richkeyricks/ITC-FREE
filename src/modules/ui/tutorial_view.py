import customtkinter as ctk
import webbrowser
import re
from ui_theme import THEME_DARK, FONTS

class TutorialView:
    """
    Premium Visual Tutorial with Color-Coded Content Hierarchy.
    Follows Gravity Dev Rules: Modular UI with Enhanced UX.
    """
    
    # Color Palette for Content Types - REFACTORED FOR FLAT PROFESSIONAL LOOK
    COLORS = {
        "header": "#ffffff",        # White (Clean Professional)
        "subheader": "#4a90e2",     # Professional Blue
        "success": "#333333",       # Flat Dark Gray (Professional)
        "warning": "#333333",       # Flat Dark Gray
        "info": "#333333",          # Flat Dark Gray
        "emphasis": "#333333",      # Flat Dark Gray
        "normal": "#bdc3c7",        # Readable Gray
        "muted": "#7f8c8d"          # Muted Text
    }
    
    @staticmethod
    def parse_and_render(parent_frame, content, translator):
        """
        Parses tutorial markdown-like content and renders with color coding.
        Recognizes patterns:
        - ━━━ lines = headers
        - [ANALOGY], [TIPS], [WARNING], [PROBLEM], [SOLUTION] = colored boxes
        - Numbered/bulleted lists = auto-formatted
        - Emoji headers = section dividers
        """
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            # 1. DIVIDER LINES (━━━)
            if line.startswith('━'):
                divider = ctk.CTkFrame(parent_frame, height=2, fg_color=TutorialView.COLORS["muted"])
                divider.pack(fill="x", pady=5)
                continue
            
            # 2. SECTION HEADERS (Emoji + CAPS)
            if re.match(r'^[🔥📋📈⚙️🗺️🛡️🧠💎🚀📥🔐📨🔎🤖🛰️]\s+[A-Z\s\(\)&-]+$', line):
                lbl = ctk.CTkLabel(parent_frame, text=line, font=("Segoe UI Bold", 16),
                                   text_color=TutorialView.COLORS["header"], anchor="w")
                lbl.pack(fill="x", pady=(15, 5), padx=10)
                continue
            
            # 3. SPECIAL BOXES ([TAG])
            if line.startswith('['):
                tag_match = re.match(r'^\[([A-Z\s]+)\](.*)$', line)
                if tag_match:
                    tag = tag_match.group(1).strip()
                    rest = tag_match.group(2).strip()
                    
                    # Choose color based on tag type
                    if tag in ["TIPS", "TIP", "RECOMMENDED", "REKOMENDASI", "SARAN"]:
                        color = TutorialView.COLORS["success"]
                        icon = "✅"
                    elif tag in ["WARNING", "PERINGATAN", "CAUTION"]:
                        color = TutorialView.COLORS["warning"]
                        icon = "⚠️"
                    elif tag in ["PROBLEM", "MASALAH"]:
                        color = TutorialView.COLORS["warning"]
                        icon = "❌"
                    elif tag in ["SOLUTION", "SOLUSI"]:
                        color = TutorialView.COLORS["success"]
                        icon = "💡"
                    elif tag in ["ANALOGI", "ANALOGY"]:
                        color = TutorialView.COLORS["info"]
                        icon = "🧩"
                    elif tag in ["KONSEP DASAR", "BASIC CONCEPT", "NEW"]:
                        color = TutorialView.COLORS["emphasis"]
                        icon = "🌟"
                    else:
                        color = TutorialView.COLORS["info"]
                        icon = "ℹ️"
                    
                    # Create colored box (FLAT PROFESSIONAL STYLE)
                    # Border is now a subtle dark gray, not colored.
                    box = ctk.CTkFrame(parent_frame, fg_color="#1a1a1a", border_width=1, border_color="#333333", corner_radius=8)
                    box.pack(fill="x", pady=8, padx=10)
                    
                    # Title is now White/Standardized (Flat)
                    tag_label = ctk.CTkLabel(box, text=f"{icon} {tag}", font=("Segoe UI Bold", 12),
                                            text_color="#E0E0E0", anchor="w")
                    tag_label.pack(fill="x", padx=10, pady=(8, 4))
                    
                    if rest:
                        content_label = ctk.CTkLabel(box, text=rest, font=("Segoe UI", 11),
                                                    text_color=TutorialView.COLORS["normal"], anchor="w", wraplength=720, justify="left")
                        content_label.pack(fill="x", padx=10, pady=(0, 8))
                    continue
            
            # 4. NUMBERED LISTS (1. 2. 3.)
            if re.match(r'^\d+\.\s', line):
                lbl = ctk.CTkLabel(parent_frame, text=line, font=("Segoe UI", 11),
                                   text_color=TutorialView.COLORS["normal"], anchor="w", wraplength=720, justify="left")
                lbl.pack(fill="x", pady=2, padx=20)
                continue
            
            # 5. BULLET POINTS (• or -)
            if line.startswith('•') or line.startswith('-'):
                lbl = ctk.CTkLabel(parent_frame, text=line, font=("Segoe UI", 11),
                                   text_color=TutorialView.COLORS["normal"], anchor="w", wraplength=720, justify="left")
                lbl.pack(fill="x", pady=2, padx=30)
                continue
            
            # 6. SUB-INDENTED TEXT (starts with spaces)
            if line.startswith('   '):
                lbl = ctk.CTkLabel(parent_frame, text=line, font=("Segoe UI", 10),
                                   text_color=TutorialView.COLORS["muted"], anchor="w", wraplength=700, justify="left")
                lbl.pack(fill="x", pady=1, padx=40)
                continue
            
            # 7. NORMAL PARAGRAPHS
            lbl = ctk.CTkLabel(parent_frame, text=line, font=("Segoe UI", 11),
                               text_color=TutorialView.COLORS["normal"], anchor="w", wraplength=740, justify="left")
            lbl.pack(fill="x", pady=3, padx=15)
    
    @staticmethod
    def show(parent):
        """Creates and shows the Premium Tutorial TopLevel window"""
        theme = THEME_DARK
        
        tutorial_window = ctk.CTkToplevel(parent)
        tutorial_window.title(parent.translator.get("tut_title"))
        tutorial_window.geometry("850x950")
        tutorial_window.attributes('-topmost', True)
        
        # Premium Header with Gradient Simulation
        header = ctk.CTkFrame(tutorial_window, fg_color="#0a0a0a", height=80)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        title_label = ctk.CTkLabel(header, text=parent.translator.get("tut_header"), 
                     font=("Segoe UI Bold", 24), text_color=TutorialView.COLORS["header"])
        title_label.pack(pady=(15, 3))
        
        subtitle_label = ctk.CTkLabel(header, text=parent.translator.get("tut_sub"), 
                     font=("Segoe UI", 12), text_color=TutorialView.COLORS["success"])
        subtitle_label.pack(pady=(0, 10))
        
        # Premium Tabview
        tabview = ctk.CTkTabview(tutorial_window, fg_color=theme["bg_secondary"], 
                                 segmented_button_selected_color=TutorialView.COLORS["subheader"], # Blue for readability
                                 segmented_button_selected_hover_color="#357abd",
                                 segmented_button_fg_color="#2a2a2a")
        tabview.pack(fill="both", expand=True, padx=15, pady=10)
        
        tab_setup = tabview.add(parent.translator.get("tut_tab_setup"))
        tab_features = tabview.add(parent.translator.get("tut_tab_features"))
        
        # Tab 1: Setup Guide (Color-Coded ScrollableFrame)
        scroll_setup = ctk.CTkScrollableFrame(tab_setup, fg_color="transparent")
        scroll_setup.pack(fill="both", expand=True, padx=5, pady=5)
        TutorialView.parse_and_render(scroll_setup, parent.translator.get("tut_content"), parent.translator)

        # Tab 2: Feature Mastery (Color-Coded ScrollableFrame)
        scroll_feat = ctk.CTkScrollableFrame(tab_features, fg_color="transparent")
        scroll_feat.pack(fill="both", expand=True, padx=5, pady=5)
        TutorialView.parse_and_render(scroll_feat, parent.translator.get("tut_features"), parent.translator)
        
        # Premium Footer
        footer = ctk.CTkFrame(tutorial_window, fg_color="#0a0a0a", height=60)
        footer.pack(fill="x", padx=0, pady=0)
        footer.pack_propagate(False)
        
        btn_container = ctk.CTkFrame(footer, fg_color="transparent")
        btn_container.pack(expand=True)
        
        ctk.CTkButton(btn_container, text=parent.translator.get("tut_btn_donasi"), 
                      fg_color=TutorialView.COLORS["warning"], hover_color="#cc5525",
                      text_color="black", font=("Segoe UI Bold", 12), width=180, height=35,
                      command=lambda: webbrowser.open("https://saweria.co/richkeyrick")).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_container, text=parent.translator.get("tut_btn_close"), 
                      fg_color="#404040", hover_color="#505050", width=120, height=35,
                      font=("Segoe UI Bold", 12),
                      command=tutorial_window.destroy).pack(side="left", padx=5)
