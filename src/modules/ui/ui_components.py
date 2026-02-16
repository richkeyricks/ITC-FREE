# src/ui_components.py
"""
Modular UI Component Factory for STC +AI CopyTrade.
Creates reusable, consistently styled components.
"""
import webbrowser
import re
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

# --- STRIKE THROUGH LABEL (Visual Reality) ---
def create_strike_label(master, text, font=None, text_color="gray", strike_color="#ff4444"):
    """
    Creates a label with a red diagonal strikethrough line overlay.
    Used for 'Harga Coret' to create psychological discount effect.
    """
    container = ctk.CTkFrame(master, fg_color="transparent")
    
    # 1. The Original Price Text
    lbl = ctk.CTkLabel(container, text=text, font=font or ("Segoe UI", 12), text_color=text_color)
    lbl.pack()
    
    # 2. The Red Line (Strikethrough)
    # We use a thin Frame placed over the center
    line = ctk.CTkFrame(container, height=2, fg_color=strike_color)
    line.place(relx=0, rely=0.5, relwidth=1, anchor="w")
    
    # Optional: Rotate slightly for "Handwritten" feel? No, standard strikethrough is horizontal.
    # If diagonal is needed, Canvas is required. But horizontal is standard for e-commerce.
    
    return container

# --- STEPPER STATES ---
STEP_PENDING = "pending"
STEP_ACTIVE = "active"
STEP_COMPLETED = "completed"

class QuickStartStepper(ctk.CTkFrame):
    """
    Interactive Stepper Component using CTkButtons.
    Maintains professional appearance while restoring navigation functionality.
    """
    def __init__(self, master, steps, callback=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.steps = steps # List of {"label": "...", "page": "...", "state": ...}
        self.callback = callback
        self.theme = get_current_theme()
        self.buttons = []
        
        self.build()

    def build(self):
        for widget in self.winfo_children(): widget.destroy()
        self.buttons = []
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", expand=True)
        
        for i, step in enumerate(self.steps):
            state = step.get("state", STEP_PENDING)
            label = step.get("label", "")
            page_id = step.get("page", "")
            
            # Semantic Colors based on State
            bg = self.theme["bg_tertiary"]
            hover = self.theme["accent_primary"]
            txt = self.theme["text_secondary"]
            border = self.theme["border_default"]
            border_w = 1
            
            prefix = f"{i+1}."
            if state == STEP_ACTIVE:
                bg = self.theme["bg_tertiary"]
                txt = self.theme["text_primary"]
                border = self.theme["accent_primary"]
                border_w = 2
            elif state == STEP_COMPLETED:
                bg = self.theme["accent_success"]
                hover = self.theme["btn_success_hover"]
                txt = "white"
                prefix = "✓"
                border = bg
            
            btn = ctk.CTkButton(
                container,
                text=f"{prefix} {label}",
                font=("Segoe UI Bold", 11),
                fg_color=bg,
                hover_color=hover,
                text_color=txt,
                border_color=border,
                border_width=border_w,
                height=34,
                corner_radius=8,
                command=lambda p=page_id: self._on_click(p)
            )
            btn.pack(side="left", fill="x", expand=True, padx=4)
            self.buttons.append(btn)
            
            # Add separator arrow (except last)
            if i < len(self.steps) - 1:
                sep = ctk.CTkLabel(container, text="›", font=("Arial", 16), text_color=self.theme["text_disabled"])
                sep.pack(side="left", padx=2)

    def _on_click(self, page_id):
        if self.callback:
            self.callback(page_id)

    def set_step_state(self, index, state):
        if 0 <= index < len(self.steps):
            if self.steps[index].get("state") != state:
                self.steps[index]["state"] = state
                self.build() # Rebuild for UI update

class ContextualTutorialCard(ctk.CTkFrame):
    """
    Glassmorphism-styled tutorial card for specific pages.
    """
    def __init__(self, master, title, steps_text, **kwargs):
        theme = get_current_theme()
        super().__init__(
            master, 
            fg_color=theme["bg_secondary"], 
            corner_radius=RADIUS["lg"],
            border_width=1,
            border_color=theme["border_default"],
            **kwargs
        )
        
        # PROPAGATION ENABLED FOR DYNAMIC SIZING
        
        # Header with icon
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(header, text="💡", font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text=title, font=("Segoe UI Bold", 13), text_color=theme["accent_info"]).pack(side="left")
        
        # Divider
        ctk.CTkFrame(self, height=1, fg_color=theme["border_default"]).pack(fill="x", padx=15, pady=5)
        
        # Content (Steps with Markdown handling)
        self.content_box = ctk.CTkTextbox(
            self, 
            fg_color="transparent", 
            font=("Segoe UI", 11), 
            text_color=theme["text_secondary"],
            wrap="word",
            cursor="arrow",
            # Reduced height to allow card to grow with content
            height=100
        )
        self.content_box.pack(fill="both", expand=True, padx=15, pady=(5, 10))
        
        self._insert_markdown_text(steps_text)
        self.content_box.configure(state="disabled")

    def _insert_markdown_text(self, text):
        """
        Parses [text](url) and inserts into CTkTextbox with clickable tags.
        """
        # Regex to find [text](url)
        pattern = r"\[(.*?)\]\((.*?)\)"
        
        parts = re.split(pattern, text)
        # re.split with groups returns: [prefix, text1, url1, text2, url2, ..., suffix]
        
        # Configure link tag
        theme = get_current_theme()
        link_color = theme.get("accent_info", "#3b82f6")
        self.content_box.tag_config("link", foreground=link_color, underline=True)
        
        for i in range(0, len(parts), 3):
            # Normal text
            self.content_box.insert("end", parts[i])
            
            # Link text (if exists)
            if i + 1 < len(parts):
                link_text = parts[i+1]
                link_url = parts[i+2]
                
                start_index = self.content_box.index("end-1c")
                self.content_box.insert("end", link_text, "link")
                end_index = self.content_box.index("end-1c")
                
                # Unique tag for each link to store its URL
                unique_tag = f"link_{i}"
                self.content_box.tag_add(unique_tag, start_index, end_index)
                self.content_box.tag_bind(unique_tag, "<Button-1>", lambda e, url=link_url: webbrowser.open(url))
                self.content_box.tag_bind(unique_tag, "<Enter>", lambda e: self.content_box.configure(cursor="hand2"))
                self.content_box.tag_bind(unique_tag, "<Leave>", lambda e: self.content_box.configure(cursor="arrow"))
