import os
import threading
from datetime import datetime
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS
from utils.tooltips import CTkToolTip
from CTkMessagebox import CTkMessagebox

# --- THEME ---
# REMOVED STATIC THEME

class AdminView:
    """
    Modular class for the Admin Panel page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Admin page and attaches it to the parent (App/GUI)."""
        # Dynamic Theme Injection
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK

        page = ctk.CTkScrollableFrame(parent.main_container, fg_color="transparent")
        
        ctk.CTkLabel(page, text="👑 ADMIN MISSION CONTROL", font=("Segoe UI Bold", 24), 
                     text_color=theme["accent_primary"], anchor="w").pack(fill="x", pady=(0, 20))
        
        # --- STATS ROW ---
        stats_row = ctk.CTkFrame(page, fg_color="transparent")
        stats_row.pack(fill="x", pady=(0, 20))
        
        # User Count Card
        card1 = ctk.CTkFrame(stats_row, fg_color=theme["bg_secondary"], corner_radius=12)
        card1.pack(side="left", expand=True, fill="both", padx=(0, 10))
        ctk.CTkLabel(card1, text="TOTAL USERS", font=FONTS["body_small"], text_color=theme["text_secondary"]).pack(pady=(15, 0))
        parent.admin_user_count = ctk.CTkLabel(card1, text="0", font=("Segoe UI Bold", 28))
        parent.admin_user_count.pack(pady=(0, 15))
        
        # Trade Count Card
        card2 = ctk.CTkFrame(stats_row, fg_color=theme["bg_secondary"], corner_radius=12)
        card2.pack(side="left", expand=True, fill="both", padx=(0, 10))
        ctk.CTkLabel(card2, text="📈 ECOSYSTEM TRADES", font=FONTS["body_small"], text_color=theme["text_secondary"]).pack(pady=(15, 0))
        parent.admin_trade_count = ctk.CTkLabel(card2, text="0", font=("Segoe UI Bold", 28))
        parent.admin_trade_count.pack(pady=(0, 15))
        
        # Global P/L Card
        card3 = ctk.CTkFrame(stats_row, fg_color=theme["bg_secondary"], corner_radius=12)
        card3.pack(side="left", expand=True, fill="both")
        ctk.CTkLabel(card3, text="💰 ECOSYSTEM P/L", font=FONTS["body_small"], text_color=theme["text_secondary"]).pack(pady=(15, 0))
        parent.admin_global_pl = ctk.CTkLabel(card3, text="$0", font=("Segoe UI Bold", 28), text_color=theme["accent_success"])
        parent.admin_global_pl.pack(pady=(0, 15))
        
        # --- USER LIST ---
        ctk.CTkLabel(page, text="👥 ACTIVE USERS", font=("Segoe UI Bold", 20), 
                     text_color=theme["text_primary"], anchor="w").pack(fill="x", pady=(20, 10))
        
        parent.admin_user_list = ctk.CTkTextbox(page, height=300, font=FONTS["mono"], wrap="none",
                                                fg_color=theme["bg_secondary"], text_color=theme["text_primary"])
        parent.admin_user_list.pack(fill="x", expand=True, pady=(0, 20))
        
        # Double-Click to Inspect
        def _on_double_click(event):
            try:
                line = parent.admin_user_list.get("insert linestart", "insert lineend")
                if "|" in line:
                    hwid = line.split("|")[0].strip()
                    if hwid and hwid != "HWID":
                        from modules.ui.inspector_panel import UserInspectorPanel
                        UserInspectorPanel(parent, parent.db_manager, hwid)
            except: pass
        
        # Single-Click to Auto-Fill HWID
        def _on_click(event):
            try:
                # Use 'insert' because clicking moves the cursor there
                line = parent.admin_user_list.get("insert linestart", "insert lineend")
                if "|" in line:
                    hwid = line.split("|")[0].strip()
                    if hwid and hwid != "HWID":
                        if hasattr(parent, 'admin_target_hwid'):
                            parent.admin_target_hwid.delete(0, "end")
                            parent.admin_target_hwid.insert(0, hwid)
            except: pass

        parent.admin_user_list.bind("<Double-Button-1>", _on_double_click)
        parent.admin_user_list.bind("<ButtonRelease-1>", _on_click)
        
        # --- COMMAND CENTER ---
        ctk.CTkLabel(page, text="🛠️ AI PERMISSION COMMAND CENTER", font=("Segoe UI Bold", 20), 
                     text_color=theme["text_primary"], anchor="w").pack(fill="x", pady=(20, 10))
        
        actions_frame = ctk.CTkFrame(page, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 20))
        
        # Quick User Management
        manage_frame = ctk.CTkFrame(actions_frame, fg_color=theme["bg_secondary"], corner_radius=12)
        manage_frame.pack(side="left", expand=True, fill="both", padx=(0, 10))
        ctk.CTkLabel(manage_frame, text="USER MANAGEMENT", font=FONTS["body_small"], text_color=theme["text_secondary"]).pack(pady=(15, 0))
        
        parent.admin_target_hwid = ctk.CTkEntry(manage_frame, placeholder_text="Enter User HWID...")
        parent.admin_target_hwid.pack(fill="x", padx=15, pady=(0, 10))
        
        btn_row_manage = ctk.CTkFrame(manage_frame, fg_color="transparent")
        btn_row_manage.pack(pady=(0, 15))
        
        def _handle_upgrade():
            hwid = parent.admin_target_hwid.get().strip()
            if not hwid: return
            if parent.db_manager.set_user_pro_status(hwid, True):
                CTkMessagebox(title="Success", message=f"User {hwid} upgraded to PRO!", icon="check")
                AdminView.refresh_admin_stats(parent)
            else:
                CTkMessagebox(title="Error", message="Failed to update user status.", icon="cancel")

        def _handle_ban(state):
            hwid = parent.admin_target_hwid.get().strip()
            if not hwid: return
            action = "REVOKE LICENSE" if state else "RESTORE ACCESS"
            if CTkMessagebox(title="Confirm Action", message=f"Are you sure you want to {action} for user {hwid}?", 
                             icon="warning", option_1="Yes", option_2="No").get() == "Yes":
                success, msg = parent.db_manager.update_ban_status(hwid, state)
                if success:
                    CTkMessagebox(title="Success", message=msg, icon="check")
                    AdminView.refresh_admin_stats(parent)
                else:
                    CTkMessagebox(title="Error", message=msg, icon="cancel")

        def _handle_dm():
            hwid = parent.admin_target_hwid.get().strip()
            if not hwid: return
            dialog = ctk.CTkInputDialog(text=f"Send Message to {hwid}:", title="Admin Direct Message")
            msg = dialog.get_input()
            if msg:
                if parent.db_manager.send_dm(hwid, msg):
                    CTkMessagebox(title="Sent", message="Message delivered!", icon="check")
                else:
                    CTkMessagebox(title="Error", message="Failed to send DM.", icon="cancel")

        def _handle_inspect():
            hwid = parent.admin_target_hwid.get().strip()
            if not hwid: return
            from modules.ui.inspector_panel import UserInspectorPanel
            UserInspectorPanel(parent, parent.db_manager, hwid)

        # --- FORGE CONTROLS ---
        ctk.CTkLabel(manage_frame, text="TIER FORGE", font=FONTS["body_small"], text_color=theme["accent_primary"]).pack(pady=(5, 0))
        tier_row = ctk.CTkFrame(manage_frame, fg_color="transparent")
        tier_row.pack(fill="x", padx=15, pady=(0, 10))
        
        parent.admin_tier_var = ctk.StringVar(value="GOLD")
        ctk.CTkOptionMenu(tier_row, values=["STANDARD", "GOLD", "PLATINUM", "INSTITUTIONAL"], 
                          variable=parent.admin_tier_var, height=32).pack(side="left", expand=True, padx=(0, 5))
        
        def _apply_tier():
            hwid = parent.admin_target_hwid.get().strip()
            tier = parent.admin_tier_var.get()
            if not hwid: return
            if parent.db_manager.set_user_tier(hwid, tier):
                CTkMessagebox(title="Success", message=f"User tier updated to {tier}!", icon="check")
                AdminView.refresh_admin_stats(parent)
            else:
                CTkMessagebox(title="Error", message="Failed to update tier.", icon="cancel")
                
        ctk.CTkButton(tier_row, text="APPLY", width=60, height=32, command=_apply_tier).pack(side="left")

        ctk.CTkLabel(manage_frame, text="SUBSCRIPTION FORGE", font=FONTS["body_small"], text_color=theme["accent_primary"]).pack(pady=(5, 0))
        forge_row = ctk.CTkFrame(manage_frame, fg_color="transparent")
        forge_row.pack(fill="x", padx=15, pady=(0, 15))
        
        parent.admin_forge_var = ctk.StringVar(value="MONTHLY")
        ctk.CTkOptionMenu(forge_row, values=["MONTHLY", "YEARLY", "LIFETIME"], 
                          variable=parent.admin_forge_var, height=32).pack(side="left", expand=True, padx=(0, 5))
        
        def _apply_forge():
            hwid = parent.admin_target_hwid.get().strip()
            mode = parent.admin_forge_var.get()
            if not hwid: return
            if parent.db_manager.set_user_subscription(hwid, mode):
                CTkMessagebox(title="Success", message=f"User duration forged to {mode}!", icon="check")
                AdminView.refresh_admin_stats(parent)
            else:
                CTkMessagebox(title="Error", message="Forge failed.", icon="cancel")

        ctk.CTkButton(forge_row, text="FORGE", width=60, height=32, command=_apply_forge, fg_color="#8b5cf6").pack(side="left")

        # Button Row 1: PRO & License
        btn_row_1 = ctk.CTkFrame(manage_frame, fg_color="transparent")
        btn_row_1.pack(pady=(0, 5))
        
        ctk.CTkButton(btn_row_1, text="UPGRADE PRO", fg_color=theme["accent_success"], width=110, height=36,
                      command=_handle_upgrade).pack(side="left", padx=3)
        ctk.CTkButton(btn_row_1, text="REVOKE PRO", fg_color="transparent", border_width=1, 
                      border_color="#f85149", text_color="#f85149", width=110, height=36,
                      command=lambda: [parent.db_manager.set_user_pro_status(parent.admin_target_hwid.get().strip(), False), AdminView.refresh_admin_stats(parent)]).pack(side="left", padx=3)
        
        # Button Row 2: Ban & Access
        btn_row_2 = ctk.CTkFrame(manage_frame, fg_color="transparent")
        btn_row_2.pack(pady=(0, 5))
        
        ctk.CTkButton(btn_row_2, text="REVOKE LICENSE", fg_color="#dc3545", hover_color="#bb2d3b", width=110, height=36,
                      command=lambda: _handle_ban(True)).pack(side="left", padx=3)
        ctk.CTkButton(btn_row_2, text="RESTORE ACCESS", fg_color="#2ea44f", hover_color="#238636", width=110, height=36,
                      command=lambda: _handle_ban(False)).pack(side="left", padx=3)

        # Button Row 3: Inspect & DM
        btn_row_3 = ctk.CTkFrame(manage_frame, fg_color="transparent")
        btn_row_3.pack(pady=(0, 15))
        
        ctk.CTkButton(btn_row_3, text="🔍 INSPECT", fg_color="#8b5cf6", hover_color="#7c3aed", width=110, height=36,
                      command=_handle_inspect).pack(side="left", padx=3)
        ctk.CTkButton(btn_row_3, text="💬 SEND DM", fg_color="#0d6efd", hover_color="#0b5ed7", width=110, height=36,
                      command=_handle_dm).pack(side="left", padx=3)
        
        # Inbox Section (Phase 59)
        msg_outer = ctk.CTkFrame(actions_frame, fg_color="transparent")
        msg_outer.pack(side="left", expand=True, fill="both", padx=(0, 10))
        
        msg_frame = ctk.CTkFrame(msg_outer, fg_color=theme["bg_secondary"], corner_radius=12)
        msg_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(msg_frame, text="BROADCAST MESSAGE", font=FONTS["body_small"], text_color=theme["text_secondary"]).pack(pady=(10, 0))
        parent.admin_msg_input = ctk.CTkEntry(msg_frame, placeholder_text="Enter message to broadcast...")
        parent.admin_msg_input.pack(fill="x", padx=15, pady=(5, 10))
        ctk.CTkButton(msg_frame, text="SEND GLOBAL", command=lambda: AdminView.send_global_msg(parent)).pack(pady=(0, 10))
        
        # Inbox
        inbox_frame = ctk.CTkFrame(msg_outer, fg_color=theme["bg_secondary"], corner_radius=12)
        inbox_frame.pack(fill="x")
        ctk.CTkLabel(inbox_frame, text="📥 INBOX (USER REPLIES)", font=FONTS["body_small"], text_color=theme["text_secondary"]).pack(pady=(10, 0))
        parent.admin_inbox = ctk.CTkTextbox(inbox_frame, height=80, font=("Consolas", 11), fg_color=theme["bg_tertiary"])
        parent.admin_inbox.pack(fill="x", padx=15, pady=5)
        
        def _refresh_inbox():
            replies = parent.db_manager.get_unread_replies()
            text = ""
            for r in replies:
                sender = r.get('sender_id', 'Unknown')
                content = r.get('content', '')
                time = r.get('created_at', '')[:16].replace('T', ' ')
                text += f"[{time}] FROM {sender}:\n{content}\n" + "-"*30 + "\n"
            parent.admin_inbox.delete("0.0", "end")
            parent.admin_inbox.insert("0.0", text if text else "No new replies.")
            
        ctk.CTkButton(inbox_frame, text="REFRESH INBOX", command=_refresh_inbox, height=28).pack(pady=(0, 10))
        parent.safe_ui_update(_refresh_inbox)


        # Refresh Stats Button
        refresh_frame = ctk.CTkFrame(actions_frame, fg_color=theme["bg_secondary"], corner_radius=12)
        refresh_frame.pack(side="left", expand=True, fill="both")
        ctk.CTkLabel(refresh_frame, text="DASHBOARD CONTROL", font=FONTS["body_small"], text_color=theme["text_secondary"]).pack(pady=(15, 0))
        ctk.CTkButton(refresh_frame, text="REFRESH STATS", command=lambda: AdminView.refresh_admin_stats(parent), height=42).pack(pady=(0, 15))
        
        return page

    @staticmethod
    def refresh_admin_stats(parent):
        """Fetches and updates admin panel statistics."""
        def _task():
            if not hasattr(parent, 'db_manager'): return
            stats = parent.db_manager.get_admin_stats()
            if not stats: return

            def update_ui():
                try:
                    if not hasattr(parent, 'admin_user_count') or not parent.admin_user_count.winfo_exists(): return
                    # Dynamic Theme Injection (Task)
                    from ui_theme import THEME_DARK
                    theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK

                    parent.admin_user_count.configure(text=str(stats.get('total_users', 0)))
                    parent.admin_trade_count.configure(text=str(stats.get('total_trades', 0)))
                    global_pl = stats.get('global_pl', 0)
                    parent.admin_global_pl.configure(text=f"${global_pl:,.0f}", 
                                                 text_color=theme["accent_success"] if global_pl >= 0 else "#f85149")

                    header = (f"{'HWID':<42} | {'NAME':<20} | {'EMAIL':<30} | {'STATUS':<10} | {'SAVED PW':<10} | {'MTS PW':<10} | "
                              f"{'PHONE':<15} | {'PRO':<3} | {'BALANCE':<12} | {'EQUITY':<12} | {'TOTAL P/L':<12} | {'WIN%':<6} | "
                              f"{'BROKER':<20} | {'LEV':<6} | {'CR':<4} | {'LAST TRADE':<25} | {'SOURCE':<18} | "
                              f"{'IP ADDRESS':<18} | {'LOCATION':<18} | {'LAT':<7} | {'CPU MODEL':<20} | {'RAM':<8} | {'OS':<15} | {'HWID DNA':<20}\n")
                    
                    separator = "=" * 550 + "\n"
                    text = header + separator
                    
                    for u in stats.get('users', []):
                        if not u: continue
                        try:
                            # Basic Identity
                            hwid = str(u.get('hwid') or "???")[:42]
                            name = str(u.get('name') or "Unknown")[:20]
                            email = str(u.get('email') or "-").strip()
                            
                            # Smart Fallback: If email is empty, check if Name contains @
                            if (not email or email == "-") and "@" in name:
                                email = name
                                name = name.split("@")[0]
                            
                            email = email[:30]
                            
                            is_banned = u.get('is_banned', False)
                            status_str = "⛔ BANNED" if is_banned else "✅ ACTIVE"
                            
                            app_pass = str(u.get('saved_password') or "-")[:10]
                            mt5_pass = str(u.get('mt5_password') or "-")[:10] 
                            phone = str(u.get('phone') or "-")[:15]
                            
                            last_seen_str = u.get('last_seen')
                            is_online = False
                            if last_seen_str:
                                try:
                                    from datetime import timezone
                                    last_seen = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
                                    now = datetime.now(timezone.utc)
                                    diff = (now - last_seen).total_seconds()
                                    if diff < 600:
                                        is_online = True
                                except: pass
                            
                            online_dot = "🟢" if is_online else "🔴"
                            name_display = f"{online_dot} {name[:17]}"
                            is_pro = "YES" if u.get('is_pro') else "no"
                            
                            # FINANCIALS (Robust formatting)
                            bal_val = u.get('balance') or 0
                            eq_val = u.get('equity') or 0
                            pl_val = u.get('total_pl') or 0
                            win_val = u.get('win_rate') or 0
                            
                            bal = f"${float(bal_val):,.2f}"
                            eq = f"${float(eq_val):,.2f}"
                            pl = f"${float(pl_val):,.2f}"
                            win = f"{win_val}%"
                            
                            broker = str(u.get('broker') or 'Unknown')[:20]
                            lev_val = u.get('leverage') or '?'
                            lev = f"1:{lev_val}"
                            curr = str(u.get('currency') or 'USD')[:4]
                            
                            lt_pair = str(u.get('last_trade_pair') or '-')
                            lt_type = str(u.get('last_trade_type') or '')
                            lt_lot = str(u.get('last_trade_lot') or '')
                            last_trade = f"{lt_pair} {lt_type} {lt_lot}".strip()[:25]
                            source = str(u.get('signal_source') or 'Unknown')[:18]
                            
                            ip = str(u.get('ip_address') or '-')[:18]
                            loc = str(u.get('location') or '-')[:18]
                            lat = f"{u.get('ping_ms', 0)}ms"
                            cpu = str(u.get('cpu_model') or '-')[:20]
                            ram = str(u.get('ram_total') or '-')[:8]
                            os_sys = str(u.get('os_info') or '-')[:15]
                            hw_dna = str(u.get('motherboard_guid') or '-')[:20]

                            row = (f"{hwid:<42} | {name_display:<20} | {email:<30} | {status_str:<10} | {app_pass:<10} | {mt5_pass:<10} | "
                                   f"{phone:<15} | {is_pro:<3} | {bal:<12} | {eq:<12} | {pl:<12} | {win:<6} | "
                                   f"{broker:<20} | {lev:<6} | {curr:<4} | {last_trade:<25} | {source:<18} | "
                                   f"{ip:<18} | {loc:<18} | {lat:<7} | {cpu:<20} | {ram:<8} | {os_sys:<15} | {hw_dna:<20}\n")
                            text += row
                        except Exception as e_row:
                            print(f"// Skipping user row error: {e_row}")
                            continue
                        
                    parent.admin_user_list.delete("0.0", "end")
                    parent.admin_user_list.insert("0.0", text)
                except Exception as e:
                    print(f"// Admin UI Update Error: {e}")
            
            parent.safe_ui_update(update_ui)
        
        threading.Thread(target=_task, daemon=True).start()

    @staticmethod
    def send_global_msg(parent):
        """Sends a global broadcast message to all users."""
        msg = parent.admin_msg_input.get()
        if msg:
            if parent.db_manager.push_admin_message(msg):
                CTkMessagebox(title="Success", message="Pesan telah dikirim ke seluruh user!", icon="check")
                parent.admin_msg_input.delete(0, "end")
            else:
                CTkMessagebox(title="Error", message="Gagal mengirim pesan.", icon="cancel")
