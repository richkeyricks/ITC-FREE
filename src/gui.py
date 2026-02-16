# src/gui.py
"""
SIMPLE TELEGRAM COPYTRADE (STC) +AI - Professional GUI
Powered by Haineo AI

Professional layout with sidebar navigation.
"""
import os
import sys
import ctypes

# --- CRITICAL FIX: PRE-LOAD SQLITE3.DLL (MUST BE FIRST) ---
try:
    if getattr(sys, 'frozen', False):
        import os
        base_path = sys._MEIPASS
        sqlite_dll_path = os.path.join(base_path, 'sqlite3.dll')
        if os.path.exists(sqlite_dll_path):
            ctypes.CDLL(sqlite_dll_path)
            print(f"// SUCCESS: Pre-loaded sqlite3.dll from {sqlite_dll_path}")
except Exception as e:
    print(f"// DLL Pre-load Error: {e}")
# ----------------------------------------------------------
from dotenv import load_dotenv, set_key



# Gravity Rule: Ensure src is in sys.path for absolute imports
_base_dir = os.path.dirname(os.path.abspath(__file__))
if _base_dir not in sys.path:
    sys.path.insert(0, _base_dir)

# Load ENV first for top-level theme detection
load_dotenv()

import threading
import time
import requests
import queue
import traceback
from datetime import datetime
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

# --- LOCAL IMPORTS ---
from index import (parse_signal, execute_trade, close_all_orders, monitor_trades, 
                   check_internet, get_mt5_status, get_account_meta, get_env_list, 
                   chat_with_ai, app as tg_app, set_signal_callback, get_positions, get_history_orders,
                   login_mt5_custom)
from ui_theme import get_theme, FONTS, SPACING, RADIUS, HEIGHTS, THEME_DARK
from ui_theme_modern import get_theme as get_modern_theme, FONTS as MODERN_FONTS, RADIUS as MODERN_RADIUS

from PIL import Image

# Import new modules for Chart + AI
from modules.chart.chart_data import ChartDataManager
from modules.chart.chart_renderer import ChartRenderer
from modules.ai.chart_analyzer import AIChartAnalyzer
from modules.db.supabase_client import SupabaseManager
from legal import EULA_TEXT
from utils.tooltips import CTkToolTip
from localization import Translator
from modules.ui.changelog_viewer import ChangelogViewer
from modules.ui.ai_view import AIView
from modules.ui.telegram_view import TelegramView
from modules.ui.mt5_view import MT5View
from modules.ui.trading_view import TradingView
from modules.ui.risk_view import RiskView
from modules.ui.dashboard_view import DashboardView
from modules.ui.analysis_view import AnalysisView
from modules.ui.marketplace_view import MarketplaceView
from modules.ui.spc_hub_view import SPCHubView
from modules.ui.logs_view import LogsView
from modules.ui.leaderboard_view import LeaderboardView
from modules.ui.education_view import EducationView
from modules.ui.news_view import NewsView
from modules.ui.settings_view import SettingsView
from modules.ui.admin_view import AdminView
from modules.ui.inspector_panel import UserInspectorPanel
from modules.ui.journal_view import JournalView
from modules.ui.chat_popup import StrictChatPopup
from modules.ui.auth_view import AuthView
from modules.ui.referral_view import ReferralView
from modules.ui.donation_view import DonationView
from modules.ui.eula_view import EULAView
from modules.logic.auth_service import AuthService
from modules.logic.affiliate_service import AffiliateService # Added for Referral Engine
from modules.logic.settings_manager import SettingsManager
from modules.logic.ai_manager import AIManager
from modules.logic.app_controller import AppController
from modules.logic.copier_controller import CopierController
from modules.logic.trading_controller import TradingController
from modules.logic.config_aggregator import ConfigAggregator
from modules.ui.tutorial_view import TutorialView
from modules.ui.navigation_panel import NavigationPanel
from modules.ui.navigation_panel_modern import ModernNavigationPanel
from modules.ui.premium_splash import PremiumSplash
from modules.ui.startup_view import StartupView
from constants.changelog_data import CHANGELOG_DATA

# --- THEME ---
theme_flag = os.getenv("UI_THEME", "dark")
if theme_flag in ["light", "neutral", "dark_modern"]:
    from ui_theme_modern import apply_theme_to_ctk as apply_modern_theme
    apply_modern_theme(ctk, "dark" if theme_flag == "dark_modern" else theme_flag)
else:
    ctk.set_appearance_mode("Dark")
THEME = THEME_DARK


# --- APP VERSION ---
APP_VERSION = "v5.1.4" # [PASSIVE_SYNC_MASTERY]


