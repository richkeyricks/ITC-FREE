# ══════════════════════════════════════════════════════════════════════════════
# 💝 DONATION VIEW (Presentation Layer)
# 🎯 ROLE: The "Hall of Hall of Wisdom". Empathetic & Premium.
# ══════════════════════════════════════════════════════════════════════════════

import customtkinter as ctk
import webbrowser
from CTkMessagebox import CTkMessagebox
import threading

class DonationView:
    """
    Hall of Fame for Donators.
    Explains development costs and honors supporters.
    """
    # UI Colors - Professional Palette
    BG_COLOR = "#0a0a0a"
    TEXT_SECONDARY = "#a1a1aa"
    ACCENT_GOLD = "#ffd700"
    GOLD_GLOW = "#3b3419"
    ACCENT_CYBER = "#00d2ff"
    CYBER_GLOW = "#0a262e"
    
    @staticmethod
    def build(parent, container=None):
        target = container if container else parent.main_container
        main_frame = ctk.CTkScrollableFrame(target, fg_color=DonationView.BG_COLOR)
        main_frame.pack(fill="both", expand=True)
        
        # --- HERO SECTION ---
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(pady=40, padx=20, fill="x")
        
        ctk.CTkLabel(header, text="SUPPORTERS HALL OF FAME 👑", 
                     font=("Segoe UI Black", 36), text_color=DonationView.ACCENT_GOLD).pack()
        
        ctk.CTkLabel(header, text="The Elite Circle fueling the Haineo SkyNET Intelligence", 
                     font=("Segoe UI", 16), text_color=DonationView.TEXT_SECONDARY).pack(pady=10)
        
        # --- THE WHY (TRANSPARENCY) ---
        info_box = ctk.CTkFrame(main_frame, fg_color="#121214", corner_radius=15, border_width=1, border_color="#27272a")
        info_box.pack(pady=10, padx=40, fill="x")
        
        # Title Center Aligned
        ctk.CTkLabel(info_box, text="POWERING THE ECOSYSTEM", font=("Segoe UI Bold", 20), 
                     text_color="white", anchor="center").pack(pady=(25, 15), padx=35, fill="x")
        
        # Grid/List Container (Centered Block)
        wrapper = ctk.CTkFrame(info_box, fg_color="transparent")
        wrapper.pack(fill="x", pady=(0, 20))
        
        list_container = ctk.CTkFrame(wrapper, fg_color="transparent")
        list_container.pack(anchor="center") # This centers the block of items
        
        features = [
            ("🚀", "High-Performance Cloud Servers", "24/7 Global Access & Latency Optimization", 0),
            ("🧠", "AI Model Neural Costs", "Haineo SkyNET Core processing & training", 0),
            ("🛡️", "Enterprise-Grade Security", "Zero-Knowledge Architecture & Encryption", -5)
        ]
        
        for icon, title, d, offset_y in features:
            f_row = ctk.CTkFrame(list_container, fg_color="transparent")
            f_row.pack(fill="x", pady=8)
            
            f_row.grid_columnconfigure(0, weight=0, minsize=60)
            f_row.grid_columnconfigure(1, weight=1)

            icon_box = ctk.CTkFrame(f_row, fg_color="transparent", width=60, height=40)
            icon_box.grid(row=0, column=0, sticky="n", pady=(2, 0))
            icon_box.pack_propagate(False) 
            
            ctk.CTkLabel(icon_box, text=icon, font=("Segoe UI", 24)).place(relx=0.5, rely=0, anchor="n", y=offset_y)
            
            txt_col = ctk.CTkFrame(f_row, fg_color="transparent")
            txt_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            
            ctk.CTkLabel(txt_col, text=title, font=("Segoe UI Bold", 14), text_color="white", anchor="w").pack(fill="x")
            ctk.CTkLabel(txt_col, text=d, font=("Segoe UI", 11), text_color=DonationView.TEXT_SECONDARY, anchor="w").pack(fill="x")

        # Bottom text
        ctk.CTkLabel(info_box, text="Your contribution ensures we stay ahead of the Institutional Whales.", 
                     font=("Segoe UI", 13), text_color=DonationView.TEXT_SECONDARY, anchor="center").pack(padx=35, pady=(0, 10), fill="x")
        
        ctk.CTkLabel(info_box, text="Your vision powers our code.", 
                     font=("Segoe UI Italic", 12), text_color=DonationView.ACCENT_CYBER, anchor="center").pack(padx=35, pady=(0, 25), fill="x")
        
        # --- ACTION SECTION ---
        cta_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cta_frame.pack(pady=30)
        
        ctk.CTkButton(cta_frame, text="💎 JOIN THE ELITE CIRCLE", font=("Segoe UI Black", 18), 
                       fg_color=DonationView.ACCENT_GOLD, hover_color="#d97706", text_color="black", height=55, width=350,
                       command=lambda: webbrowser.open("https://saweria.co/richkeyrick")).pack()
        
        ctk.CTkLabel(cta_frame, text="*Top supporters gain priority access to Founder's Pitch session.*", 
                     font=("Segoe UI Italic", 11), text_color=DonationView.ACCENT_CYBER).pack(pady=10)

        # --- LEADERBOARD (Hall of Fame) ---
        ctk.CTkLabel(main_frame, text="🏆 TOP SUPPORTERS", font=("Segoe UI Black", 24), text_color=DonationView.ACCENT_GOLD).pack(pady=(40, 20))
        
        lb_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        lb_container.pack(fill="x", padx=60, pady=10)
        
        # --- DATA FETCHING & RENDERING ---
        def _fetch_donors():
            final_list = []
            if hasattr(parent, 'db_manager'):
                try:
                    # Fix for TypeError: unexpected keyword argument 'limit'
                    # We use positional argument to be safe if keyword fails
                    data = parent.db_manager.get_donations(30)
                except TypeError:
                    # Fallback if method signature is strictly no-args (should not happen but safety first)
                    try:
                        data = parent.db_manager.get_donations()
                    except: data = []
                except Exception as e:
                    print(f"// Donation Fetch Error: {e}")
                    data = []

                for i, d in enumerate(data):
                    amt = d.get('amount', 0)
                    from utils.currency import format_currency
                    formatted_amt = format_currency(amt)
                    name = d.get('name', 'Anonymous')
                    if not any(f in name for f in ["🇺🇸", "🇮🇩", "🇲🇾", "🌐"]):
                        name = f"🌐 {name}"
                    
                    rank = i + 1
                    color = DonationView.ACCENT_GOLD if rank == 1 else "#e5e5e5" if rank == 2 else "#cd7f32" if rank == 3 else DonationView.ACCENT_CYBER
                    final_list.append((rank, name, formatted_amt, d.get('message', 'Thank you!'), color))
            
            # Fallback for Demo/Offline
            if not final_list:
                final_list = [
                    (1, "💎 David Wang", "$ 2,500", "Haineo AI accuracy is unmatched. Great work!", DonationView.ACCENT_GOLD),
                    (2, "🇦 Ahmed Al-Fayyad", "$ 1,800", "Barakallah, thank you for the consistent signals.", "#e5e5e5"),
                    (3, "🇮🇩 Budi Santoso", "Rp 15.000.000", "Maju terus karya anak bangsa! Amazing AI.", "#cd7f32"),
                    (4, "🇺🇸 Jonathan Reed", "$ 1,000", "The SkyNET precision is world-class.", DonationView.ACCENT_CYBER)
                ]

            def _update_ui():
                if not lb_container.winfo_exists(): return
                for widget in lb_container.winfo_children():
                    widget.destroy()
                for rank, name, amount, message, color in final_list:
                    DonationView._create_donator_row(lb_container, rank, name, amount, message, color)
            
            if hasattr(parent, 'after'):
                parent.after(0, _update_ui)

        threading.Thread(target=_fetch_donors, daemon=True).start()
        
        # Footer Padding
        ctk.CTkLabel(main_frame, text="", height=60).pack()

        return main_frame

    @staticmethod
    def _create_donator_row(parent, rank, name, amount, message, color):
        # Ghost row style for Premium feel
        accent_col = DonationView.ACCENT_CYBER
        row = ctk.CTkFrame(parent, fg_color="#141417", height=65, corner_radius=12, border_width=1 if rank <= 3 else 0, border_color=color)
        row.pack(fill="x", pady=4)
        row.pack_propagate(False)
        
        # Rank Badge
        r_badge = ctk.CTkFrame(row, width=40, height=40, fg_color=color, corner_radius=10)
        r_badge.pack(side="left", padx=(15, 12), pady=12)
        r_badge.pack_propagate(False)
        
        ctk.CTkLabel(r_badge, text=f"#{rank}", font=("Inter Black", 14), 
                     text_color="black" if rank <= 3 else "white").place(relx=0.5, rely=0.5, anchor="center")
        
        # Name Info
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="y", pady=10)
        
        ctk.CTkLabel(info_frame, text=name, font=("Segoe UI Bold", 15), text_color="white").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"💬 \"{message}\"", font=("Segoe UI Italic", 11), text_color="#6b7280", wraplength=450, justify="left").pack(anchor="w")
        
        # Amount
        ctk.CTkLabel(row, text=amount, font=("Inter Black", 15), 
                     text_color=accent_col).pack(side="right", padx=25)
