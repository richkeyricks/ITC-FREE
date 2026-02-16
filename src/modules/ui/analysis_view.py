from ui_theme import THEME_DARK, FONTS as LEGACY_FONTS
from ui_theme_modern import get_theme as get_modern_theme, FONTS as MODERN_FONTS

# --- HELPER ---
def get_current_theme_data(parent):
    if hasattr(parent, 'selected_theme') and parent.selected_theme in ["light", "neutral"]:
        return get_modern_theme(parent.selected_theme), MODERN_FONTS
    return THEME_DARK, LEGACY_FONTS

class AnalysisView:
    """
    Modular class for the AI Analysis page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Analysis page and attaches it to the parent (App/GUI)."""
        import customtkinter as ctk # Ensure ctk is available
        theme, fonts = get_current_theme_data(parent)
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        ctk.CTkLabel(page, text=parent.translator.get("analysis_title"), font=fonts.get("header_large", ("Segoe UI Semibold", 22)), 
                     text_color=theme["text_primary"], anchor="w").pack(fill="x", pady=(0, 15))
        
        # Main Layout: Chart on Left, AI Analysis on Right
        content = ctk.CTkFrame(page, fg_color="transparent")
        content.pack(fill="both", expand=True)
        
        # Left Side - Chart
        parent.chart_frame = ctk.CTkFrame(content, fg_color=theme["bg_secondary"], corner_radius=12, border_width=1, border_color=theme["border_default"])
        parent.chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        parent.chart_label = ctk.CTkLabel(parent.chart_frame, text=parent.translator.get("analysis_empty"), 
                                        font=fonts["body"], text_color=theme["text_secondary"])
        parent.chart_label.pack(expand=True)
        
        # Right Side - AI Analysis
        analysis_side = ctk.CTkFrame(content, fg_color="transparent", width=300)
        analysis_side.pack(side="right", fill="y")
        
        # Verdict Card
        parent.verdict_card = ctk.CTkFrame(analysis_side, fg_color=theme["bg_tertiary"], height=100, corner_radius=12)
        parent.verdict_card.pack(fill="x", pady=(0, 10))
        parent.verdict_card.pack_propagate(False)
        
        parent.verdict_title = ctk.CTkLabel(parent.verdict_card, text=parent.translator.get("analysis_verdict"), font=fonts["body_small"], text_color=theme["text_secondary"])
        parent.verdict_title.pack(pady=(15, 0))
        parent.verdict_val = ctk.CTkLabel(parent.verdict_card, text=parent.translator.get("analysis_waiting"), font=fonts.get("header_large", ("Segoe UI Bold", 20)), text_color=theme["text_primary"])
        parent.verdict_val.pack()
        
        # Accuracy Card
        parent.acc_card = ctk.CTkFrame(analysis_side, fg_color=theme["bg_tertiary"], height=100, corner_radius=12)
        parent.acc_card.pack(fill="x", pady=(0, 10))
        parent.acc_card.pack_propagate(False)
        
        parent.acc_title = ctk.CTkLabel(parent.acc_card, text=parent.translator.get("analysis_acc"), font=fonts["body_small"], text_color=theme["text_secondary"])
        parent.acc_title.pack(pady=(15, 0))
        parent.acc_val = ctk.CTkLabel(parent.acc_card, text="0%", font=fonts.get("header_large", ("Segoe UI Bold", 20)), text_color=theme["accent_primary"])
        parent.acc_val.pack()
        
        # Reasoning Card
        parent.reason_card = ctk.CTkFrame(analysis_side, fg_color=theme["bg_secondary"], corner_radius=12)
        parent.reason_card.pack(fill="both", expand=True)
        
        ctk.CTkLabel(parent.reason_card, text=parent.translator.get("analysis_reason"), font=fonts["section_header"], 
                     text_color=theme["text_primary"]).pack(anchor="w", padx=15, pady=15)
        
        parent.reason_text = ctk.CTkTextbox(parent.reason_card, font=fonts["body_small"], 
                                          fg_color="transparent", text_color=theme["text_secondary"], border_width=0)
        parent.reason_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        parent.reason_text.insert("0.0", parent.translator.get("analysis_reason_empty"))
        parent.reason_text.configure(state="disabled")

        # Action Buttons
        btn_row = ctk.CTkFrame(page, fg_color="transparent")
        btn_row.pack(fill="x", pady=15)
        
        parent.btn_execute = ctk.CTkButton(btn_row, text=parent.translator.get("analysis_execute"), font=fonts["button_large"], 
                                         fg_color=theme["btn_primary_bg"], hover_color=theme["btn_primary_hover"],
                                         state="disabled")
        parent.btn_execute.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        parent.btn_skip = ctk.CTkButton(btn_row, text=parent.translator.get("analysis_skip"), font=fonts["button_large"], 
                                      fg_color=theme["btn_danger_bg"], hover_color=theme["btn_danger_hover"],
                                      state="disabled")
        parent.btn_skip.pack(side="left", fill="x", expand=True)
        
        # Debug Test Button
        ctk.CTkButton(page, text=parent.translator.get("analysis_debug_test"), font=fonts["body_small"], 
                      fg_color="transparent", text_color=theme["text_disabled"],
                      command=lambda: parent.perform_analysis("XAUUSD", "BUY", 2020.0, 2035.0, 2010.0)).pack(pady=5)
        
        return page
