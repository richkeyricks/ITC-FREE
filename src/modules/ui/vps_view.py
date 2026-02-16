import webbrowser
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS

class VPSView:
    """
    Standalone View for VPS Servers.
    Extracted from LeaderboardView for dedicated Sidebar access.
    """
    
    @staticmethod
    def build(parent):
        """Builds the VPS interface."""
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        # --- HEADER ---
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(header, text="☁️ VPS SERVER OPTIONS", font=("Segoe UI Bold", 26), 
                     text_color=theme["accent_info"]).pack(side="top", anchor="center")
        ctk.CTkLabel(header, text="High Stability & Low Latency for 24/7 Trading", font=("Segoe UI", 12),
                     text_color=theme["text_secondary"]).pack(side="top", anchor="center")

        # --- SCROLLABLE LIST ---
        content_area = ctk.CTkScrollableFrame(page, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Fetch Data
        items = parent.translator.get_vps()
        print(f"// DEBUG: VPS Items Count: {len(items)}") # Debugging Blank Page
        
        # Render Cards (Blue Theme)
        # Render Cards (Blue Theme)
        if not items:
            ctk.CTkLabel(content_area, text="No VPS Providers Available", font=("Segoe UI", 12), 
                         text_color=theme["text_secondary"]).pack(pady=40)
        
        for item in items:
            try:
                # --- DYNAMIC BADGING LOGIC ---
                is_rec = item.get("recommended", False)
                target_color = item.get("color", "blue")
                
                # Map simple color names to hex
                color_map = {
                    "yellow": "#f59e0b", # Hostinger Gold
                    "blue": "#3498db",   # Standard VPS Blue
                    "green": "#10b981"
                }
                accent_col = color_map.get(target_color, "#3498db")
                
                # Icon
                icon_char = item.get('icon', '☁️')
                
                # Card Container
                # If recommended, add a subtle border glow
                border_col = accent_col if is_rec else theme["border_default"]
                border_width = 2 if is_rec else 1
                
                card = ctk.CTkFrame(content_area, fg_color=theme["bg_secondary"], corner_radius=12, 
                                  border_width=border_width, border_color=border_col)
                card.pack(fill="x", pady=8) # Increased spacing
                
                h_frame = ctk.CTkFrame(card, fg_color="transparent")
                h_frame.pack(fill="x", padx=15, pady=(12, 5))
                
                # Title with Icon
                title_lbl = ctk.CTkLabel(h_frame, text=f"{icon_char}  {item['name']}", 
                                       font=("Segoe UI Bold", 16), text_color=accent_col)
                title_lbl.pack(side="left")
                
                # BADGE (If Recommended)
                if is_rec:
                    badge = ctk.CTkLabel(h_frame, text="RECOMMENDED", font=("Segoe UI Bold", 10),
                                       text_color="#000000", fg_color=accent_col, corner_radius=6)
                    badge.pack(side="right", padx=5)
    
                # Desc
                desc_text = item.get('desc') or item.get('reason')
                desc = ctk.CTkLabel(card, text=desc_text, font=("Segoe UI", 12), 
                                  text_color=theme["text_secondary"], bg_color="transparent", justify="left", anchor="w")
                desc.pack(fill="x", padx=20, pady=(0, 12))
                
                # CTA Button
                btn_txt = "🔥 GET PROMO ⚡" if is_rec else "VISIT PROVIDER"
                btn_col = accent_col if is_rec else "#3498db"
                btn_hover = "#d97706" if is_rec else "#2980b9"
                
                ctk.CTkButton(card, text=btn_txt, fg_color=btn_col, hover_color=btn_hover,
                              text_color="black" if is_rec else "white", height=36, font=("Segoe UI Bold", 12),
                              command=lambda u=item['url']: webbrowser.open_new_tab(u)).pack(fill="x", padx=15, pady=(0, 15))
            except Exception as e:
                print(f"// VPS Item Render Error: {e}")

        return page
