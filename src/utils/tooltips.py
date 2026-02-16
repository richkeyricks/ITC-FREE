# src/utils/tooltips.py
import customtkinter as ctk
import tkinter as tk

class CTkToolTip:
    """
    A professional tooltip helper for CustomTkinter widgets.
    Displays a floating hint when hover, designed to follow the app's dark theme.
    """
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay  # ms before tooltip appears
        self.tip_window = None
        self.id = None
        
        # --- BINDINGS ---
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        self.schedule()

    def on_leave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show(self):
        if self.tip_window or not self.text:
            return

        # Position the tooltip
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        # Add widget height to spawn below it, preventing overlap/flicker
        y += self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Create floating window
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # No window decorations
        tw.wm_geometry(f"+{x}+{y}")
        tw.wm_attributes("-topmost", True)
        
        # Style (Matching ITC Theme)
        # We use a standard tk.Label inside because it's lightweight for small popups
        label = tk.Label(
            tw, text=self.text, justify='left',
            background="#242A31", foreground="#E6EAF0",
            relief='solid', borderwidth=1,
            font=("Segoe UI", 10),
            padx=10, pady=5
        )
        label.pack()

    def hide(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
