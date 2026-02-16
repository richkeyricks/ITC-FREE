import os

file_path = "src/gui.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if "def _build_ai_page(self):" in line:
        start_idx = i
        break

if start_idx == -1:
    print("Start not found")
    exit(1)

end_idx = -1
for i in range(start_idx, len(lines)):
    if 'CTkToolTip(self.ai_send_btn' in lines[i]:
        end_idx = i
        break

if end_idx == -1:
    print("End not found")
    exit(1)

new_code = """    def _build_ai_page(self):
        # 1. Main Container (Fixed, grid layout - No Page Scroll)
        page = ctk.CTkFrame(self.main_container, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(1, weight=1) # Row 1 (Chat) expands
        
        # 2. Header & Settings (Row 0)
        settings_container = ctk.CTkFrame(page, fg_color="transparent")
        settings_container.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        
        ctk.CTkLabel(settings_container, text=self.translator.get("ai_title"), font=("Segoe UI Semibold", 22), 
                     text_color="white", anchor="w").pack(fill="x", pady=(0, 10))
        
        settings = ctk.CTkFrame(settings_container, fg_color=THEME["bg_secondary"], corner_radius=10)
        settings.pack(fill="x")
        
        # Row A: Switch & Provider
        row_a = ctk.CTkFrame(settings, fg_color="transparent")
        row_a.pack(fill="x", padx=15, pady=10)
        
        self.ai_enabled = ctk.BooleanVar(value=os.getenv("USE_AI", "False") == "True")
        ctk.CTkSwitch(row_a, text=self.translator.get("ai_fallback"), variable=self.ai_enabled, 
                      font=FONTS["body"]).pack(side="left")
        
        ctk.CTkLabel(row_a, text=self.translator.get("ai_provider"), font=FONTS["body_small"],
                     text_color=THEME["text_secondary"]).pack(side="left", padx=(30, 10))
        
        self.ai_provider = ctk.StringVar(value=os.getenv("AI_PROVIDER", "OpenRouter"))
        ctk.CTkSegmentedButton(row_a, values=["Gemini", "OpenRouter", "Groq"], 
                                variable=self.ai_provider).pack(side="left")

        # Row B: API Key
        row_b = ctk.CTkFrame(settings, fg_color="transparent")
        row_b.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(row_b, text=self.translator.get("ai_key"), font=FONTS["body_small"],
                     text_color=THEME["text_secondary"]).pack(side="left", padx=(0, 10))
        
        self.entry_ai_key = ctk.CTkEntry(row_b, height=32, fg_color=THEME["bg_tertiary"],
                                          border_color=THEME["border_default"], width=300,
                                          placeholder_text="sk-...")
        self.entry_ai_key.insert(0, os.getenv("AI_API_KEY", ""))
        self.entry_ai_key.pack(side="left", padx=(0, 15))
        
        try:
            import webbrowser
        except:
            pass
            
        for name, url in [("Get OpenRouter", "https://openrouter.ai/keys"), 
                          ("Get Gemini", "https://aistudio.google.com/app/apikey"), 
                          ("Get Groq", "https://console.groq.com/keys")]:
            ctk.CTkButton(row_b, text=name, width=80, height=28, font=("Segoe UI", 11),
                          fg_color=THEME["bg_tertiary"], hover_color=THEME["border_default"],
                          command=lambda u=url: webbrowser.open(u)).pack(side="left", padx=2)

        # 3. Chat Area (Row 1 - Expands)
        chat_frame = ctk.CTkFrame(page, fg_color="transparent")
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 10))
        
        ctk.CTkLabel(chat_frame, text=self.translator.get("ai_chat_title"), font=FONTS["section_header"],
                     text_color=THEME["text_secondary"], anchor="w").pack(fill="x", pady=(0, 5))
        
        self.ai_chat = ctk.CTkTextbox(chat_frame, font=FONTS["body"], 
                                      fg_color=THEME["bg_secondary"], corner_radius=8)
        self.ai_chat.pack(fill="both", expand=True)
        self.ai_chat.insert("0.0", f"{self.translator.get('ai_chat_intro')}\\n")
        self.ai_chat.configure(state="disabled")
        
        # 4. Input Area (Row 2 - Fixed Bottom)
        input_frame = ctk.CTkFrame(page, fg_color="transparent")
        input_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=(0, 5))
        
        self.ai_input = ctk.CTkEntry(input_frame, height=45, placeholder_text="Type your question here...",
                                      fg_color=THEME["bg_tertiary"], border_width=1)
        self.ai_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.ai_input.bind("<Return>", lambda e: self.send_ai_message())
        
        self.ai_send_btn = ctk.CTkButton(input_frame, text=self.translator.get("ai_chat_send"), width=100, height=45, 
                                         command=lambda: self.send_ai_message())
        self.ai_send_btn.pack(side="right")
        CTkToolTip(self.ai_send_btn, self.translator.get("hint_ai_send"))
"""

lines[start_idx:end_idx+1] = [new_code + "\n"]

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
