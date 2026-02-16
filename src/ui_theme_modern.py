"""
Modern Professional Design System for STC +AI CopyTrade
Light & Sleek Theme with Futuristic Elements
"""

# ============================================================
# MODERN LIGHT THEME COLORS
# ============================================================
MODERN_LIGHT_THEME = {
    "name": "modern_light",
    "appearance_mode": "Light",

    # Foundation Colors (Clean, Minimal)
    "bg_primary": "#ffffff",           # Pure white background
    "bg_secondary": "#f8fafc",         # Soft card background
    "bg_tertiary": "#f1f5f9",          # Hover/selected states
    "border_default": "#e2e8f0",       # Subtle borders
    "border_active": "#3b82f6",        # Blue active border
    "border_glow": "#dbeafe",          # Light blue glow

    # Text Colors
    "text_primary": "#0f172a",         # Dark gray for main text
    "text_secondary": "#64748b",       # Medium gray for labels
    "text_disabled": "#cbd5e1",        # Light gray for disabled

    # Accent Colors (Professional Palette)
    "accent_primary": "#3b82f6",       # Professional blue
    "accent_primary_hover": "#2563eb", # Darker blue for hover
    "accent_secondary": "#8b5cf6",     # Purple accent
    "accent_success": "#10b981",       # Professional green
    "accent_warning": "#f59e0b",       # Amber warning
    "accent_danger": "#ef4444",        # Red danger
    "accent_info": "#0ea5e9",          # Sky blue info

    # Trading-Specific Colors
    "buy": "#10b981",                  # Profit/green
    "sell": "#ef4444",                 # Loss/red
    "neutral": "#94a3b8",              # Neutral state

    # Status Colors
    "status_online": "#10b981",        # Success green
    "status_offline": "#94a3b8",       # Gray offline
    "status_warning": "#f59e0b",       # Warning amber
    "status_error": "#ef4444",         # Error red

    # Card & Component Styles
    "card_bg": "#ffffff",              # White cards
    "card_border": "#e2e8f0",          # Light border
    "card_border_hover": "#3b82f6",    # Blue border on hover
    "card_shadow": "#e2e8f0",          # Subtle shadow

    # Button Styles
    "btn_primary_bg": "#3b82f6",       # Blue primary
    "btn_primary_hover": "#2563eb",    # Darker blue hover
    "btn_success_bg": "#10b981",       # Green success
    "btn_success_hover": "#059669",    # Darker green hover
    "btn_danger_bg": "#ef4444",        # Red danger
    "btn_danger_hover": "#dc2626",     # Darker red hover
    "btn_secondary_bg": "#f1f5f9",     # Light gray secondary
    "btn_secondary_hover": "#e2e8f0",  # Darker gray hover
    "btn_premium_bg": "#8b5cf6",       # Purple premium
    "btn_premium_hover": "#7c3aed",    # Darker purple hover

    # Sidebar & Navigation
    "sidebar_bg": "#f8fafc",           # Light sidebar
    "sidebar_active_bg": "#eff6ff",    # Blue-tinged active
    "sidebar_active_border": "#3b82f6", # Blue active border
    "sidebar_hover_bg": "#f1f5f9",     # Hover state

    # Glassmorphism Effects (Light version)
    "glass_bg": "#ffffff",                   # Semi-transparent white fallback
    "glass_border": "#e2e8f0",               # Light border
    
    # Scrollbar
    "scrollbar_width": 8,
    "scrollbar_button_color": "#cbd5e1",
    "scrollbar_button_hover_color": "#94a3b8"
}

