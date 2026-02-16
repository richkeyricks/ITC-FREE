import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS

# --- THEME ---
# REMOVED STATIC THEME

class LogsView:
    """
    Modular class for the Full Logs page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Logs page and attaches it to the parent (App/GUI)."""
        # Dynamic Theme Injection
        theme = parent.get_theme_data() if hasattr(parent, 'get_theme_data') else THEME_DARK

        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        ctk.CTkLabel(page, text=parent.translator.get("menu_logs"), font=("Segoe UI Semibold", 22), 
                     text_color="white", anchor="w").pack(fill="x", pady=(0, 15))
        
        # Buttons
        btn_row = ctk.CTkFrame(page, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(btn_row, text=parent.translator.get("logs_history"), font=FONTS["button"],
                      fg_color=theme["bg_secondary"], hover_color=theme["border_default"],
                      command=parent.open_history).pack(side="left", padx=(0, 10))
                      
        ctk.CTkButton(btn_row, text=parent.translator.get("logs_clear"), font=FONTS["button"],
                      fg_color=theme["bg_secondary"], hover_color=theme["border_default"],
                      command=parent.clear_logs).pack(side="left")
        
        # Copy Log Button (NEW FEATURE)
        def copy_log_to_clipboard():
            """Copy all log content to clipboard"""
            try:
                log_content = parent.full_log.get("1.0", "end-1c")
                parent.clipboard_clear()
                parent.clipboard_append(log_content)
                parent.update()  # Required for clipboard to work
                
                # Show success notification
                if hasattr(parent, 'show_toast'):
                    parent.show_toast("✅ Log copied to clipboard!", duration=2000)
                else:
                    print("// Copy Log: Success - Copied to clipboard")
            except Exception as e:
                print(f"// Copy Log Error: {e}")
                if hasattr(parent, 'show_toast'):
                    parent.show_toast(f"❌ Failed to copy log: {str(e)}", duration=3000)
        
        ctk.CTkButton(btn_row, text=parent.translator.get("logs_copy"), font=FONTS["button"],
                      fg_color="#fbbf24", hover_color="#f59e0b", text_color="#000000",
                      command=copy_log_to_clipboard).pack(side="left", padx=(10, 0))
        
        parent.full_log = ctk.CTkTextbox(page, font=FONTS["log"], fg_color=theme["bg_secondary"], corner_radius=8)
        parent.full_log.pack(fill="both", expand=True)
        
        return page
