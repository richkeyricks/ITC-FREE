
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
try:
    import customtkinter as ctk
    
    # Mock Parent
    class MockParent:
        def __init__(self):
            self.selected_theme = "modern_dark"
            self.menu_buttons = {}
            self.translator = self
        def get(self, k): return k
        def show_page(self, p): pass
        def show_donation_info(self): pass
        def logout(self): pass

    print("DEBUG: Importing ModernNavigationPanel...")
    from src.modules.ui.navigation_panel_modern import ModernNavigationPanel
    
    app = ctk.CTk()
    
    # Attach mock attributes to app
    app.selected_theme = "modern_dark"
    app.menu_buttons = {}
    app.translator = MockParent() # use the mock class as translator provider
    app.show_page = lambda p: None
    app.show_donation_info = lambda: None
    app.logout = lambda: None
    
    # Add dummy db_manager
    app.db_manager = lambda: None
    app.db_manager.is_admin = lambda: True
    
    print("DEBUG: Importing DashboardView...")
    from src.modules.ui.dashboard_view import DashboardView
    
    app.main_container = ctk.CTkFrame(app) # Mock main container
    
    # Mock translator.get_vps
    app.translator.get_vps = lambda: [{"name": "VPS1", "reason": "Test", "url": "#"}]
    app.translator.get = lambda k: k
    
    # Mock Theme Data
    app.theme_data = {
        "bg_secondary": "gray", "accent_primary": "blue", "text_primary": "white", 
        "text_secondary": "gray", "accent_success": "green", "bg_tertiary": "darkgray",
        "card_bg": "black", "card_border": "white", "status_error": "red", "text_disabled": "gray",
        "btn_primary_bg": "blue", "btn_primary_hover": "darkblue", "btn_premium_bg": "gold",
        "btn_premium_hover": "darkgold", "btn_danger_bg": "red", "btn_danger_hover": "darkred",
        "bg_primary": "black", "accent_secondary": "purple", "sidebar_hover_bg": "gray"
    }
    
    # Mock Card helpers if needed?
    # DashboardView uses internal static methods.
    
    print("DEBUG: Creating Dashboard...")
    DashboardView.build(app)
    print("DEBUG: Dashboard Success!")
    
except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