# ============================================================
# DARK MODE - MODERN PROFESSIONAL
# ============================================================
MODERN_DARK_THEME = {
    "name": "modern_dark",
    "appearance_mode": "Dark",

    # Foundation Colors (Deep, Professional)
    "bg_primary": "#0f172a",           # Deep navy blue
    "bg_secondary": "#1e293b",         # Dark slate
    "bg_tertiary": "#334155",          # Medium slate
    "border_default": "#475569",       # Steel border
    "border_active": "#60a5fa",        # Light blue active
    "border_glow": "#1e3a8a",          # Deep blue glow

    # Text Colors
    "text_primary": "#f1f5f9",         # Light text
    "text_secondary": "#94a3b8",       # Medium light text
    "text_disabled": "#64748b",        # Muted text

    # Accent Colors (Professional Dark Palette)
    "accent_primary": "#60a5fa",       # Light blue primary
    "accent_primary_hover": "#3b82f6", # Medium blue hover
    "accent_secondary": "#a78bfa",     # Light purple
    "accent_success": "#34d399",       # Mint green
    "accent_warning": "#fbbf24",       # Golden yellow
    "accent_danger": "#f87171",        # Light red
    "accent_info": "#7dd3fc",          # Sky blue

    # Trading-Specific Colors
    "buy": "#34d399",                  # Profit mint
    "sell": "#f87171",                 # Loss pink-red
    "neutral": "#94a3b8",              # Neutral slate

    # Status Colors
    "status_online": "#34d399",        # Mint success
    "status_offline": "#64748b",       # Muted gray
    "status_warning": "#fbbf24",       # Golden warning
    "status_error": "#f87171",         # Pink-red error

    # Card & Component Styles
    "card_bg": "#1e293b",              # Dark slate card
    "card_border": "#475569",          # Steel border
    "card_border_hover": "#60a5fa",    # Light blue hover
    "card_shadow": "#0f172a",          # Deep shadow

    # Button Styles
    "btn_primary_bg": "#60a5fa",       # Light blue primary
    "btn_primary_hover": "#3b82f6",    # Medium blue hover
    "btn_success_bg": "#34d399",       # Mint success
    "btn_success_hover": "#10b371",    # Darker mint hover
    "btn_danger_bg": "#f87171",        # Light red danger
    "btn_danger_hover": "#ef4444",     # Medium red hover
    "btn_secondary_bg": "#334155",     # Medium slate secondary
    "btn_secondary_hover": "#475569",  # Darker slate hover
    "btn_premium_bg": "#a78bfa",       # Light purple premium
    "btn_premium_hover": "#8b5cf6",    # Medium purple hover

    # Sidebar & Navigation
    "sidebar_bg": "#0f172a",           # Deep navy sidebar
    "sidebar_active_bg": "#1e3a8a",    # Blue-tinged active
    "sidebar_active_border": "#60a5fa", # Light blue active border
    "sidebar_hover_bg": "#1e293b",     # Dark slate hover

    # Glassmorphism Effects (Dark version)
    "glass_bg": "#0f172a",                # Semi-transparent deep blue fallback
    "glass_border": "#475569",             # Steel border
    
    # Scrollbar
    "scrollbar_width": 8,
    "scrollbar_button_color": "#60a5fa",
    "scrollbar_button_hover_color": "#3b82f6"
}

