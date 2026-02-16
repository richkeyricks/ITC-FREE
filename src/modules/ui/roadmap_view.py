# ══════════════════════════════════════════════════════════════════════════════
# 🗺️ ROADMAP VIEW (Presentation Layer)
# 🎯 ROLE: Community Governance Interface.
# ══════════════════════════════════════════════════════════════════════════════

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from ui_theme import THEME_DARK, FONTS
from modules.logic.roadmap_controller import RoadmapController

class RoadmapView:
    
    BG_COLOR = "#0a0a0a"
    CARD_BG = "#18181b"
    ACCENT_CYBER = "#00d2ff"
    ACCENT_GOLD = "#ffd700"
    
    @staticmethod
    def build(parent, container=None):
        target = container if container else parent.main_container
        
        # Initialize Controller
        if not hasattr(parent, 'roadmap_controller'):
            parent.roadmap_controller = RoadmapController(parent)
            
        main_frame = ctk.CTkScrollableFrame(target, fg_color=RoadmapView.BG_COLOR)
        main_frame.pack(fill="both", expand=True)

        # --- HERO SECTION ---
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(pady=(30, 20), padx=30, fill="x")
        
        ctk.CTkLabel(header, text="🗺️ ROADMAP & FEATURE REQUESTS", font=("Segoe UI Bold", 26), 
                     text_color=THEME_DARK["accent_primary"]).pack(side="top", anchor="center")
        ctk.CTkLabel(header, text="Feature Requests & Voting by Donors", font=("Segoe UI", 12),
                     text_color="gray").pack(side="top", anchor="center", pady=(5, 0))
        
        # Access & Action Bar
        action_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_bar.pack(fill="x", padx=30, pady=(10, 20))
        
        # Status Badge
        is_voter, is_architect, total = parent.roadmap_controller.get_user_tier_status()
        status_text = "ARCHITECT 🏛️" if is_architect else "ELITE VOTER 🗳️" if is_voter else "OBSERVER 👀"
        status_col = RoadmapView.ACCENT_GOLD if is_architect else RoadmapView.ACCENT_CYBER if is_voter else "gray"
        
        badge = ctk.CTkFrame(action_bar, fg_color=status_col if is_architect or is_voter else "#1a1d21", corner_radius=20)
        badge.pack(side="top", anchor="center") # Centered Badge
        ctk.CTkLabel(badge, text=f" STATUS: {status_text} ", font=("Segoe UI Bold", 11), 
                     text_color="black" if status_col != "gray" else "white").pack(padx=12, pady=4)
        
        # New Proposal (Architect Only) - BIG BUTTON
        if is_architect:
            ctk.CTkButton(action_bar, text="+ SUBMIT NEW PROPOSAL", font=("Segoe UI Bold", 12),
                          fg_color=RoadmapView.ACCENT_GOLD, text_color="black", hover_color="#d97706",
                          height=36, width=200, corner_radius=8,
                          command=lambda: RoadmapView._show_proposal_dialog(parent)).pack(side="right")

        # --- TIMELINE SECTION ---
        timeline_outer = ctk.CTkFrame(main_frame, fg_color="transparent")
        timeline_outer.pack(fill="both", expand=True, padx=30)
        
        # Add a subtle vertical 'line' to the left to simulate timeline
        v_line = ctk.CTkFrame(timeline_outer, width=2, fg_color="#27272a")
        v_line.place(relx=0.03, rely=0, relheight=1)
        
        grid = ctk.CTkFrame(timeline_outer, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=(50, 0)) # Spacing for the line
        
        # Load Items
        items = parent.roadmap_controller.fetch_items()
        
        if not items:
            # PREMIUM DEFAULT VISION CONTENT
            default_items = [
                {"id": "v1", "category": "MOBILE APP", "title": "ITC Universal Mobile App (v5.0)", "description": "Native iOS/Android companion for instant signal sync, cloud monitoring, and biometric security.", "status": "IN PROGRESS", "votes": 92, "icon": "📱"},
                {"id": "v2", "category": "AI ENGINE", "title": "Neural Engine V3 - Multi-Modal", "description": "Processing technical, fundamental, and social sentiment data simultaneously for 'God-Mode' precision.", "status": "PLANNED", "votes": 128, "icon": "🛰️"},
                {"id": "v3", "category": "INFRA", "title": "Decentralized Copytrade Network", "description": "Zero-latency blockchain synchronization across global MT5 servers. No more slippage.", "status": "PROPOSED", "votes": 45, "icon": "💎"}
            ]
            for item in default_items:
                RoadmapView._create_card(grid, parent, item)
        else:
            for item in items:
                RoadmapView._create_card(grid, parent, item)

        # Footer padding
        ctk.CTkLabel(main_frame, text="", height=40).pack()
        return main_frame

    @staticmethod
    def _create_card(container, app, item):
        card = ctk.CTkFrame(container, fg_color="#121214", corner_radius=15, border_width=1, border_color="#27272a")
        card.pack(fill="x", pady=10)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=20, pady=20, fill="both")
        
        # Left Side (Icon + Info)
        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)
        
        # Meta Row
        h_row = ctk.CTkFrame(left, fg_color="transparent")
        h_row.pack(fill="x", pady=(0, 5))
        
        cat_badge = ctk.CTkLabel(h_row, text=item.get('category', 'FEATURE'), font=("Segoe UI Bold", 9), 
                               fg_color="#00d2ff", text_color="black", corner_radius=5)
        cat_badge.pack(side="left", padx=(0, 10))
        
        status = item.get('status', 'PROPOSED')
        status_col = "#ffd700" if status in ["WHITELISTED", "IN PROGRESS"] else "gray"
        ctk.CTkLabel(h_row, text=f"● {status}", font=("Segoe UI Bold", 10), text_color=status_col).pack(side="left")

        # Title
        display_icon = item.get('icon', '🔹')
        ctk.CTkLabel(left, text=f"{display_icon}  {item.get('title', 'Untitled').upper()}", 
                     font=("Segoe UI Bold", 18), text_color="white", anchor="w").pack(fill="x")
        
        # Description
        ctk.CTkLabel(left, text=item.get('description', ''), font=("Segoe UI", 12), 
                     text_color="#a1a1aa", wraplength=550, justify="left", anchor="w").pack(fill="x", pady=(8, 15))
        
        # Vote Interaction
        vote_row = ctk.CTkFrame(left, fg_color="transparent")
        vote_row.pack(fill="x")
        
        votes = item.get('votes', 0)
        max_v = 150 # Normalized for 150
        prog = min(votes / max_v, 1.0)
        
        pg = ctk.CTkProgressBar(vote_row, height=8, corner_radius=4, progress_color="#00d2ff", width=250)
        pg.pack(side="left", padx=(0, 15))
        pg.set(prog)
        
        ctk.CTkLabel(vote_row, text=f"{votes} Votes", font=("Segoe UI Bold", 12), text_color="white").pack(side="left")
        
        # Right Side (Vote Button)
        right = ctk.CTkFrame(inner, fg_color="transparent")
        right.pack(side="right", anchor="center")
        
        has_voted = item.get('has_voted', False)
        btn_txt = "VOTED ✅" if has_voted else "VOTE"
        btn_col = "#27272a" if has_voted else "#00d2ff"
        
        def cast_vote():
            if app.roadmap_controller.vote_item(item['id']):
                app.show_page("roadmap") 

        ctk.CTkButton(right, text=btn_txt, width=100, height=36, corner_radius=18,
                      font=("Segoe UI Bold", 12),
                      fg_color=btn_col, text_color="black" if not has_voted else "white",
                      state="disabled" if has_voted else "normal",
                      command=cast_vote).pack()

    @staticmethod
    def _show_proposal_dialog(app):
        dialog = ctk.CTkToplevel(app)
        dialog.title("Submit Proposal")
        dialog.geometry("500x400")
        dialog.attributes("-topmost", True)
        
        ctk.CTkLabel(dialog, text="New Feature Proposal", font=("Segoe UI Bold", 18)).pack(pady=20)
        
        title_entry = ctk.CTkEntry(dialog, placeholder_text="Feature Title", width=400)
        title_entry.pack(pady=10)
        
        desc_entry = ctk.CTkTextbox(dialog, width=400, height=150)
        desc_entry.pack(pady=10)
        
        def submit():
            t = title_entry.get()
            d = desc_entry.get("1.0", "end").strip()
            if app.roadmap_controller.submit_proposal(t, d):
                dialog.destroy()
                app.show_page("roadmap")
                
        ctk.CTkButton(dialog, text="SUBMIT", command=submit, fg_color=RoadmapView.ACCENT_GOLD, text_color="black").pack(pady=20)