def handle_exception(exc_type, exc_value, exc_traceback):
    """Global handler for unhandled exceptions to prevent silent crashes"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    try:
        with open("crash_report.txt", "a") as f:
            f.write(f"\n\n--- CRASH LOG {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            f.write(error_msg)
    except:
        pass
    
    print(f"// CRITICAL ERROR: {exc_value}")
    # Optional: Display a popup before exiting
    try:
        # We create a temporary window to show the error if mainloop is broken
        temp_root = ctk.CTk()
        temp_root.withdraw()
        CTkMessagebox(title="Critical Error", 
                       message=f"Application encountered a critical error and must close.\nDetails saved to crash_report.txt\n\nError: {exc_value}", 
                       icon="cancel")
    except:
        pass
    sys.exit(1)

sys.excepthook = handle_exception

class STCApp(ctk.CTk):
    """Main Application Window with Sidebar Navigation"""
    
    APP_TITLE = "ITC - Intelligence Telegram Copytrade +AI"
    VERSION = "v4.9.5"
    
    def __init__(self):
        super().__init__()
        load_dotenv()
        
        # 1. HIDE PRINCIPAL WINDOW IMMEDIATELY
        self.withdraw()
        
        # 2. SHOW PREMIUM SPLASH
        try:
            self.splash = PremiumSplash(self)
        except:
            self.splash = None
            
        # 3. REGISTER KILL SWITCH (Crucial for Zombie App Fix)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.boot_start = time.time()
        
        # --- PULSED BOOT SEQUENCE (v4 Architecture) ---
        # Instead of lazy loading, we pre-render key modules to ensure 0ms navigation.
        # We use a localized helper to pulse the UI thread.
        def _loading_pulse(percent, text):
            if hasattr(self, 'splash') and self.splash:
                self.splash.update_progress(percent, text)
                # self.update() # REMOVED: Do not force main update manually here to avoid thread conflict
        
        self._pulse_callback = _loading_pulse

        # --- A. INITIAL CONFIG (Fast) ---
        self.env = {} # Initial placeholder for safety
        try:
            current_lang = os.getenv("APP_LANGUAGE", "EN")
            self.translator = Translator(current_lang)
            self.env = get_env_list() # Standardize environment access for views
            
            self.selected_theme = os.getenv("UI_THEME", "dark")
            if self.selected_theme in ["light", "neutral", "dark_modern"]:
                from ui_theme_modern import get_theme as get_modern_theme
                self.theme_data = get_modern_theme("dark" if self.selected_theme == "dark_modern" else self.selected_theme)
                self.configure(fg_color=self.theme_data["bg_primary"])
            else:
                self.theme_data = THEME
                self.configure(fg_color=THEME["bg_primary"])
                
            self.title(self.translator.get("app_title"))
            # self.geometry("1100x750") # REMOVED: Causes resize glitch. We go straight to zoomed.
            # self.minsize(1000, 700) # REMOVED: Potential conflict with Zoomed state on some OS
            
            # --- ASSET LOADING (PyInstaller Compatible) ---
            from utils.path_helper import resource_path
            try:
                icon_path = resource_path("assets/app_icon.ico")
                if icon_path and os.path.exists(icon_path):
                    try:
                        # Primary: Set Window Icon (ICO)
                        self.iconbitmap(icon_path)
                        
                        # Secondary (High-Res Fix): Set Icon Photo (PNG/ICO layer) for Taskbar/High-DPI
                        from PIL import ImageTk
                        img = Image.open(icon_path)
                        photo = ImageTk.PhotoImage(img)
                        self.iconphoto(True, photo)
                        self._icon_photo_ref = photo # Keep reference to avoid GC
                    except Exception as e_icon:
                        print(f"// Icon Load Error: {e_icon}")
            except: pass
            
        except Exception as e:
            print(f"// Theme/Loc Error: {e}")
            self.translator = Translator("ID") # Critical Fallback
            if not hasattr(self, 'env') or not self.env:
                self.env = {} # Ensure it exists even if get_env_list fails
            self.configure(fg_color="#1c1c1c")

        # --- B. MASTER ASYNC BOOT (The Heavy Lifter) ---
        self.ui_queue = queue.Queue()
        self._process_queue_loop()
        
        # State Management
        self.current_page = "dashboard"
        self.menu_buttons = {}

        # We launch a SINGLE background thread to handle ALL BLOCKING IO.
        threading.Thread(target=self._async_boot_sequence, daemon=True).start()

    def _async_boot_sequence(self):
        """
        MASTER ASYNC BOOT
        Executes ALL blocking network/disk IO in background.
        Updates Splash via safe_ui_update.
        """
        # Helper for thread-safe splash update
        def update_splash(pct, msg):
            self.safe_ui_update(lambda: self._pulse_callback(pct, msg))

        # 1. SUPABASE BRIDGE (Network - Level 0 Priority)
        update_splash(15, "Establishing Supabase Bridge...")
        try:
            self.db_manager = SupabaseManager()
            self.quota_warned = False 
            self.is_pro = False
            
            # --- CLOUD VAULT INJECTION ---
            # Any key in 'app_secrets' table will override/fallback local .env
            update_splash(25, "Fetching Secure Cloud Vault...")
            cloud_secrets = self.db_manager.fetch_all_secrets()
            if cloud_secrets:
                for key, val in cloud_secrets.items():
                    if val:
                        os.environ[key] = str(val)
                print(f"// Vault: {len(cloud_secrets)} secrets injected from Cloud.")
        except Exception as e:
            print(f"// Supabase Core Error: {e}")
            self.db_manager = None

        # 2. MT5 HANDSHAKE (Network / Process) - DEFERRED TO POST-AUTH
        self.is_mt5_connected = False
        self.is_telegram_validated = False
        # update_splash(35, "Initializing MT5 Service (Background)...")
        # try:
        #     from modules.mt5.mt5_service import MT5Service
        #     service = MT5Service.instance()
        #     login_str = os.getenv("MT5_LOGIN", "0").strip()
        #     mt5_login = int(login_str) if login_str.isdigit() else 0
        #     mt5_pass = os.getenv("MT5_PASSWORD", "")
        #     mt5_serv = os.getenv("MT5_SERVER", "")
        #     if mt5_login > 0:
        #         if service.initialize(login=mt5_login, password=mt5_pass, server=mt5_serv):
        #             self.is_mt5_connected = True
        # except Exception as e:
        #     print(f"// MT5 Async Init Error: {e}")

        # 3. SERVICES LAYER (Logic)
        update_splash(45, "Loading Service Plugins...")
        try:
            from modules.logic.affiliate_service import AffiliateService
            if self.db_manager:
                self.affiliate_service = AffiliateService(self.db_manager)
        except Exception as e:
             print(f"// Service Plugin Error: {e}")

        # 4. AI INTELLIGENCE (Config/Network)
        update_splash(55, "Preparing AI Intelligence...")
        try:
            self.analyzer = AIChartAnalyzer()
            self.last_analysis = None
        except Exception as e:
             print(f"// AI Analyer Error: {e}")
             self.analyzer = None

        # 5. QUEUE SYSTEM
        update_splash(65, "Calibrating Async Engines...")

        # --- BOOT COMPLETE -> HANDOFF TO MAIN THREAD ---
        update_splash(75, "Finalizing UI Shell...")
        self.safe_ui_update(self._finalize_boot)

    def _finalize_boot(self):
        """
        MAIN THREAD HANDLER
        Constructs UI widgets (must be on main thread) and reveals app.
        """
        # Start Queue Loop
        self._process_queue_loop()

        # 1. UI SHELL ARCHITECTURE
        # REMOVED: Premature UI Building causing Flash. Moved to show_main_interface()
        # self._create_sidebar()
        # self._create_topbar()
        # self._create_main_area() # Will be created after login

        self.pages = {}
        
        # 2. DASHBOARD OVERHAUL (DEFERRED)
        # We handle this via show_main_interface() -> lazy load
        try:
             self._pulse_callback(75, "Architecting Command Center...")
             # self.pages["dashboard"] = DashboardView.build(self, progress_callback=None)
        except Exception as e:
             pass

        # 3. MARKETPLACE ENGINE (DEFERRED)
        try:
             self._pulse_callback(85, "Connecting Global Marketplace...")
             pass
        except Exception as e:
             pass

        # 4. AI NEURAL NET (DEFERRED)
        try:
            self._pulse_callback(90, "Wake-up AI Neural System...")
            pass
        except Exception as e:
             pass

        # 5. DATA ANALYTICS (DEFERRED)
        try:
            self._pulse_callback(95, "Calibrating Financial Models...")
            pass
        except: pass
        
        # 6. FINAL UI INTEGRATION (Ready to Show)
        self.is_page_loading = False
        # self.show_page("dashboard") # REMOVED: Do not show until authorized.
        
        self._pulse_callback(100, "Initialization Complete.")
        
        # Start Background tasks
        self.shown_dm_ids = set() 
        try:
            set_signal_callback(self.on_signal_detected)
        except: pass
        # self.after(500, self.start_pro_monitor) # Deferred to show_main_interface

        self._reveal_app()

    def _reveal_app(self):
        """Fade out splash and show main app window (GLITCH FREE)."""
        if hasattr(self, 'splash'):
            try:
                self.splash.close()
            except: pass
            del self.splash
        
        # KEY FIX: Force State FIRST, then Show.
        self.state('zoomed') 
        self.deiconify()
        self.lift()
        self.focus_force()
        
        # Set Privacy Initials
        self.after(1000, lambda: SettingsManager.load_privacy_settings(self))
        
        # --- INITIAL AUTH FLOW (Deferred for instant window draw) ---
        # First Check: Language Setup -> Then Auth
        self.after(100, lambda: self.check_language_setup())

    def on_closing(self):
        """Force Kill Application on Exit"""
        try:
            # Stop Queue Loop
            self.ui_queue = None 
            
            # Destroy Window
            self.destroy()
            
            # Force Kill Process (Zombie Killer)
            os._exit(0) 
        except:
            os._exit(0)
        
        # Check for updates in background (DISABLED per user request - moved to Settings)
        # self.after(3000, lambda: threading.Thread(target=self.check_for_updates, daemon=True).start())
    
    def _handle_oauth_callback(self, data):
        """Handle OAuth callback from browser deep link (PKCE code or direct tokens)"""
        try:
            print(f"// Deep Link Received: {data}")
            
            # PKCE Flow: Exchange code for session
            if data.get("code"):
                code = data["code"]
                print(f"// Attempting PKCE code exchange...")
                success, msg = self.db_manager.exchange_code_for_session(code)
                
                if success:
                    print(f"// OAuth Login Success via deep link!")
                    
                    # Stealth Referral Sync
                    if data.get("invite"):
                        print(f"// Syncing stealth referral: {data['invite']}")
                        self.affiliate_service.bind_referral_stealth(data["invite"])

                    # Skip to dashboard after successful login
                    self.after(100, lambda: setattr(self, '_oauth_login_success', True))
                else:
                    print(f"// OAuth Code Exchange Failed: {msg}")
            
            # Implicit Flow: Direct tokens
            elif data.get("access_token"):
                access_token = data["access_token"]
                refresh_token = data.get("refresh_token", "")
                print(f"// Setting session from implicit flow tokens...")
                # TODO: Implement set_session with provided tokens
                
        except Exception as e:
            print(f"// OAuth Callback Error: {e}")
    
    def on_google_login_success(self):
        """Called when Google OAuth login succeeds. Navigates to main UI."""
        print("[SUCCESS] on_google_login_success triggered - reloading UI")
        try:
            # Reload environment to pick up new auth tokens
            load_dotenv(override=True)
            
            # --- SYNC SESSION IMMEDIATELY ---
            if hasattr(self, 'db_manager'):
                self.db_manager.user_id = os.getenv("USER_ID", "anonymous")
                # Refresh names and pro status for UI labels
                self.check_pro_status()
            
            # Show success message
            CTkMessagebox(
                title=self.translator.get("popup_success_title"), 
                message="Google Login berhasil!", 
                icon="check"
            )
            
            # Navigate to main app UI
            self.after(500, self.show_main_interface)
            
        except Exception as e:
            print(f"[ERROR] on_google_login_success error: {e}")
            self.show_auth_error(str(e))
    
    def show_auth_error(self, error_msg):
        """Display authentication error to user."""
        print(f"[ERROR] show_auth_error: {error_msg}")
        CTkMessagebox(
            title="Login Gagal", 
            message=f"Error: {error_msg}", 
            icon="cancel"
        )
        # Re-enable buttons if they exist (Prevent stuck UI)
        try:
            if hasattr(self, 'auth_google_btn') and self.auth_google_btn.winfo_exists():
                self.auth_google_btn.configure(state="normal", text=self.translator.get("auth_google"))
            if hasattr(self, 'auth_submit_btn') and self.auth_submit_btn.winfo_exists():
                self.auth_submit_btn.configure(state="normal")
        except: pass



    def _process_queue_loop(self):
        """Processes the UI update queue every 100ms on the main thread."""
        try:
            # Check if alive
            try:
                if not self.winfo_exists(): return
            except: return

            while not self.ui_queue.empty():
                callback, args, kwargs = self.ui_queue.get_nowait()
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    # Filter out destruction errors
                    if "application has been destroyed" not in str(e):
                        print(f"// Queue Processing Error: {e}")
            
            # Re-schedule only if alive
            self.after(100, self._process_queue_loop)
        except:
            pass

    def safe_ui_update(self, callback, *args, **kwargs):
        """Thread-safe UI update. Pushes to queue for main thread processing."""
        self.ui_queue.put((callback, args, kwargs))

    def check_for_updates(self):
        """Checks cloud version and shows update prompt"""
        try:
            latest = self.db_manager.get_latest_version()
            if latest and latest != APP_VERSION:
                metadata = self.db_manager.get_app_metadata()
                msg = self.translator.get("popup_update_msg").format(
                    version=latest, 
                    changelog=metadata.get("changelog", "- Perbaikan Performa\n- Pembaruan UI") if metadata else "- Bug fixes"
                )
                
                # Use main thread for UI
                self.after(0, lambda: StartupView.show_update_prompt(self, msg, metadata, APP_VERSION))
        except Exception as e:
            print(f"// Update check failed: {e}")


    def check_pro_status(self):
        """Checks if the user has PRO status and updates global state (Async)"""
        def _task():
            try:
                if hasattr(self, 'db_manager') and self.db_manager:
                    is_pro = self.db_manager.is_pro_user()
                    # Update local state safely if needed
                    self.is_pro = is_pro
            except Exception as e:
                print(f"// Pro check warning: {e}")
        
        threading.Thread(target=_task, daemon=True).start()

    def _async_connect_mt5(self):
        """Connects to MT5 in a background thread to prevent Startup Freeze."""
        def _task():
            try:
                from modules.mt5.mt5_service import MT5Service
                service = MT5Service.instance()
                mt5_login = int(os.getenv("MT5_LOGIN", "0"))
                mt5_pass = os.getenv("MT5_PASSWORD", "")
                mt5_serv = os.getenv("MT5_SERVER", "")
                
                if mt5_login > 0:
                    # This call is BLOCKING (5-10s), so we are in a thread.
                    if service.initialize(login=mt5_login, password=mt5_pass, server=mt5_serv):
                        self.is_mt5_connected = True
                        self.safe_ui_update(lambda: self.log("SUCCESS", "MT5 Connected via Background Service"))
                    else:
                        err = service.last_error()
                        self.safe_ui_update(lambda: self.log("ERROR", f"MT5 Background Connect Failed: {err}"))
            except Exception as e:
                print(f"// MT5 Async Error: {e}")
        
        threading.Thread(target=_task, daemon=True).start()

    def check_language_setup(self):
        """Checks if language is configured, otherwise shows selector"""
        if os.getenv("LANGUAGE_CONFIGURED") == "True":
            self.check_initial_auth()
        else:
            self.show_language_view()

    def show_language_view(self):
        return StartupView.show_language_view(self)

    def show_auth_view(self, mode="login"):
        return AuthView.build(self, mode)

    def show_eula_view(self):
        return EULAView.build(self)
    def _set_lang_action(self, lang_code):
        """Saves language choice and proceeds"""
        # Update Runtime
        self.translator.set_language(lang_code)
        self.title(self.translator.get("app_title"))
        
        # Save to Env
        from dotenv import set_key
        set_key(".env", "APP_LANGUAGE", lang_code)
        set_key(".env", "LANGUAGE_CONFIGURED", "True")
        
        # Proceed
        AuthService.check_initial_auth(self)
        
    def clear_window(self):
        """Removes all widgets from the main window"""
        for widget in self.winfo_children():
            widget.destroy()
            
    def start_boot_handshake(self):
        """
        Luxury Enterprise Handshake Sequence.
        Steers the user through Cloud Sync, MT5 Detection, and Auto-Login.
        """
        from ui_theme import THEME_DARK
        self.clear_window()
        self.title(f"{self.translator.get('app_title')} - Handshake Protocol")
        
        # 1. Background
        bg = ctk.CTkFrame(self, fg_color=THEME_DARK["bg_primary"])
        bg.pack(fill="both", expand=True)
        
        # 2. Handshake Card
        card = ctk.CTkFrame(bg, fg_color=THEME_DARK["bg_secondary"], width=450, height=520, corner_radius=20)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        # Logo/Header
        # Logo/Header
        # Title with Premium Font
        ctk.CTkLabel(card, text="ITC + SkyNET AI", font=("Poppins", 32, "bold"), text_color="#fbbf24").pack(pady=(50, 8))
        # Subtitle - Keep original but premium styling
        subtitle = ctk.CTkLabel(card, text="RAG AGENTIC INSTITUTION TERMINAL", 
                                font=("Poppins", 11, "normal"), 
                                text_color="#6e7681")  # Softer gray
        subtitle.pack(pady=(0, 35))
        
        # Stepper Container
        stepper_frame = ctk.CTkFrame(card, fg_color="transparent")
        stepper_frame.pack(fill="x", padx=40)
        
        steps = [
            ("CLOUD", "Synchronizing Profile..."),
            ("MT5", "Detecting Terminal..."),
            ("AUTH", "Security Auto-Login..."),
            ("PULSE", "Verifying Connection...")
        ]
        
        step_labels = []
        for i, (tag, text) in enumerate(steps):
             f = ctk.CTkFrame(stepper_frame, fg_color="transparent")
             f.pack(fill="x", pady=12)
             
             # Status Icon (Premium Checkmark/Dot)
             dot = ctk.CTkLabel(f, text="○", font=("Poppins", 20), text_color="#30363d", width=24) # Empty circle pending
             dot.pack(side="left", padx=(0, 18))
             
             # Text with Premium Font
             lbl = ctk.CTkLabel(f, text=text, font=("Poppins", 13, "normal"), text_color="#8b949e")
             lbl.pack(side="left")
             
             step_labels.append((dot, lbl))

        # Progress Bar with Glow Effect (Luxury)
        p_bar = ctk.CTkProgressBar(card, orientation="horizontal", height=6, 
                                   fg_color="#21262d",  # Darker background
                                   progress_color="#fbbf24",  # Gold color
                                   corner_radius=3)
        p_bar.pack(fill="x", padx=50, pady=(45, 0))
        p_bar.set(0)
        
        # Status Message - Premium Font
        status_msg = ctk.CTkLabel(card, text="Establishing Secure Link...", 
                                  font=("Poppins", 10, "normal"), 
                                  text_color="#6e7681")
        status_msg.pack(pady=(18, 0))

        # Handshake Logic
        def _execute_handshake():
            import time
            from modules.mt5.mt5_service import MT5Service
            service = MT5Service.instance()
            
            try:
                # STEP 1: CLOUD SYNC (Animated)
                self.after(0, lambda: step_labels[0][1].configure(text_color="#e6edf3"))
                self.after(0, lambda: step_labels[0][0].configure(text="●", text_color="#fbbf24"))  # Filled dot = active
                p_bar.set(0.1)
                
                if hasattr(self, 'db_manager'):
                    self.db_manager._clear_mt5_credentials()
                    self.db_manager.pull_user_config()
                
                time.sleep(1.2) # Elegant Delay
                self.after(0, lambda: step_labels[0][0].configure(text="✓", text_color="#3fb950"))  # Green checkmark
                p_bar.set(0.25)
                
                # STEP 2: MT5 DETECTION (Animated)
                self.after(0, lambda: step_labels[1][1].configure(text_color="#e6edf3"))
                self.after(0, lambda: step_labels[1][0].configure(text="●", text_color="#fbbf24"))  # Filled dot = active
                p_bar.set(0.35)
                
                # Check if MT5 is running via terminal_info (PASSIVE DETECTION)
                info = service.get_terminal_info(passive=True)
                # Note: We do NOT force init here to avoid premature launch
                
                time.sleep(1.0)
                self.after(0, lambda: step_labels[1][0].configure(text="✓", text_color="#3fb950"))  # Green checkmark
                p_bar.set(0.5)

                # STEP 3: AUTO-LOGIN (Animated)
                self.after(0, lambda: step_labels[2][1].configure(text_color="#e6edf3"))
                self.after(0, lambda: step_labels[2][0].configure(text="●", text_color="#fbbf24"))  # Filled dot = active
                
                login_str = os.getenv("MT5_LOGIN", "0").strip()
                mt5_login = int(login_str) if login_str.isdigit() else 0
                
                if mt5_login > 0:
                    connected = service.initialize(
                        login=mt5_login,
                        password=os.getenv("MT5_PASSWORD", ""),
                        server=os.getenv("MT5_SERVER", ""),
                        allow_launch=True  # ACTIVE LAUNCH: Connect now that we have cloud data
                    )
                    self.is_mt5_connected = connected
                else:
                    service.shutdown()
                    self.is_mt5_connected = False
                
                time.sleep(1.5)
                self.after(0, lambda: step_labels[2][0].configure(text="✓", text_color="#3fb950"))  # Green checkmark
                p_bar.set(0.75)

                # STEP 4: VERIFY (Animated)
                self.after(0, lambda: step_labels[3][1].configure(text_color="#e6edf3"))
                self.after(0, lambda: step_labels[3][0].configure(text="●", text_color="#fbbf24"))  # Filled dot = active
                
                # Wait for Pulse
                retries = 5
                while retries > 0:
                    acc = service.get_account_info()
                    if acc: break
                    time.sleep(1)
                    retries -= 1
                
                self.after(0, lambda: step_labels[3][0].configure(text_color="#3fb950", text="✔"))
                p_bar.set(1.0)
                self.after(0, lambda: status_msg.configure(text="PROTOCOL OPTIMIZED - ACCESS GRANTED", text_color="#3fb950"))
                
                time.sleep(1.0)
                self.after(0, self.show_main_interface)
                
            except Exception as e:
                print(f"// Handshake Error: {e}")
                self.after(0, lambda: status_msg.configure(text=f"PROTOCOL ERROR: {e}", text_color="#f85149"))
                time.sleep(3)
                self.after(0, self.show_main_interface)

        threading.Thread(target=_execute_handshake, daemon=True).start()

    def show_main_interface(self):
        """Builds the main application layout. ONLY call after Handshake success."""
        try:
            self.clear_window()
            # Force window to be visible if hidden
            self.deiconify()
            self.state("zoomed") # KEEP ZOOMED
            
            # --- BUILD LAYOUT ---
            self._create_topbar()
            self._create_sidebar()
            self._create_main_area()
            
            # Show dashboard by default
            self.show_page("dashboard")
            
            # Start background tasks (deferred to ensure class fully loaded)
            self.after(100, lambda: self.start_connectivity_monitor())
            self.after(2000, lambda: self.start_pro_monitor())
        except Exception as e:
            self.log("ERROR", f"Failed to load main interface: {e}")
            CTkMessagebox(title="Critical Error", message=f"Application crashed during load: {e}", icon="cancel")


        
    def get_theme_data(self):
        """Dynamic helper to get the current theme dictionary"""
        if self.selected_theme in ["light", "neutral"]:
            from ui_theme_modern import get_theme as get_modern_theme
            return get_modern_theme(self.selected_theme)
        return THEME_DARK

    def check_initial_auth(self):
        return AuthService.check_initial_auth(self)

    def restart_application(self):
        """Restarts the current application process"""
        import sys
        import subprocess
        try:
            self.destroy()
            # Relaunch the application
            subprocess.Popen([sys.executable, "src/gui.py"], cwd=os.getcwd())
            sys.exit(0)
        except Exception as e:
            print(f"Failed to restart: {e}")

    def change_theme(self, new_theme_flag):
        """Theme Switcher: Updates config and auto-restarts for clean state"""
        try:
            self.selected_theme = new_theme_flag
            
            # 1. Update .env
            set_key(".env", "UI_THEME", new_theme_flag)
            os.environ["UI_THEME"] = new_theme_flag
            
            # 2. Show brief loading feedback before restart
            self.log("INFO", f"🎨 Applying theme: {new_theme_flag}...")
            
            # 3. Auto-Restart (Solves Freezing/Stuck Issue)
            # We use after() to let the UI update one last time
            self.after(500, self.restart_application)
            
        except Exception as e:
            self.log("ERROR", f"Failed to switch theme: {e}")

    def change_language(self, new_lang_code):
        """Language Switcher: Updates config and auto-restarts"""
        try:
            # 1. Update .env
            set_key(".env", "APP_LANGUAGE", new_lang_code)
            set_key(".env", "LANGUAGE_CONFIGURED", "True")
            os.environ["APP_LANGUAGE"] = new_lang_code
            
            # 2. Show brief loading feedback before restart
            self.log("INFO", f"🌐 Switching language to: {new_lang_code}...")
            
            # 3. Auto-Restart
            self.after(500, self.restart_application)
            
        except Exception as e:
            self.log("ERROR", f"Failed to switch language: {e}")
    
    # ========================================
    # TOP BAR
    # ========================================
    def _create_topbar(self):
        # Use modern navigation panel if modern theme is selected
        if self.selected_theme in ["light", "neutral", "dark_modern"]:
            self.topbar = ModernNavigationPanel.create_topbar(self)
        else:
            self.topbar = NavigationPanel.create_topbar(self)

    def _create_badge(self, parent, text, color):
        # Use modern badge if modern theme is selected
        if self.selected_theme in ["light", "neutral", "dark_modern"]:
            return ModernNavigationPanel._create_status_badge(self, parent, text, color, get_modern_theme("dark" if self.selected_theme == "dark_modern" else self.selected_theme))
        else:
            return NavigationPanel._create_badge(self, parent, text, color)

    def _create_sidebar(self):
        """
        Creates the sidebar using ModernNavigationPanel for ALL themes 
        to ensure menu consistency (22-Items Strict).
        """
        # UNIVERSAL SIDEBAR: Always use the Modern 22-Item Panel
        from modules.ui.navigation_panel_modern import ModernNavigationPanel
        
        # Correctly call create_sidebar (it returns the sidebar frame)
        self.sidebar = ModernNavigationPanel.create_sidebar(self)
    
    # ========================================
    # MAIN CONTENT AREA
    # ========================================
    def _create_main_area(self):
        modern_theme_bg = get_modern_theme("dark" if self.selected_theme == "dark_modern" else self.selected_theme)["bg_primary"] if self.selected_theme in ["light", "neutral", "dark_modern"] else THEME["bg_primary"]
        self.main_container = ctk.CTkFrame(self, fg_color=modern_theme_bg, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, side="right")

        # LAZY LOADING ARCHITECTURE (v22-Items Optimized)
        # Only initialize Dashboard at startup. Others are built on-demand.
        self.pages = {}
        
        # Real-time tracking for the first build
        def cb(p, t):
            if hasattr(self, 'splash') and self.splash:
                self.splash.update_progress(p, t)
                self.update() # CRITICAL: Prevents freeze during heavy render
        
        self.pages["dashboard"] = DashboardView.build(self, progress_callback=cb)
        
        # Placeholder for lazy loading status
        self.is_page_loading = False
        
    # --- PRO STATUS LOGIC ---
    def start_pro_monitor(self):
        """Background thread to check Pro status updates in real-time"""
        def _task():
            # Initial check
            if hasattr(self, 'db_manager') and self.db_manager:
                self._fetch_pro_data()
                while True:
                    import time
                    time.sleep(60)
                    if hasattr(self, 'db_manager') and self.db_manager:
                        self._fetch_pro_data()
        import threading
        threading.Thread(target=_task, daemon=True).start()

    def _fetch_pro_data(self):
        """Helper to fetch and apply pro status"""
        if self.db_manager.is_admin():
            self.is_pro = True
            self.is_vip = True
            self.safe_ui_update(self._update_premium_locks)
            return

        try:
            res = self.db_manager.client.table("user_profiles").select("is_pro,is_vip,premium_until").eq("hwid", self.db_manager.user_id).execute()
            if res.data:
                data = res.data[0]
                perm_pro = data.get('is_pro', False)
                perm_vip = data.get('is_vip', False)
                
                # Check Temporal Boost
                until_str = data.get("premium_until")
                is_boosted = False
                if until_str:
                    try:
                        from datetime import datetime
                        expiry = datetime.fromisoformat(until_str.replace('Z', '+00:00'))
                        is_boosted = datetime.now().astimezone() < expiry
                    except: pass
                
                self.is_pro = perm_pro or is_boosted
                self.is_vip = perm_vip or is_boosted # Boost usually covers both for MVP
                self.safe_ui_update(self._update_premium_locks)
        except: pass

    def _update_premium_locks(self):
        """Update UI based on PRO/VIP status"""
        # Unlock PRO (AI)
        if self.is_pro or self.is_vip:
            if hasattr(self, 'ai_pro_overlay'): self.ai_pro_overlay.place_forget()
            if hasattr(self, 'ai_input'):
                self.ai_input.configure(state="normal")
                self.ai_send_btn.configure(state="normal")
        
        # Unlock VIP (Already handled via overlay in SPCView but we can add badge)
        if self.is_vip:
            pass # Badge could be added to sidebar
    
    def show_page(self, page_id, sub_tab=None):
        """
        Master Navigation Handler (Instant-Snap Architecture).
        Switches between pre-rendered pages with 0ms delay.
        """
        # --- RESTRICTION: INTELLIGENCE TERMINAL ---
        # (MOVED TO INTERNAL PAGE LOCK SCREEN)      
        # ------------------------------------------
        # 1. Hide all existing pages (Memory Resident)
        for pid, page in self.pages.items():
            if page and hasattr(page, 'pack_forget'):
                page.pack_forget()
        
        # 2. Clear clean container (Safety)
        for child in self.main_container.winfo_children():
            child.pack_forget()

        # --- POPUP INTERCEPTS ---
        if page_id == "changelog":
            from modules.ui.changelog_viewer import ChangelogViewer
            ChangelogViewer.show(self)
            return

        if page_id == "inspector":
             dialog = ctk.CTkInputDialog(text="Enter User HWID to Inspect:", title="Inspector Panel")
             hwid = dialog.get_input()
             if hwid:
                 from modules.ui.inspector_panel import UserInspectorPanel
                 UserInspectorPanel(self, self.db_manager, hwid)
             return

        # --- INSTANT SNAP & LAZY LOAD HYBRID ---
        # If page exists in memory, show it instantly
        if page_id not in self.pages or self.pages[page_id] is None:
            self.is_page_loading = True
            
            # Show a temporary loading indicator if it's a cold boot for this module
            self.log("INFO", f"❄ Cold Booting Module: {page_id}...")
            
            try:
                # Core Modules (Pre-Rendered during Splash usually)
                if page_id == "dashboard": 
                    cb = lambda p, t: self.splash.update_progress(p, t) if hasattr(self, 'splash') else None
                    self.pages["dashboard"] = DashboardView.build(self, progress_callback=cb)
                elif page_id == "signals": 
                    from modules.ui.marketplace_view import MarketplaceView
                    self.pages["signals"] = MarketplaceView.build(self)
                elif page_id == "ai": self.pages["ai"] = self._build_ai_page()
                elif page_id == "analysis": self.pages["analysis"] = self._build_analysis_page()
                elif page_id == "news": self.pages["news"] = NewsView.build(self)
                
                # Standard Modules
                elif page_id == "telegram": self.pages["telegram"] = self._build_telegram_page()
                elif page_id == "mt5": self.pages["mt5"] = self._build_mt5_page()
                elif page_id == "trading": self.pages["trading"] = self._build_trading_page()
                elif page_id == "risk": self.pages["risk"] = self._build_risk_page()
                elif page_id == "spc":
                    if hasattr(self, '_build_spc_page'): self.pages["spc"] = self._build_spc_page()
                    else: 
                        from modules.ui.spc_hub_view import SPCHubView
                        self.pages["spc"] = SPCHubView.build(self)
                elif page_id == "logs": self.pages["logs"] = self._build_logs_page()
                elif page_id == "leaderboard": self.pages["leaderboard"] = self._build_leaderboard_page()
                elif page_id == "broker": 
                    from modules.ui.broker_view import BrokerView
                    self.pages["broker"] = BrokerView.build(self)
                elif page_id == "vps":
                    from modules.ui.vps_view import VPSView
                    self.pages["vps"] = VPSView.build(self)
                elif page_id == "other_partners":
                    from modules.ui.other_partners_view import OtherPartnersView
                    self.pages["other_partners"] = OtherPartnersView.build(self)
                elif page_id == "roadmap":
                    from modules.ui.roadmap_view import RoadmapView
                    self.pages["roadmap"] = RoadmapView.build(self)
                elif page_id == "education": self.pages["education"] = self._build_education_page()
                elif page_id == "settings": 
                    if hasattr(self, '_build_settings_page'): self.pages["settings"] = self._build_settings_page()
                    else:
                        from modules.ui.settings_view import SettingsView
                        self.pages["settings"] = SettingsView.build(self)
                elif page_id == "journal": 
                    if hasattr(self, '_build_journal_page'): self.pages["journal"] = self._build_journal_page()
                    else:
                        from modules.ui.journal_view import JournalView
                        self.pages["journal"] = JournalView.build(self)
                elif page_id == "subscription":
                    from modules.ui.subscription_view import SubscriptionView
                    self.pages["subscription"] = SubscriptionView.build(self)
                elif page_id == "donation": self.pages["donation"] = DonationView.build(self)
                elif page_id == "merchant":
                    from modules.ui.merchant_dashboard_view import MerchantDashboardView
                    self.pages["merchant"] = MerchantDashboardView(self.main_container, self)
                elif page_id == "marketing_vault":
                    from modules.ui.marketing_vault_view import MarketingVaultView
                    self.pages["marketing_vault"] = MarketingVaultView(self.main_container, self)
                elif page_id == "admin":
                    if hasattr(self, 'db_manager') and self.db_manager.is_admin():
                        from modules.ui.admin_view import AdminView
                        self.pages["admin"] = AdminView.build(self)
                        self.refresh_admin_stats()
            except Exception as e:
                print(f"// Module Load Error [{page_id}]: {e}")
                self.log("ERROR", f"Failed to load {page_id}: {e}")
            finally:
                self.is_page_loading = False

        # --- SPECIAL REBUILDS (Dynamic Content) ---
        # REMOVED: Redundant subscription rebuild logic that caused double-init and potential errors.
        # The page is already built in the main block above.


        # Handle sub-tabs logic
        if sub_tab:
            if page_id == "signals" and hasattr(self.pages.get("signals"), "market_tabs"):
                try: self.pages["signals"].market_tabs.set(sub_tab)
                except: pass

        # 3. REVEAL PAGE (Instant Pack)
        if page_id in self.pages and self.pages[page_id]:
            # Use pack to fill the container immediately
            self.pages[page_id].pack(fill="both", expand=True, padx=20, pady=15)
        
        # 4. HIGHLIGHT SIDEBAR
        for pid, btn in self.menu_buttons.items():
            if pid == page_id:
                if isinstance(btn, ctk.CTkFrame):
                    btn.configure(fg_color=THEME["bg_tertiary"])
                    if hasattr(btn, 'icon_lbl'): btn.icon_lbl.configure(text_color="white")
                    if hasattr(btn, 'text_lbl'): btn.text_lbl.configure(text_color="white")
                else:
                    btn.configure(fg_color=THEME["bg_tertiary"], text_color="white")
            else:
                if isinstance(btn, ctk.CTkFrame):
                    btn.configure(fg_color="transparent")
                    # Revert to theme defaults
                    default_icon_color = THEME["text_primary"]
                    default_text_color = THEME["text_secondary"]
                    if hasattr(btn, 'icon_lbl'): btn.icon_lbl.configure(text_color=default_icon_color)
                    if hasattr(btn, 'text_lbl'): btn.text_lbl.configure(text_color=default_text_color)
                else:
                    btn.configure(fg_color="transparent", text_color=THEME["text_secondary"])
        
        self.current_page = page_id
        
        # Auto-Focus optimizations
        if page_id == "ai" and hasattr(self, 'ai_input'):
            self.after(200, lambda: self.ai_input.focus_set())
    
    # ========================================
    # DASHBOARD PAGE
    # ========================================
    def _build_dashboard_page(self):
        return DashboardView.build(self)
    
    
    # ========================================
    # TELEGRAM PAGE
    # ========================================
    def _build_telegram_page(self):
        return TelegramView.build(self)
    
    # ========================================
    # MT5 PAGE
    # ========================================
    def _build_mt5_page(self):
        return MT5View.build(self)
    
    # ========================================
    # TRADING RULES PAGE (Two Column)
    # ========================================
    def _build_trading_page(self):
        return TradingView.build(self)
    
    # ========================================
    # RISK PAGE
    # ========================================
    def _build_risk_page(self):
        return RiskView.build(self)
    
    
    def toggle_password(self):
        if self.show_pass.get():
            self.entry_mt5_pass.configure(show="")
        else:
            self.entry_mt5_pass.configure(show="*")
    
    def test_telegram(self):
        return CopierController.test_telegram(self)
    
    def test_mt5(self):
        return CopierController.test_mt5(self)
    
    # ========================================
    # AI PAGE
    # ========================================
    def _build_ai_page(self):
        return AIView.build(self)

    def _show_locked_overlay(self):
        return AIView.show_locked_overlay(self)
    
    # ========================================
    # SIGNAL ANALYSIS PAGE
    # ========================================
    def _build_analysis_page(self):
        return AnalysisView.build(self)

    def _build_logs_page(self):
        return LogsView.build(self)

    def _build_leaderboard_page(self):
        return LeaderboardView.build(self)

    def refresh_leaderboards(self):
        return LeaderboardView.refresh_leaderboards(self)

    def refresh_signals(self):
        return MarketplaceView.refresh_signals(self)

    def refresh_admin_stats(self):
        return AdminView.refresh_admin_stats(self)

    def show_changelog(self):
        return self.show_page("journal")


    def _build_education_page(self):
        return EducationView.build(self)

    def start_quiz(self):
        return EducationView.start_quiz(self)

    def reset_education_view(self):
        return EducationView.reset_education_view(self)

    def _start_async_quiz(self):
        return EducationView.generate_quiz_thread(self)

    def log(self, level, message):
        """Displays a timestamped log message in the UI log box"""
        color = {"ERROR": "🔴", "INFO": "🟢", "WARN": "🟡", "SUCCESS": "✅"}.get(level, "⚪")
        if hasattr(self, "log_box") and self.log_box.winfo_exists():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", f"{color} {level}    {message}\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        else:
            print(f"[{level}] {message}")
        
        # Cloud Log Sync
        if hasattr(self, "db_manager") and self.db_manager:
            threading.Thread(target=lambda: self.db_manager.push_log(level, message), daemon=True).start()

    def clear_logs(self):
        """Clears the UI log box"""
        if hasattr(self, "log_box") and self.log_box.winfo_exists():
            self.log_box.configure(state="normal")
            self.log_box.delete("0.0", "end")
            self.log_box.configure(state="disabled")

    def export_logs(self):
        """Saves current session logs to a file"""
        try:
            if not hasattr(self, "log_box") or not self.log_box.winfo_exists(): return
            logs = self.log_box.get("0.0", "end")
            with open("logs.txt", "w", encoding="utf-8") as f:
                f.write(logs)
            self.log("INFO", "✅ Logs exported to logs.txt")
            os.startfile("logs.txt")
        except Exception as e:
            self.log("ERROR", f"Export failed: {e}")


    # ========================================
    # MONITORING & UI UPDATES
    # ========================================
    def start_connectivity_monitor(self):
        """Starts the background UI update loop"""
        threading.Thread(target=self.update_ui_loop, daemon=True).start()

    def show_recap(self, session_data):
        """Displays the session summary popup (ShareRecapView)"""
        try:
            from modules.ui.share_recap_view import ShareRecapView
            ShareRecapView(self, session_data)
        except Exception as e:
            print(f"// Recap Popup Error: {e}")

    def update_ui_loop(self):
        """Periodic UI updates for status and guide"""
        from index import check_internet, get_mt5_status, get_account_meta
        while True:
            try:
                # 1. Internet Check
                is_online = check_internet()
                
                # 2. MT5 Status
                mt5_ok = get_mt5_status()
                
                # 3. Update Dashboard Logic
                if hasattr(self, 'current_page') and self.current_page == "dashboard":
                    # Guide Step 1: Telegram
                    tg_ok = False
                    if hasattr(self, 'entry_api_id') and self.entry_api_id.get().strip():
                        tg_ok = True
                    
                    # Guide Step 3: Mode
                    mode_text = "MANUAL"
                    mode_color = "#f85149" # Red
                    if hasattr(self, 'chk_auto_exec') and self.chk_auto_exec.get():
                        if hasattr(self, 'ai_enabled') and self.ai_enabled.get():
                            mode_text = "AI-AUTO"
                            mode_color = "#3fb950" # Green
                        else:
                            mode_text = "DIRECT"
                            mode_color = "#d29922" # Orange
                    
                    # Guide Step 4: Copier
                    copier_text = "STOPPED"
                    copier_color = "#f85149"
                    if getattr(self, "copier_running", False):
                        copier_text = "RUNNING"
                        copier_color = "#3fb950"

                    # UI Updates (Main Thread)
                    def _update():
                        # Status Cards (Legacy)
                        if hasattr(self, 'status_internet'):
                            color = "#3fb950" if is_online else "#f85149"
                            text = "Online" if is_online else "Offline"
                            self.status_internet.configure(text=f"● {text}", text_color=color)
                            
                        # Quick Guide Updates
                        if hasattr(self, 'lbl_guide_s1'):
                            color = "#3fb950" if tg_ok else "#f85149"
                            self.lbl_guide_s1.configure(text_color=color)
                        
                        if hasattr(self, 'lbl_guide_s2'):
                            color = "#3fb950" if mt5_ok else "#f85149"
                            self.lbl_guide_s2.configure(text_color=color)
                            
                        if hasattr(self, 'lbl_guide_s3'):
                            self.lbl_guide_s3.configure(text=f"3. {mode_text}", text_color=mode_color)
                            
                        if hasattr(self, 'lbl_guide_s4'):
                            self.lbl_guide_s4.configure(text=f"4. {copier_text}", text_color=copier_color)
                            
                        # Account Meta
                        if mt5_ok:
                            meta = get_account_meta()
                            if hasattr(self, 'card_balance'): self.card_balance.configure(text=f"${meta['balance']:,.2f}")
                            if hasattr(self, 'card_equity'): self.card_equity.configure(text=f"${meta['equity']:,.2f}")
                            
                            pl_color = "#3fb950" if meta['profit'] >= 0 else "#f85149"
                            if hasattr(self, 'card_pnl'): self.card_pnl.configure(text=f"${meta['profit']:,.2f}", text_color=pl_color)
                            
                            hist_color = "#3fb950" if meta['total_pl'] >= 0 else "#f85149"
                            if hasattr(self, 'card_loss'): self.card_loss.configure(text=f"${meta['total_pl']:,.2f}", text_color=hist_color)

                    if hasattr(self, 'safe_ui_update'):
                        self.safe_ui_update(_update)
                    else:
                        try:
                            if self.winfo_exists():
                                self.after(0, _update)
                        except:
                            pass
            except Exception as e:
                print(f"// Monitor Error: {e}")
            
            time.sleep(3)


    def send_ai_message(self, force_search=False, prompt_override=None):
        """Handles AI Chat Input with Trial Limit Check"""
        try:
            # Determine message source
            if prompt_override:
                user_msg = prompt_override
            else:
                if not hasattr(self, 'ai_input') or not self.ai_input.get().strip(): return
                user_msg = self.ai_input.get().strip()
            
            # 1. Check Usage vs Limit
            # Only apply limit if User is NOT providing their own Key AND not Pro
            using_default_key = not os.getenv("AI_API_KEY") # If empty, using fallback
            
            if using_default_key and not self.is_pro:
                usage = self.db_manager.get_ai_message_count()
                limit = self.db_manager.get_total_ai_limit()
                
                if usage >= limit:
                    AIView.show_locked_overlay(self)
                    return

            # 2. Clear & Send
            if not prompt_override:
                self.ai_input.delete(0, 'end')
            
            # Use Bubble UI
            AIView.add_chat_bubble(self, user_msg, is_user=True)
            
            # Insert Loading Bubble (Placeholder)
            # We'll let AIManager handle the "Thinking" state via a temporary bubble or status
            self.ai_thinking = True
            threading.Thread(target=lambda: AIManager.animate_thinking(self), daemon=True).start()
            
            # Disable Input to prevent spam
            if hasattr(self, 'ai_input'):
                self.ai_input.configure(state="disabled")
            
            user_name = os.getenv("USER_NAME", "Trader")
            
            # Start AI Thread
            threading.Thread(target=lambda: AIManager.get_ai_response(self, user_msg, user_name, force_search=force_search), daemon=True).start()
            
            # --- AI TRACKING (ADMIN) ---
            if hasattr(self, 'db_manager'):
                 threading.Thread(target=self.db_manager.track_ai_usage, daemon=True).start()
            
        except Exception as e:
            self.log("ERROR", f"AI Chat Error: {e}")

    def add_chat_bubble(self, text, is_user=False, is_thinking=False):
        """Wrapper for AIView Bubble"""
        return AIView.add_chat_bubble(self, text, is_user, is_thinking)

    def _start_async_quiz(self):
        """Launches the quiz generation in a background thread"""
        threading.Thread(target=lambda: EducationView.generate_quiz_thread(self), daemon=True).start()

    def save_config(self):
        return ConfigAggregator.save_config(self)

    def logout(self):
        return AuthService.logout(self)
        
    def show_quota_warning(self, provider="Groq"):
        return AppController.show_quota_warning(self, provider)
    
    def show_donation_info(self):
        """Redirect to the dedicated subscription/upgrade page"""
        self.show_page("subscription")

    def show_admin_broadcast(self, msg_data):
        """Wrapper to call Admin Broadcast logic"""
        return AppController.show_admin_broadcast(self, msg_data)

    # --- CALLBACKS ---
    def start_connectivity_monitor(self):
        """Delegates connectivity monitoring to AppController"""
        return AppController.start_connectivity_monitor(self)

    def on_signal_detected(self, signal):
        """Delegates signal handling to TradingController"""
        return TradingController.on_signal_detected(self, signal)

    # --- RESTORED TRADING & UTILITY WIRING ---
    def start_copier(self):
        return CopierController.start_copier(self)

    def run_telegram(self):
        return CopierController.run_telegram(self)

    def emergency_close(self):
        return CopierController.emergency_close(self)

    def test_mt5(self):
        return CopierController.test_mt5(self)

    def test_telegram(self):
        return CopierController.test_telegram(self)

    def toggle_copier(self, from_shortcut=False):
        """
        Toggles the copier state. 
        If from_shortcut=True (e.g. from Telegram view), it ensures we only START, 
        never stop. If already running, just go to Dashboard.
        """
        is_running = getattr(self, "copier_running", False)
        
        if from_shortcut:
            # Shortcut Logic: Only Start, never Stop.
            if is_running:
                # Already running? Just show dashboard.
                self.show_page("dashboard")
                self.log("INFO", "ℹ️ Copier is already running.")
            else:
                # Not running? Start it, then switch to dashboard.
                CopierController.start_copier(self)
                self.show_page("dashboard")
        else:
            # Normal Toggle (Dashboard Button)
            CopierController.start_copier(self)

    def toggle_password(self):
        """Toggles password visibility for MT5 and API Hash"""
        try:
            # Determine state from BooleanVar if exists, else toggle based on entry
            should_show = True
            if hasattr(self, 'show_pass'):
                should_show = self.show_pass.get()
            
            char = "" if should_show else "*"
            
            if hasattr(self, 'entry_mt5_pass'):
                self.entry_mt5_pass.configure(show=char)
            if hasattr(self, 'entry_api_hash'):
                self.entry_api_hash.configure(show=char)
        except: pass



    # ========================================
    # AUTH VIEW (SINGLE WINDOW - REDESIGNED)
    # ========================================
    
    # ========================================
    # EULA VIEW (SINGLE WINDOW)
    # ========================================
    
    def open_history(self):
        return CopierController.open_history(self)
    
    def open_tutorial(self):
        return TutorialView.show(self)

    def _get_changelog_versions(self):
        """Returns the changelog data structure"""
        return CHANGELOG_DATA
    def _update_sltp_preview(self, *args):
        try:
            return TradingView.update_sltp_preview(self, *args)
        except Exception as e:
            print(f"// SL/TP Preview Error: {e}")
    



if __name__ == "__main__":
    app = STCApp()
    app.mainloop()
