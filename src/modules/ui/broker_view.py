import webbrowser
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS

class BrokerView:
    """
    Standalone View for Official Brokers.
    Extracted from LeaderboardView for dedicated Sidebar access.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Brokers interface."""
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK
        
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        # --- HEADER ---
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(header, text="🏦 OFFICIAL BROKERS", font=("Segoe UI Bold", 26), 
                     text_color=theme["accent_primary"]).pack(side="top", anchor="center")
        ctk.CTkLabel(header, text="Official & Regulated Partners", font=("Segoe UI", 12),
                     text_color=theme["text_secondary"]).pack(side="top", anchor="center")

        # --- SCROLLABLE LIST ---
        content_area = ctk.CTkScrollableFrame(page, fg_color="transparent")
        content_area.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Fetch Data
        items = parent.translator.get_brokers()
        
        # Logic: Dedupe
        unique_items = []
        seen = set()
        for x in items:
            if x['name'] not in seen:
                unique_items.append(x)
                seen.add(x['name'])


        # Render Cards (Gold Theme)
        for item in unique_items:
            card = ctk.CTkFrame(content_area, fg_color=theme["bg_secondary"], corner_radius=10, 
                              border_width=1, border_color=theme["border_default"])
            card.pack(fill="x", pady=6)
            
            # Hover Effect
            def on_enter(e, f=card, c=theme["bg_tertiary"]): f.configure(fg_color=c)
            def on_leave(e, f=card, c=theme["bg_secondary"]): f.configure(fg_color=c)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            
            h_frame = ctk.CTkFrame(card, fg_color="transparent")
            h_frame.pack(fill="x", padx=15, pady=12)
            
            is_vip = item.get("is_affiliate") or "HSB" in item['name']
            icon = "🔥" if is_vip else "🏦"
            nm_col = "#f59e0b" if is_vip else theme["text_primary"]
            
            # Title
            title_lbl = ctk.CTkLabel(h_frame, text=f"{icon}  {item['name']}", 
                                   font=("Segoe UI Bold", 16), text_color=nm_col)
            title_lbl.pack(side="left")
            
            # Desc
            desc = ctk.CTkLabel(card, text=item.get('desc') or item.get('reason'), font=("Segoe UI", 12), 
                              text_color=theme["text_secondary"], bg_color="transparent", justify="left", anchor="w")
            desc.pack(fill="x", padx=15, pady=(0, 10))
            
            # CTA Button
            btn_txt = "OPEN ACCOUNT 🚀" if is_vip else "VISIT BROKER"
            btn_col = "#f59e0b" if is_vip else theme["bg_tertiary"]
            text_col = "black" if is_vip else theme["text_primary"]
            
            ctk.CTkButton(card, text=btn_txt, fg_color=btn_col, hover_color="#d97706" if is_vip else theme["border_active"],
                          text_color=text_col, height=36, font=("Segoe UI Bold", 12),
                          command=lambda u=item['url']: webbrowser.open_new_tab(u)).pack(fill="x", padx=15, pady=(0, 15))

        return page
