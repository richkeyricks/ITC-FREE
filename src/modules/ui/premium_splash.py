# src/modules/ui/premium_splash.py
# --- IMPORTS ---
import customtkinter as ctk
import os
import threading
import time
import random
import math
from tkinter import Canvas

# --- CONSTANTS ---
# Colors (Deep Industrial Dark - Command Center Palette)
BG_COLOR = "#0b0e14"
BG_CARD = "#111820"
ACCENT_BLUE = "#3b82f6"
ACCENT_CYAN = "#06d6a0"
ACCENT_GREEN = "#10b981"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#94a3b8"
TEXT_GHOST = "#1a1f2e"
BORDER_COLOR = "#1e2735"

# Ghost Matrix Characters
MATRIX_CHARS = "01アイウエオカキクケコサシスセソ"

# Neural Boot Sequence Messages
BOOT_SEQUENCE = [
    "INITIALIZING_NEURAL_CORE...",
    "LOADING_MARKET_INTELLIGENCE...",
    "ENCRYPTING_API_TUNNEL...",
    "SYNCING_GLOBAL_FEEDS...",
    "CALIBRATING_AI_MODELS...",
    "APEX_HEALER_ONLINE...",
    "SYSTEM_OPTIMIZED_AND_READY."
]

# --- CLASSES ---
class PremiumSplash(ctk.CTkToplevel):
    """
    World-class Premium Splash Screen V2 for ITC +AI Enterprise.
    Design Pillars:
    1. Superscript Logo (ITC^+AI)
    2. Wide-Tracked Military Subtitle
    3. Liquid Gradient Progress Bar (Canvas)
    4. Ghost Matrix Background Animation
    5. Dynamic Neural Boot Sequence
    6. Fade-Zoom Portal Exit Transition
    """

    def __init__(self, parent):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("ITC AI Initialization")
        self.overrideredirect(True)

        # Center on screen
        self.w, self.h = 650, 420
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{self.w}x{self.h}+{(sw - self.w) // 2}+{(sh - self.h) // 2}")

        self.configure(fg_color=BG_COLOR)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.0) # Start invisible for fade-in

        # --- STATE ---
        self._progress_value = 0.0
        self._shimmer_offset = 0
        self._matrix_columns = []
        self._is_alive = True
        self._boot_index = 0

        # --- BUILD UI ---
        self._build_ui()

        # --- START ANIMATIONS ---
        self._fade_in()
        self._start_matrix_animation()
        self._start_shimmer_animation()

    def _build_ui(self):
        """Constructs the entire splash screen UI."""
        # --- LAYER 0: GHOST MATRIX BACKGROUND ---
        self.matrix_canvas = Canvas(self, bg=BG_COLOR, highlightthickness=0,
                                    width=self.w, height=self.h)
        self.matrix_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Initialize matrix columns
        col_count = self.w // 18
        for i in range(col_count):
            x = i * 18 + 9
            y = random.randint(-self.h, 0)
            speed = random.uniform(0.5, 2.0)
            char = random.choice(MATRIX_CHARS)
            text_id = self.matrix_canvas.create_text(
                x, y, text=char, fill=TEXT_GHOST,
                font=("Consolas", 11), anchor="center"
            )
            self._matrix_columns.append({
                "id": text_id, "x": x, "y": y,
                "speed": speed, "char": char
            })

        # --- LAYER 1: MAIN CONTAINER (Glassmorphism Card) ---
        self.main_frame = ctk.CTkFrame(
            self, fg_color=BG_CARD, corner_radius=18,
            border_width=1, border_color=BORDER_COLOR
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center",
                              relwidth=0.92, relheight=0.88)

        # --- LAYER 2: LOGO SECTION ---
        logo_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        logo_container.place(relx=0.5, rely=0.32, anchor="center")

        # "ITC" - Primary Logo (Premium Heavy Font)
        self.logo_itc = ctk.CTkLabel(
            logo_container, text="ITC",
            font=("Segoe UI Black", 72, "bold"),
            text_color=ACCENT_BLUE
        )
        self.logo_itc.pack(side="left", anchor="s")

        # "+AI" - Superscript / Exponent (Small, Elevated)
        self.logo_ai = ctk.CTkLabel(
            logo_container, text="+AI",
            font=("Segoe UI Semibold", 22),
            text_color=ACCENT_GREEN
        )
        self.logo_ai.pack(side="left", anchor="n", padx=(2, 0), pady=(8, 0))

        # --- LAYER 3: SUBTITLE (Wide-Tracked Military Style) ---
        wide_text = "E N T E R P R I S E   I N T E L L I G E N C E   S Y S T E M"
        self.sub_label = ctk.CTkLabel(
            self.main_frame, text=wide_text,
            font=("Segoe UI Light", 9),
            text_color=TEXT_SECONDARY
        )
        self.sub_label.place(relx=0.5, rely=0.48, anchor="center")

        # --- LAYER 4: PROGRESS SECTION ---
        progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=80)
        progress_frame.place(relx=0.5, rely=0.73, anchor="center", relwidth=0.78)

        # Dynamic Status Text
        self.status_lbl = ctk.CTkLabel(
            progress_frame, text=BOOT_SEQUENCE[0],
            font=("Consolas", 10),
            text_color=TEXT_SECONDARY
        )
        self.status_lbl.pack(anchor="w", pady=(0, 8))

        # Liquid Gradient Progress Bar (Canvas)
        self.bar_height = 7
        self.bar_canvas = Canvas(
            progress_frame, height=self.bar_height + 4,
            bg=BG_CARD, highlightthickness=0
        )
        self.bar_canvas.pack(fill="x")

        # Draw bar track (dark background)
        self.bar_canvas.bind("<Configure>", self._on_bar_configure)

        # Percentage Label (Monospace, Clean)
        self.percent_lbl = ctk.CTkLabel(
            progress_frame, text="0%",
            font=("Consolas Bold", 11),
            text_color=ACCENT_CYAN
        )
        self.percent_lbl.pack(anchor="e", pady=(3, 0))

        # --- LAYER 5: FOOTER ---
        self.footer_lbl = ctk.CTkLabel(
            self.main_frame,
            text="© 2026 ITC TECHNOLOGY GROUP  •  HIGH-FREQUENCY TRADING LAYER",
            font=("Segoe UI Light", 7),
            text_color="#2a3040"
        )
        self.footer_lbl.place(relx=0.5, rely=0.94, anchor="center")

    # --- HANDLERS ---
    def _on_bar_configure(self, event=None):
        """Redraws the progress bar when the canvas is resized."""
        self._redraw_bar()

    def _redraw_bar(self):
        """Draws the liquid gradient progress bar on canvas."""
        try:
            if not self.winfo_exists():
                return
            self.bar_canvas.delete("all")
            canvas_w = self.bar_canvas.winfo_width()
            if canvas_w <= 1:
                canvas_w = 400

            h = self.bar_height
            y_offset = 2

            # Track background (Dark Groove)
            self.bar_canvas.create_rectangle(
                0, y_offset, canvas_w, y_offset + h,
                fill="#1c2128", outline=""
            )

            # Active bar width
            bar_w = int(canvas_w * self._progress_value)
            if bar_w < 2:
                return

            # Draw gradient segments (Blue → Cyan)
            segments = max(1, bar_w)
            for i in range(segments):
                ratio = i / max(1, bar_w - 1)
                # Interpolate from ACCENT_BLUE (#3b82f6) to ACCENT_CYAN (#06d6a0)
                r = int(59 + (6 - 59) * ratio)
                g = int(130 + (214 - 130) * ratio)
                b = int(246 + (160 - 246) * ratio)

                # Shimmer effect: brighten near the shimmer_offset
                shimmer_dist = abs(i - self._shimmer_offset)
                if shimmer_dist < 30:
                    brightness = 1.0 + 0.3 * (1.0 - shimmer_dist / 30.0)
                    r = min(255, int(r * brightness))
                    g = min(255, int(g * brightness))
                    b = min(255, int(b * brightness))

                color = f"#{r:02x}{g:02x}{b:02x}"
                self.bar_canvas.create_rectangle(
                    i, y_offset, i + 1, y_offset + h,
                    fill=color, outline=""
                )

            # Rounded cap at the end of the bar
            self.bar_canvas.create_oval(
                bar_w - 3, y_offset, bar_w + 3, y_offset + h,
                fill=ACCENT_CYAN, outline=""
            )
        except Exception:
            pass

    # --- ANIMATIONS ---
    def _fade_in(self):
        """Smooth fade-in on startup."""
        alpha = 0.0

        def _step():
            nonlocal alpha
            if not self._is_alive:
                return
            try:
                if not self.winfo_exists():
                    return
                alpha += 0.05
                if alpha >= 1.0:
                    self.attributes("-alpha", 1.0)
                    return
                self.attributes("-alpha", alpha)
                self.after(20, _step)
            except Exception:
                pass

        self.after(50, _step)

    def _start_matrix_animation(self):
        """Animates the ghost data stream in the background."""
        def _tick():
            if not self._is_alive:
                return
            try:
                if not self.winfo_exists():
                    return
                for col in self._matrix_columns:
                    col["y"] += col["speed"]
                    if col["y"] > self.h:
                        col["y"] = random.randint(-80, -10)
                        col["char"] = random.choice(MATRIX_CHARS)
                        self.matrix_canvas.itemconfig(col["id"], text=col["char"])
                    self.matrix_canvas.coords(col["id"], col["x"], col["y"])
                self.after(50, _tick)
            except Exception:
                pass

        self.after(100, _tick)

    def _start_shimmer_animation(self):
        """Animates the shimmer highlight across the progress bar."""
        def _tick():
            if not self._is_alive:
                return
            try:
                if not self.winfo_exists():
                    return
                canvas_w = self.bar_canvas.winfo_width()
                if canvas_w <= 1:
                    canvas_w = 400
                self._shimmer_offset = (self._shimmer_offset + 3) % (canvas_w + 60)
                self._redraw_bar()
                self.after(30, _tick)
            except Exception:
                pass

        self.after(200, _tick)

    # --- PUBLIC API ---
    def update_progress(self, percent, status_text=None):
        """Update progress bar and status text safely from any thread."""
        def _apply():
            try:
                if not self.winfo_exists():
                    return
                self._progress_value = max(0.0, min(1.0, percent / 100.0))
                self.percent_lbl.configure(text=f"{int(percent)}%")

                if status_text:
                    self.status_lbl.configure(text=status_text)
                elif percent < 100:
                    # Auto-cycle boot sequence based on progress
                    idx = min(len(BOOT_SEQUENCE) - 2, int(percent / 100 * (len(BOOT_SEQUENCE) - 1)))
                    self.status_lbl.configure(text=BOOT_SEQUENCE[idx])
                else:
                    self.status_lbl.configure(text=BOOT_SEQUENCE[-1])

            except Exception:
                pass

        try:
            if self.winfo_exists():
                self.after(0, _apply)
        except Exception:
            pass

    def close(self):
        """Portal Exit: Fade-out + subtle zoom before destroying."""
        self._is_alive = False
        alpha = 1.0

        def _fade_step():
            nonlocal alpha
            try:
                if not self.winfo_exists():
                    return
                alpha -= 0.06
                if alpha <= 0.0:
                    self.destroy()
                    return
                self.attributes("-alpha", alpha)

                # Subtle zoom effect: expand window slightly
                current_w = self.w + int((1.0 - alpha) * 40)
                current_h = self.h + int((1.0 - alpha) * 25)
                sw = self.winfo_screenwidth()
                sh = self.winfo_screenheight()
                x = (sw - current_w) // 2
                y = (sh - current_h) // 2
                self.geometry(f"{current_w}x{current_h}+{x}+{y}")

                self.after(25, _fade_step)
            except Exception:
                try:
                    self.destroy()
                except Exception:
                    pass

        self.after(200, _fade_step)
