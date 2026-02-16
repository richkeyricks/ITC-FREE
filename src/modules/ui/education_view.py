import threading
import random
import customtkinter as ctk
from ui_theme import THEME_DARK, FONTS as LEGACY_FONTS
from ui_theme_modern import get_theme as get_modern_theme, FONTS as MODERN_FONTS
from utils.tooltips import CTkToolTip
from CTkMessagebox import CTkMessagebox

# --- HELPER ---
def get_current_theme_data(parent):
    if hasattr(parent, 'selected_theme') and parent.selected_theme in ["light", "neutral"]:
        return get_modern_theme(parent.selected_theme), MODERN_FONTS
    return THEME_DARK, LEGACY_FONTS

class EducationView:
    """
    Modular class for the Education (Academy) page.
    Follows Gravity Dev Rules: Modular & SoC.
    """
    
    @staticmethod
    def build(parent):
        """Builds the Education page and attaches it to the parent (App/GUI)."""
        theme, fonts = get_current_theme_data(parent)
        page = ctk.CTkFrame(parent.main_container, fg_color="transparent")
        
        # Header
        header_frame = ctk.CTkFrame(page, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="🎓 ITC Academy", font=fonts.get("header_large", ("Segoe UI Bold", 26)), 
                     text_color=theme["text_primary"]).pack(side="left")
        
        ctk.CTkLabel(header_frame, text="Daily Challenge", font=fonts["body"], 
                     text_color=theme["accent_primary"]).pack(side="right", padx=10)
        
        # Main Content Container
        parent.edu_main = ctk.CTkFrame(page, fg_color=theme["bg_secondary"], corner_radius=15, 
                                       border_width=1, border_color=theme["border_default"])
        parent.edu_main.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Populate with initial state
        EducationView.reset_education_view(parent)
        
        return page

    @staticmethod
    def reset_education_view(parent):
        """Restores the Education page to its initial state."""
        theme, fonts = get_current_theme_data(parent)
        for w in parent.edu_main.winfo_children(): w.destroy()
        
        # Layout: Centered Card
        center_frame = ctk.CTkFrame(parent.edu_main, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # Icon
        ctk.CTkLabel(center_frame, text="🧠", font=("Segoe UI", 64)).pack(pady=(0, 15))
        
        # Title
        ctk.CTkLabel(center_frame, text="Knowledge Challenge", font=fonts.get("header_large", ("Segoe UI Bold", 28)),
                     text_color=theme["text_primary"]).pack(pady=(0, 10))
        
        # Description
        ctk.CTkLabel(center_frame, text="Test your trading knowledge with AI-generated questions.\nComplete the daily challenge to earn bonus AI credits.", 
                     font=fonts["body"], text_color=theme["text_secondary"], justify="center").pack(pady=(0, 25))
        
        # Mission Badge
        mission_frame = ctk.CTkFrame(center_frame, fg_color=theme["bg_tertiary"], corner_radius=20, 
                                     border_width=1, border_color=theme["accent_success"])
        mission_frame.pack(pady=10, ipadx=10, ipady=5)
        
        ctk.CTkLabel(mission_frame, text="🎯", font=("Segoe UI", 16)).pack(side="left", padx=(15, 5), pady=8)
        ctk.CTkLabel(mission_frame, text="DAILY MISSION: Score 10/10 to Unlock +3 AI Chats!", 
                     font=fonts.get("body_bold", ("Segoe UI Bold", 13)), text_color=theme["accent_success"]).pack(side="left", padx=(0, 15), pady=8)
        
        # Difficulty Selector
        options_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        options_frame.pack(pady=20)
        
        ctk.CTkLabel(options_frame, text="Difficulty Level:", font=fonts["body_small"], 
                     text_color=theme["text_secondary"]).pack(pady=(0, 5))
        
        parent.edu_level = ctk.CTkOptionMenu(options_frame, values=["Pemula", "Menengah", "Ahli", "Legenda"], 
                                         font=fonts["body"], fg_color=theme["bg_tertiary"], 
                                         button_color=theme["accent_primary"], width=220, height=36)
        parent.edu_level.set("Pemula")
        parent.edu_level.pack()
        
        # Generate Button with Loading Logic
        parent.btn_quiz = ctk.CTkButton(center_frame, text="GENERATE AI QUIZ", height=50, width=280,
                                     fg_color=theme["accent_primary"], hover_color=theme["accent_primary_hover"],
                                     font=fonts.get("button_large", ("Segoe UI Bold", 15)), corner_radius=25,
                                     command=lambda: EducationView._handle_quiz_start(parent))
        parent.btn_quiz.pack(pady=10)

    @staticmethod
    def _handle_quiz_start(parent):
        """Disables button and shows loading state"""
        parent.btn_quiz.configure(state="disabled", text="Generating Questions... ⏳")
        parent._start_async_quiz() # Calls the delegated method in gui.py

    @staticmethod
    def generate_quiz_thread(parent):
        """Background Worker for Quiz Generation."""
        from index import generate_quiz_questions, get_env_list
        try:
            cfg = get_env_list()
            key = cfg["AI_API_KEY"] 
            provider = cfg["AI_PROVIDER"]
            level = parent.edu_level.get()
            
            questions = generate_quiz_questions(level, key, provider)
            
            if questions:
                parent.quiz_questions = questions
                parent.quiz_score = 0
                parent.quiz_index = 0
                parent.safe_ui_update(lambda: EducationView._show_next_question(parent))
            else:
                def _error_ui():
                    CTkMessagebox(title="AI Error", message="Gagal membuat soal. Coba lagi atau cek koneksi internet.", icon="cancel")
                    parent.btn_quiz.configure(state="normal", text="GENERATE AI QUIZ")
                parent.safe_ui_update(_error_ui)
                
        except Exception as e:
            print(f"// Quiz Thread Error: {e}")
            parent.safe_ui_update(lambda: parent.btn_quiz.configure(state="normal", text="GENERATE AI QUIZ"))

    @staticmethod
    def _show_next_question(parent):
        theme, fonts = get_current_theme_data(parent)
        for w in parent.edu_main.winfo_children(): w.destroy()
        
        if parent.quiz_index >= len(parent.quiz_questions):
            EducationView._show_result(parent)
            return

        q_data = parent.quiz_questions[parent.quiz_index]
        level_text = parent.edu_level.get() if hasattr(parent, 'edu_level') else "Quiz"
        
        # Layout
        q_frame = ctk.CTkFrame(parent.edu_main, fg_color="transparent")
        q_frame.pack(expand=True, fill="both", padx=60, pady=40)
        
        # Progress
        progress = (parent.quiz_index + 1) / len(parent.quiz_questions)
        ctk.CTkProgressBar(q_frame, width=400, progress_color=theme["accent_primary"]).pack(pady=(0, 10))
        ctk.CTkLabel(q_frame, text=f"Question {parent.quiz_index+1} / {len(parent.quiz_questions)}", 
                     font=fonts["body_small"], text_color=theme["text_secondary"]).pack(pady=(0, 20))
        
        # Question Card
        card = ctk.CTkFrame(q_frame, fg_color=theme["bg_tertiary"], corner_radius=15, border_width=1, border_color=theme["border_default"])
        card.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(card, text=q_data["q"], font=fonts.get("header_large", ("Segoe UI Bold", 22)), wraplength=500, justify="center", text_color=theme["text_primary"]).pack(pady=30, padx=20)
        
        # Options
        options = q_data["o"] + [q_data["a"]]
        random.shuffle(options)
        
        for opt in options:
            btn = ctk.CTkButton(q_frame, text=opt, height=55, fg_color="transparent", 
                                border_width=2, border_color=theme["border_default"],
                                hover_color=theme["bg_tertiary"], text_color=theme["text_primary"], font=fonts.get("button_large", ("Segoe UI", 16)),
                                corner_radius=12,
                                command=lambda o=opt: EducationView._check_answer(parent, o))
            btn.pack(fill="x", pady=8)

    @staticmethod
    def _check_answer(parent, selected):
        correct_ans = parent.quiz_questions[parent.quiz_index]["a"]
        if selected == correct_ans:
            parent.quiz_score += 1
            # Visual feedback could be added here (Green highlight), but for now we move next
        else:
            CTkMessagebox(title="Incorrect", message=f"Jawaban yang benar adalah:\n\n{correct_ans}", icon="info")
        
        parent.quiz_index += 1
        EducationView._show_next_question(parent)

    @staticmethod
    def _show_result(parent):
        theme, fonts = get_current_theme_data(parent)
        for w in parent.edu_main.winfo_children(): w.destroy()
        
        res_frame = ctk.CTkFrame(parent.edu_main, fg_color="transparent")
        res_frame.pack(expand=True)
        
        score = parent.quiz_score
        total = len(parent.quiz_questions)
        is_perfect = score == total
        
        icon = "🏆" if is_perfect else "📊"
        title = "Perfect Score!" if is_perfect else "Quiz Completed"
        color = theme["accent_success"] if is_perfect else theme["text_primary"]
        
        ctk.CTkLabel(res_frame, text=icon, font=("Segoe UI", 80)).pack(pady=(0, 20))
        ctk.CTkLabel(res_frame, text=title, font=fonts.get("header_large", ("Segoe UI Bold", 32)), text_color=color).pack(pady=(0, 10))
        ctk.CTkLabel(res_frame, text=f"You Scored: {score} / {total}", font=fonts.get("header_large", ("Segoe UI", 24)), text_color=theme["text_primary"]).pack(pady=(0, 30))
        
        reward_msg = ""
        if is_perfect:
            if parent.db_manager.increment_ai_bonus(3):
                reward_msg = "Bonus Unlocked: +3 AI Credits Added! 🚀"
            else:
                reward_msg = "(Login required for rewards)"
        else:
            reward_msg = "Tip: Score 10/10 to unlock AI bonuses!"
            
        ctk.CTkLabel(res_frame, text=reward_msg, font=fonts["body"], 
                     text_color=theme["accent_success"] if is_perfect else theme["text_secondary"]).pack(pady=(0, 40))
        
        parent.db_manager.push_quiz_score(score)
        
        ctk.CTkButton(res_frame, text="Back to Academy", height=50, width=200, corner_radius=25,
                      font=fonts.get("button_large", ("Segoe UI Bold", 15)), fg_color=theme["bg_tertiary"], hover_color=theme["border_default"],
                      text_color=theme["text_primary"],
                      command=lambda: EducationView.reset_education_view(parent)).pack()
