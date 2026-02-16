# --- IMPORTS ---
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from ui_theme import THEME_DARK, FONTS

THEME = THEME_DARK

class UserInspectorPanel(ctk.CTkToplevel):
    """
    World-Class 6-Panel Mission Control User Inspector.
    Redesigned from Tabview to Grid Layout matching mockup.
    """
    
    TAG_OPTIONS = ["VIP", "BEGINNER", "WHALE", "RISKY", "SUPPORT"]
    
    def __init__(self, parent, db_manager, user_hwid):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_hwid = user_hwid
        self.user_data = db_manager.get_full_user_profile(user_hwid)
        
        if not self.user_data:
            CTkMessagebox(title="Error", message="User not found!", icon="cancel")
            self.destroy()
            return
            
        # --- WINDOW CONFIG ---
        self.title(f"🔍 USER INSPECTOR - {self.user_data.get('name', 'Unknown')}")
        self.geometry("1250x900")
        self.configure(fg_color="#0d1117")
        self.resizable(True, True)
        self.attributes('-topmost', True)
        
        # --- BUILD UI ---
        self._build_header()
        self._build_main_grid()
        self._build_flags_row()
        self._build_footer()

    # --- HEADER ---
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=12, height=100)
        header.pack(fill="x", padx=15, pady=(15, 10))
        header.pack_propagate(False)
        
        # Left: Avatar + Name + Badges
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(left, text="👤", font=("Segoe UI Emoji", 48)).pack(side="left")
        
        info = ctk.CTkFrame(left, fg_color="transparent")
        info.pack(side="left", padx=15)
        
        ctk.CTkLabel(info, text=self.user_data.get('name', 'Unknown'), 
                     font=("Segoe UI Bold", 28)).pack(anchor="w")
        
        badge_row = ctk.CTkFrame(info, fg_color="transparent")
        badge_row.pack(anchor="w", pady=(5, 0))
        
        # Online Status
        is_online = self._check_online_status()
        self._create_badge(badge_row, "🟢 ONLINE" if is_online else "⚪ OFFLINE", 
                          "#2ea44f" if is_online else "#6e7681")
        
        if self.user_data.get('is_pro'):
            self._create_badge(badge_row, "💎 PRO", "#8b5cf6")
        
        if self.user_data.get('is_banned'):
            self._create_badge(badge_row, "🚫 BANNED", "#f85149")
        else:
            self._create_badge(badge_row, "✓ ACTIVE", "#2ea44f")
        
        # Right: Action Buttons
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=20)
        
        ctk.CTkButton(right, text="💬 CHAT", width=90, height=36, 
                      fg_color="#0d6efd", hover_color="#0b5ed7",
                      command=self._send_dm).pack(side="left", padx=5)
        ctk.CTkButton(right, text="🚫 BAN USER", width=110, height=36, 
                      fg_color="#f85149", hover_color="#da3633",
                      command=self._toggle_ban).pack(side="left", padx=5)
        ctk.CTkButton(right, text="📋 COPY HWID", width=110, height=36, 
                      fg_color="#238636", hover_color="#2ea44f",
                      command=self._copy_hwid).pack(side="left", padx=5)

    def _check_online_status(self):
        last_seen = self.user_data.get('last_seen')
        if not last_seen:
            return False
        try:
            from datetime import datetime, timezone
            last = datetime.fromisoformat(str(last_seen).replace('Z', '+00:00'))
            return (datetime.now(timezone.utc) - last).total_seconds() < 300
        except:
            return False

    def _create_badge(self, parent, text, color):
        ctk.CTkLabel(parent, text=text, font=("Segoe UI Bold", 11), fg_color=color,
                     corner_radius=6, padx=12, pady=4).pack(side="left", padx=3)

    # --- MAIN UI ---
    def _build_main_grid(self):
        # Create Tabview for better organization
        self.tab_view = ctk.CTkTabview(self, fg_color="transparent")
        self.tab_view.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tab_view.add("MAIN DASHBOARD")
        self.tab_view.add("RAW CONFIG & TELEMETRY")
        
        # --- TAB 1: DASHBOARD (Original 6 Panels) ---
        dash = self.tab_view.tab("MAIN DASHBOARD")
        
        # Row 1: Identity | Financial | Trading
        row1 = ctk.CTkFrame(dash, fg_color="transparent")
        row1.pack(fill="both", expand=True, pady=5)
        
        self._build_identity_panel(row1)
        self._build_financial_panel(row1)
        self._build_trading_panel(row1)
        
        # Row 2: Network | Device | Activity
        row2 = ctk.CTkFrame(dash, fg_color="transparent")
        row2.pack(fill="both", expand=True, pady=5)
        
        self._build_network_panel(row2)
        self._build_device_panel(row2)
        self._build_activity_panel(row2)
        
        # --- TAB 2: DEEP TELEMETRY (New) ---
        self._build_telemetry_tab(self.tab_view.tab("RAW CONFIG & TELEMETRY"))

    def _build_telemetry_tab(self, parent_frame):
        """Renders the Raw JSON Telemetry Data"""
        scroll = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        data = self.user_data.get('telemetry_data', {})
        if not data:
            ctk.CTkLabel(scroll, text="No Deep Telemetry Data Received Yet.", 
                         font=("Consolas", 14), text_color="gray").pack(pady=40)
            ctk.CTkLabel(scroll, text="* User needs to be online with v2.1.0+ Client", 
                         font=("Consolas", 12), text_color="gray").pack()
            return

        # Categorize
        categories = {'sys': '🖥 SYSTEM', 'mt5': '📈 MT5 RAW', 'config': '⚙️ CONFIG DUMP', 'screen': '📺 SCREEN', 'app': '📱 APP'}
        
        sorted_keys = sorted(data.keys())
        current_cat = ""
        
        for key in sorted_keys:
            # Detect Category based on prefix
            cat = key.split('_')[0]
            if cat in categories and cat != current_cat:
                current_cat = cat
                # Category Header
                ctk.CTkLabel(scroll, text=f"\n{categories[cat]}", font=("Segoe UI Bold", 14), 
                             text_color="#58a6ff", anchor="w").pack(fill="x", pady=(10, 5))
            
            # Row
            row = ctk.CTkFrame(scroll, fg_color="#161b22", corner_radius=6)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=key, font=("Consolas", 12), text_color="#8b949e", width=200, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=str(data[key]), font=("Consolas", 12, "bold"), text_color="#e6edf3", anchor="w").pack(side="left", padx=10)

    def _build_panel(self, parent, title, icon):
        """Helper: Creates a glass panel card"""
        panel = ctk.CTkFrame(parent, fg_color="#161b22", corner_radius=12, 
                             border_width=1, border_color="#30363d")
        panel.pack(side="left", fill="both", expand=True, padx=5)
        
        # Title Header
        ctk.CTkLabel(panel, text=f"{icon}  {title}", font=("Segoe UI Bold", 13),
                     text_color="#58a6ff").pack(anchor="w", padx=15, pady=(12, 8))
        
        content = ctk.CTkFrame(panel, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        return content

    def _add_field(self, parent, label, value, color=None, is_secret=False):
        """Helper: Adds a label-value row"""
        row = ctk.CTkFrame(parent, fg_color="transparent", height=24)
        row.pack(fill="x", pady=2)
        row.pack_propagate(False)
        
        ctk.CTkLabel(row, text=label, font=("Consolas", 11), text_color="#8b949e",
                     width=110, anchor="w").pack(side="left")
        
        display_val = "********" if is_secret else str(value or "N/A")
        val_color = color or "#e6edf3"
        val_label = ctk.CTkLabel(row, text=display_val, font=("Consolas", 11, "bold"),
                                 text_color=val_color, anchor="w")
        val_label.pack(side="left", fill="x", expand=True)
        
        if is_secret and value:
            ctk.CTkButton(row, text="👁", width=28, height=22, fg_color="#30363d",
                         command=lambda v=value, l=val_label: l.configure(text=v)).pack(side="right")

    # --- PANEL 1: IDENTITY & QUOTA ---
    def _build_identity_panel(self, parent):
        content = self._build_panel(parent, "IDENTITY & SECURITY", "🔐")
        d = self.user_data
        
        self._add_field(content, "HWID", d.get('hwid'))
        self._add_field(content, "NAME", d.get('name'))
        self._add_field(content, "EMAIL", d.get('email'))
        self._add_field(content, "PHONE", d.get('phone'))
        
        # Admin Quota Controls
        ctk.CTkLabel(content, text="─── AI QUOTA ───", font=("Segoe UI", 9), text_color="#6e7681").pack(pady=5)
        
        # Tier Selector
        row_tier = ctk.CTkFrame(content, fg_color="transparent")
        row_tier.pack(fill="x", pady=2)
        ctk.CTkLabel(row_tier, text="TIER", font=("Consolas", 11), text_color="#8b949e", width=60, anchor="w").pack(side="left")
        self.tier_var = ctk.StringVar(value=d.get('subscription_tier', 'STANDARD'))
        self.combo_tier = ctk.CTkComboBox(row_tier, values=["STANDARD", "GOLD", "VIP", "PLATINUM", "INSTITUTIONAL"],
                                         width=140, height=24, variable=self.tier_var,
                                         font=("Consolas", 11))
        self.combo_tier.pack(side="left")
        
        # Override
        row_ov = ctk.CTkFrame(content, fg_color="transparent")
        row_ov.pack(fill="x", pady=2)
        ctk.CTkLabel(row_ov, text="OVERRIDE", font=("Consolas", 11), text_color="#8b949e", width=60, anchor="w").pack(side="left")
        self.entry_override = ctk.CTkEntry(row_ov, width=80, height=24, placeholder_text="Limit")
        if d.get('ai_limit_override'):
            self.entry_override.insert(0, str(d.get('ai_limit_override')))
        self.entry_override.pack(side="left")
        
        ctk.CTkButton(row_ov, text="💾", width=30, height=24, fg_color="#238636", 
                     command=self._update_quota).pack(side="right", padx=5)

        # Subscription Mode Forge
        row_dur = ctk.CTkFrame(content, fg_color="transparent")
        row_dur.pack(fill="x", pady=2)
        ctk.CTkLabel(row_dur, text="DURATION", font=("Consolas", 11), text_color="#8b949e", width=60, anchor="w").pack(side="left")
        self.forge_var = ctk.StringVar(value="MONTHLY")
        self.combo_forge = ctk.CTkComboBox(row_dur, values=["MONTHLY", "YEARLY", "LIFETIME"],
                                          width=140, height=24, variable=self.forge_var,
                                          font=("Consolas", 11))
        self.combo_forge.pack(side="left")
        
        ctk.CTkButton(row_dur, text="🔨", width=30, height=24, fg_color="#8b5cf6", 
                     command=self._forge_subscription).pack(side="right", padx=5)

        ctk.CTkLabel(content, text="─── SECURITY ───", font=("Segoe UI", 9), text_color="#6e7681").pack(pady=5)
        self._add_field(content, "IS_BANNED", "YES" if d.get('is_banned') else "NO",
                       color="#f85149" if d.get('is_banned') else "#2ea44f")

    def _update_quota(self):
        tier = self.tier_var.get()
        ov_str = self.entry_override.get().strip()
        override = int(ov_str) if ov_str.isdigit() else None
        
        if self.db_manager.set_user_tier(self.user_hwid, tier, override):
             CTkMessagebox(title="Success", message=f"User upgraded to {tier}!", icon="check")
        else:
             CTkMessagebox(title="Error", message="Update failed", icon="cancel")

    def _forge_subscription(self):
        mode = self.forge_var.get()
        if self.db_manager.set_user_subscription(self.user_hwid, mode):
             CTkMessagebox(title="Success", message=f"User duration forged to {mode}!", icon="check")
        else:
             CTkMessagebox(title="Error", message="Forge failed", icon="cancel")

    # --- PANEL 2: FINANCIAL ---
    def _build_financial_panel(self, parent):
        content = self._build_panel(parent, "FINANCIAL", "💰")
        d = self.user_data
        
        # Big Balance Display
        balance = d.get('balance') or 0
        bal_frame = ctk.CTkFrame(content, fg_color="transparent")
        bal_frame.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(bal_frame, text=f"${balance:,.2f}", font=("Segoe UI Bold", 28),
                     text_color="#2ea44f").pack(anchor="w")
        ctk.CTkLabel(bal_frame, text="BALANCE", font=("Segoe UI", 10),
                     text_color="#8b949e").pack(anchor="w")
        
        self._add_field(content, "EQUITY", f"${d.get('equity', 0):,.2f}", color="#2ea44f")
        
        pl = d.get('total_pl') or d.get('pl') or 0
        self._add_field(content, "TOTAL_PL", f"${pl:,.2f}", 
                       color="#2ea44f" if pl >= 0 else "#f85149")
        
        wr = d.get('win_rate') or 0
        self._add_field(content, "WIN_RATE", f"{wr}%", 
                       color="#2ea44f" if wr > 50 else "#f85149")
        self._add_field(content, "CURRENCY", d.get('currency') or "USD")

    # --- PANEL 3: BROKER & TRADING ---
    def _build_trading_panel(self, parent):
        content = self._build_panel(parent, "BROKER & TRADING", "📈")
        d = self.user_data
        
        self._add_field(content, "BROKER", d.get('broker'))
        self._add_field(content, "SERVER", d.get('server'))
        self._add_field(content, "LEVERAGE", f"1:{d.get('leverage', 0)}")
        self._add_field(content, "LAST_PAIR", d.get('last_trade_pair'))
        self._add_field(content, "LAST_LOT", d.get('last_trade_lot'))
        
        trade_type = d.get('last_trade_type') or ''
        self._add_field(content, "LAST_TYPE", trade_type,
                       color="#2ea44f" if trade_type == "BUY" else "#f85149")
        self._add_field(content, "SIGNAL_SRC", d.get('signal_source'))
        self._add_field(content, "WIN_RATE", f"{d.get('win_rate', 0)}%")

    # --- PANEL 4: NETWORK ---
    def _build_network_panel(self, parent):
        content = self._build_panel(parent, "NETWORK & SECURITY", "🌐")
        d = self.user_data
        
        self._add_field(content, "IP_ADDRESS", d.get('ip_address'))
        self._add_field(content, "LOCATION", d.get('location'))
        self._add_field(content, "ISP", d.get('isp'))
        
        ping = d.get('ping_ms') or 0
        ping_color = "#2ea44f" if ping < 100 else "#f0883e" if ping < 300 else "#f85149"
        self._add_field(content, "PING_MS", f"{ping}ms", color=ping_color)
        self._add_field(content, "MAC_ADDR", d.get('mac_address'))

    # --- PANEL 5: DEVICE ---
    def _build_device_panel(self, parent):
        content = self._build_panel(parent, "DEVICE INFO", "🖥️")
        d = self.user_data
        
        self._add_field(content, "OS_INFO", d.get('os_info'))
        self._add_field(content, "DEVICE", d.get('device_name'))
        
        quota = d.get('ai_bonus_quota') or 0
        self._add_field(content, "AI_QUOTA", f"{quota}/100")
        
        ai_q = d.get('last_ai_question') or "No questions"
        truncated = ai_q[:40] + "..." if len(ai_q) > 40 else ai_q
        self._add_field(content, "LAST_AI_Q", truncated)

    # --- PANEL 6: ACTIVITY ---
    def _build_activity_panel(self, parent):
        content = self._build_panel(parent, "ACTIVITY LOG", "📊")
        d = self.user_data
        
        self._add_field(content, "LAST_SEEN", str(d.get('last_seen', 'Never'))[:19])
        self._add_field(content, "LAST_LOGOUT", str(d.get('last_logout', 'Never'))[:19])
        
        # Privacy Section
        ctk.CTkLabel(content, text="─── Privacy ───", font=("Segoe UI", 9),
                     text_color="#6e7681").pack(pady=5)
        self._add_field(content, "PUB_PROFIT", "ON" if d.get('publish_profit') else "OFF",
                       color="#2ea44f" if d.get('publish_profit') else "#6e7681")
        self._add_field(content, "PUB_KNOWLEDGE", "ON" if d.get('publish_knowledge') else "OFF")
        self._add_field(content, "INITIALS_ONLY", "ON" if d.get('publish_initials_only') else "OFF")

    # --- FLAGS ROW ---
    def _build_flags_row(self):
        flags_frame = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=8, height=45)
        flags_frame.pack(fill="x", padx=15, pady=5)
        flags_frame.pack_propagate(False)
        
        ctk.CTkLabel(flags_frame, text="⚠️ FLAGS:", font=("Segoe UI Bold", 12),
                     text_color="#f0883e").pack(side="left", padx=15)
        
        d = self.user_data
        flags = []
        
        # Low Balance
        if (d.get('balance') or 0) < 100:
            flags.append(("💸 LOW BALANCE", "#f85149"))
        
        # Inactive 7+ days
        from datetime import datetime, timezone
        last_seen = d.get('last_seen')
        if last_seen:
            try:
                last = datetime.fromisoformat(str(last_seen).replace('Z', '+00:00'))
                if (datetime.now(timezone.utc) - last).days >= 7:
                    flags.append(("⏰ INACTIVE 7+ DAYS", "#f0883e"))
            except: pass
        
        # Hot Streak
        if (d.get('win_rate') or 0) > 70:
            flags.append(("🔥 HOT STREAK", "#2ea44f"))
        
        # New User
        if not d.get('balance') and not d.get('broker'):
            flags.append(("🆕 NEW USER", "#58a6ff"))
        
        if not flags:
            flags.append(("✓ NO ISSUES", "#2ea44f"))
        
        for text, color in flags:
            ctk.CTkLabel(flags_frame, text=text, font=("Segoe UI", 11), fg_color=color,
                        corner_radius=6, padx=10, pady=3).pack(side="left", padx=4)

    # --- FOOTER ---
    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=12)
        footer.pack(fill="x", padx=15, pady=(5, 15))
        
        # Admin Notes
        notes_frame = ctk.CTkFrame(footer, fg_color="transparent")
        notes_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        ctk.CTkLabel(notes_frame, text="📝 ADMIN NOTES", font=("Segoe UI Bold", 12)).pack(anchor="w")
        
        self.notes_entry = ctk.CTkTextbox(notes_frame, height=60, fg_color="#0d1117", border_width=1)
        self.notes_entry.pack(fill="x", pady=5)
        self.notes_entry.insert("0.0", self.user_data.get('admin_notes') or "")
        
        ctk.CTkButton(notes_frame, text="💾 SAVE NOTES", width=120, fg_color="#238636",
                     command=self._save_notes).pack(anchor="e")
        
        # User Tags
        tags_frame = ctk.CTkFrame(footer, fg_color="transparent", width=350)
        tags_frame.pack(side="right", fill="y", padx=15, pady=10)
        tags_frame.pack_propagate(False)
        
        ctk.CTkLabel(tags_frame, text="🏷️ USER TAGS", font=("Segoe UI Bold", 12)).pack(anchor="w")
        
        tags_row = ctk.CTkFrame(tags_frame, fg_color="transparent")
        tags_row.pack(fill="x", pady=8)
        
        current_tags = self.user_data.get('user_tags') or []
        for tag in self.TAG_OPTIONS:
            is_active = tag in current_tags
            ctk.CTkButton(tags_row, text=tag, width=65, height=28,
                         fg_color="#238636" if is_active else "#30363d",
                         command=lambda t=tag: self._toggle_tag(t)).pack(side="left", padx=2)

    # --- ACTIONS ---
    def _save_notes(self):
        notes = self.notes_entry.get("0.0", "end-1c")
        if self.db_manager.update_admin_notes(self.user_hwid, notes):
            CTkMessagebox(title="Success", message="Notes saved!", icon="check")
        else:
            CTkMessagebox(title="Error", message="Failed to save notes", icon="cancel")

    def _toggle_tag(self, tag):
        current = self.user_data.get('user_tags') or []
        if tag in current:
            current.remove(tag)
        else:
            current.append(tag)
        
        if self.db_manager.update_user_tags(self.user_hwid, current):
            self.user_data['user_tags'] = current
            CTkMessagebox(title="Success", message=f"Tag '{tag}' updated!", icon="check")

    def _send_dm(self):
        dialog = ctk.CTkInputDialog(text="Enter message for this user:", title="Send DM")
        msg = dialog.get_input()
        if msg:
            if self.db_manager.send_dm(self.user_hwid, msg):
                CTkMessagebox(title="Success", message="DM sent!", icon="check")

    def _toggle_ban(self):
        is_banned = self.user_data.get('is_banned', False)
        action = "Restore user access?" if is_banned else "Revoke license and BAN user?"
        if CTkMessagebox(title="Confirm", message=action, icon="warning", 
                        option_1="Yes", option_2="No").get() == "Yes":
            success, msg = self.db_manager.update_ban_status(self.user_hwid, not is_banned)
            if success:
                CTkMessagebox(title="Done", message="User status updated!", icon="check")
                self.destroy()

    def _copy_hwid(self):
        self.clipboard_clear()
        self.clipboard_append(self.user_hwid)
        CTkMessagebox(title="Copied", message=f"HWID copied to clipboard!", icon="info")
