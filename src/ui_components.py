# src/ui_components.py
"""
Modular UI Component Factory for STC +AI CopyTrade.
Creates reusable, consistently styled components.
"""
import customtkinter as ctk
from ui_theme import get_theme, FONTS, SPACING, RADIUS, HEIGHTS

# --- GLOBAL STATE ---
_current_theme_name = "dark"

def set_theme(theme_name):
    """Sets the current theme for all new components"""
    global _current_theme_name
    _current_theme_name = theme_name

def get_current_theme():
    return get_theme(_current_theme_name)

# --- SECTION HEADER ---
def create_section_header(master, text):
    """Creates a styled section header (e.g., 'TELEGRAM CONFIG')"""
    theme = get_current_theme()
    frame = ctk.CTkFrame(master, fg_color=theme["bg_secondary"], corner_radius=0)
    frame.pack(fill="x", pady=(SPACING["md"], SPACING["xs"]))
    
    label = ctk.CTkLabel(
        frame, 
        text=text.upper(),
        font=FONTS["section_header"],
        text_color=theme["text_secondary"],
        anchor="w"
    )
    label.pack(fill="x", padx=SPACING["md"], pady=SPACING["xs"])
    return frame

# --- INPUT ROW ---
def create_input_row(master, label_text, initial_val="", placeholder="", show="", entry_width=None):
    """Creates a compact, aligned input row (label + entry)"""
    theme = get_current_theme()
    
    row = ctk.CTkFrame(master, fg_color="transparent")
    row.pack(fill="x", pady=SPACING["xs"], padx=SPACING["md"])
    
    # Grid layout for alignment
    row.columnconfigure(1, weight=1)
    
    label = ctk.CTkLabel(
        row, 
        text=label_text,
        font=FONTS["body"],
        text_color=theme["text_secondary"],
        width=100,
        anchor="w"
    )
    label.grid(row=0, column=0, sticky="w", padx=(0, SPACING["sm"]))
    
    entry = ctk.CTkEntry(
        row,
        placeholder_text=placeholder,
        show=show,
        height=HEIGHTS["input"],
        font=FONTS["input"],
        fg_color=theme["bg_tertiary"],
        border_color=theme["border_default"],
        text_color=theme["text_primary"],
        corner_radius=RADIUS["sm"]
    )
    entry.insert(0, initial_val)
    entry.grid(row=0, column=1, sticky="ew")
    
    return entry

# --- BUTTON STYLES ---
def create_button(master, text, command, style="primary", width=None, height=None):
    """Creates styled buttons with consistent appearance"""
    theme = get_current_theme()
    
    styles = {
        "primary": (theme["btn_primary_bg"], theme["btn_primary_hover"], "white"),
        "secondary": (theme["bg_tertiary"], theme["border_default"], theme["text_primary"]),
        "danger": (theme["btn_danger_bg"], theme["btn_danger_hover"], "white"),
        "success": (theme["accent_success"], theme["btn_primary_hover"], "white"),
        "warning": (theme["accent_warning"], theme["btn_danger_hover"], "white"),
    }
    
    bg, hover, text_color = styles.get(style, styles["primary"])
    
    btn = ctk.CTkButton(
        master,
        text=text,
        command=command,
        font=FONTS["button"],
        fg_color=bg,
        hover_color=hover,
        text_color=text_color,
        height=height or HEIGHTS["button"],
        width=width,
        corner_radius=RADIUS["md"]
    )
    return btn

# --- INDICATOR DOT ---
def create_status_indicator(master, label_text):
    """Creates a status indicator with dot and label"""
    theme = get_current_theme()
    
    container = ctk.CTkFrame(master, fg_color="transparent")
    container.pack(side="left", expand=True, padx=SPACING["sm"])
    
    dot = ctk.CTkLabel(
        container, 
        text="●", 
        text_color=theme["accent_danger"],  # Default red
        font=("Segoe UI", 14)
    )
    dot.pack(side="left", padx=(0, SPACING["xs"]))
    
    lbl = ctk.CTkLabel(
        container, 
        text=label_text, 
        font=FONTS["body_small"],
        text_color=theme["text_secondary"]
    )
    lbl.pack(side="left")
    
    return dot

# --- CARD FRAME ---
def create_card(master, title=None):
    """Creates a card-style frame with optional title"""
    theme = get_current_theme()
    
    card = ctk.CTkFrame(
        master,
        fg_color=theme["bg_secondary"],
        corner_radius=RADIUS["lg"],
        border_width=1,
        border_color=theme["border_default"]
    )
    
    if title:
        title_lbl = ctk.CTkLabel(
            card,
            text=title.upper(),
            font=FONTS["section_header"],
            text_color=theme["text_secondary"],
            anchor="w"
        )
        title_lbl.pack(fill="x", padx=SPACING["md"], pady=(SPACING["sm"], SPACING["xs"]))
    
    return card

# --- DASHBOARD STAT ---
def create_stat_display(master, label, value, color=None):
    """Creates a stat display for dashboard (Balance, Equity, P/L)"""
    theme = get_current_theme()
    
    frame = ctk.CTkFrame(master, fg_color="transparent")
    
    lbl = ctk.CTkLabel(
        frame,
        text=label,
        font=FONTS["body_small"],
        text_color=theme["text_secondary"]
    )
    lbl.pack()
    
    val = ctk.CTkLabel(
        frame,
        text=value,
        font=("Segoe UI Semibold", 14),
        text_color=color or theme["text_primary"]
    )
    val.pack()
    
    return frame, val