# ============================================================
# NEUTRAL THEME (Balanced)
# ============================================================
NEUTRAL_THEME = {
    "name": "neutral",
    "appearance_mode": "Light",

    # Foundation Colors (Neutral Professional - Darker Slate Grey)
    "bg_primary": "#f1f5f9",           # Slate-100 (Much darker than white)
    "bg_secondary": "#e2e8f0",         # Slate-200 (Distinct card bg)
    "bg_tertiary": "#cbd5e1",          # Slate-300
    "border_default": "#94a3b8",       # Slate-400
    "border_active": "#64748b",        # Slate-500
    "border_glow": "#cbd5e1",          # Slate-300 glow

    # Text Colors
    "text_primary": "#0f172a",         # Slate-900
    "text_secondary": "#475569",       # Slate-600
    "text_disabled": "#94a3b8",        # Slate-400

    # Accent Colors (Professional Grey-Blue)
    "accent_primary": "#475569",       # Slate-600 (Professional Grey)
    "accent_primary_hover": "#334155", # Slate-700
    "accent_secondary": "#64748b",     # Slate-500
    "accent_success": "#059669",       # Emerald-600
    "accent_warning": "#d97706",       # Amber-600
    "accent_danger": "#dc2626",        # Red-600
    "accent_info": "#0284c7",          # Sky-600

    # Trading-Specific Colors
    "buy": "#059669",                  # Emerald
    "sell": "#dc2626",                 # Red
    "neutral": "#64748b",              # Slate

    # Status Colors
    "status_online": "#059669",
    "status_offline": "#94a3b8",
    "status_warning": "#d97706",
    "status_error": "#dc2626",

    # Card & Component Styles
    "card_bg": "#ffffff",              # White cards stand out on Slate BG
    "card_border": "#cbd5e1",          # Slate-300
    "card_border_hover": "#94a3b8",    # Slate-400
    "card_shadow": "#cbd5e1",

    # Button Styles
    "btn_primary_bg": "#475569",       # Slate Primary
    "btn_primary_hover": "#334155",
    "btn_success_bg": "#059669",
    "btn_success_hover": "#047857",
    "btn_danger_bg": "#dc2626",
    "btn_danger_hover": "#b91c1c",
    "btn_secondary_bg": "#e2e8f0",
    "btn_secondary_hover": "#cbd5e1",
    "btn_premium_bg": "#7c3aed",
    "btn_premium_hover": "#6d28d9",

    # Sidebar & Navigation
    "sidebar_bg": "#e2e8f0",           # Slate-200 Sidebar
    "sidebar_active_bg": "#cbd5e1",    # Slate-300 Active
    "sidebar_active_border": "#475569", # Slate-600 Border
    "sidebar_hover_bg": "#f1f5f9",

    # Glassmorphism Effects
    "glass_bg": "#f1f5f9",
    "glass_border": "#cbd5e1",
    
    # Scrollbar
    "scrollbar_width": 10,
    "scrollbar_button_color": "#94a3b8",
    "scrollbar_button_hover_color": "#64748b"
}

# ============================================================
# TYPOGRAPHY (Modern Font Stack)
# ============================================================
FONTS = {
    "title": ("Inter", 24, "bold"),           # Modern sans-serif
    "header_large": ("Inter", 26, "bold"),    # Large headers
    "title_ai": ("Inter", 30, "bold"),        # AI section titles
    "subtitle": ("Inter", 12),
    "section_header": ("Inter Medium", 14),
    "body": ("Inter", 12),
    "body_bold": ("Inter Medium", 12),
    "body_small": ("Inter", 11),
    "input": ("Inter", 12),
    "button": ("Inter Medium", 12),
    "button_large": ("Inter Medium", 14),
    "log": ("JetBrains Mono", 11),
    "mono": ("JetBrains Mono", 11),
}

# ============================================================
# SPACING SCALE (Consistent Rhythm)
# ============================================================
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
    "xxl": 32,
}

# ============================================================
# CORNER RADIUS (Modern Rounded Elements)
# ============================================================
RADIUS = {
    "sm": 6,
    "md": 8,
    "lg": 12,
    "xl": 16,
    "full": 9999,  # Pill shape
}

# ============================================================
# COMPONENT HEIGHTS
# ============================================================
HEIGHTS = {
    "input": 40,
    "button": 42,
    "button_large": 52,
    "tab": 36,
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def get_theme(theme_name="dark"):
    """Returns the theme dictionary"""
    themes = {
        "light": MODERN_LIGHT_THEME,
        "dark": MODERN_DARK_THEME,
        "neutral": NEUTRAL_THEME
    }
    return themes.get(theme_name, MODERN_DARK_THEME)

def apply_theme_to_ctk(ctk_module, theme_name="dark"):
    """Applies the theme to CustomTkinter appearance"""
    ctk_module.set_appearance_mode(get_theme(theme_name)["appearance_mode"])