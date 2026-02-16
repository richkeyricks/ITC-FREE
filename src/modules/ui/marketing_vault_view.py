# ══════════════════════════════════════════════════════════════════════════════
# 🏛️ MARKETING VAULT (ACADEMY OF TITANS v5.3.2)
# 🎯 ROLE: Marketing Kit Hub — Scripts, AI Prompts (with AI Generator), Tools
# 🎨 STYLE: Dark Mode Command Center
# ══════════════════════════════════════════════════════════════════════════════

import customtkinter as ctk
import webbrowser
import json
import threading
from CTkMessagebox import CTkMessagebox

# --- CONSTANTS ---

# System prompt for AI Video Prompt Generator
VEO_SYSTEM_PROMPT = """You are a professional video prompt engineer for AI video generators (Google Veo 2/3, RunwayML, Kling AI, Pika, etc).

Generate ONE unique, highly detailed JSON video prompt.

MANDATORY BRANDING (MUST appear in EVERY prompt):
- Brand Name: "ITC Intelligence Copy Trading"
- Website: "www.TelegramCopyTrading.com"
- These MUST appear as text_overlay in the generated prompt

OUTPUT FORMAT (return ONLY valid JSON, no markdown, no code blocks, no explanation):
{
  "title": "A short creative title for this video concept",
  "platform": "Google Veo / RunwayML / Kling AI",
  "duration": "8s",
  "aspect_ratio": "9:16 or 16:9",
  "visual_prompt": "Extremely detailed scene description including subject, action, environment, textures, colors. Be specific like a film director.",
  "camera_motion": "Specific camera movement (e.g., slow dolly in, orbital tracking shot, crane up, handheld follow)",
  "lighting": "Detailed lighting description (e.g., dramatic rim light with cool blue fill, golden hour volumetric rays)",
  "color_palette": "Dominant color scheme (e.g., deep navy + neon green + gold accents)",
  "text_overlay": "ITC Intelligence Copy Trading\\nwww.TelegramCopyTrading.com",
  "audio": {
    "music_style": "Genre and mood (e.g., epic cinematic orchestral, lo-fi chill beats, dark trap)",
    "music_bpm": "Estimated BPM (e.g., 90-110)",
    "voiceover": "Narration script if applicable (e.g., 'Your money. Your rules. AI does the rest.')",
    "voiceover_tone": "Voice character (e.g., deep confident male, professional female, robotic AI)",
    "sfx": ["impact whoosh on logo reveal", "digital data stream sound", "cash register ding"]
  },
  "style": "Visual style (e.g., cinematic 4K, cyberpunk neon, clean corporate, retro VHS)",
  "mood": "Emotional tone (e.g., empowering, luxurious, urgent, futuristic)",
  "negative_prompt": "Elements to avoid (e.g., cartoon style, bright daylight, text errors)",
  "hashtags": ["#AITrading", "#CopyTrade", "#PassiveIncome", "#Fintech", "#ITC"],
  "posting_tip": "Brief advice (e.g., Post on IG Reels at 7-9PM for max reach)"
}

VARIATION RULES:
- Each generation MUST be completely unique and creative
- Rotate themes: wealth/lifestyle, technology/AI, community/trust, performance/data, urgency/FOMO
- Rotate scenes: trading desk, luxury apartment, city skyline, modern office, phone close-up, holographic displays
- Rotate camera: dolly, crane, tracking, static, handheld, aerial, first-person
- Rotate audio: orchestral, electronic, lo-fi, trap, ambient, corporate
- Rotate aspect: alternate between 9:16 (Reels/TikTok) and 16:9 (YouTube)
- ALWAYS include detailed audio section for Veo 3 / audio-capable generators"""

VEO_USER_PROMPT = "Generate a completely new and unique AI video prompt for a fintech/trading brand advertisement. Make it creative, cinematic, and different from any previous generation. Return ONLY the JSON object."

# Viral Scripts Data
VIRAL_SCRIPTS = [
    (
        "The 'FOMO' Hook (15s Video)",
        "📱 TikTok / IG Reels",
        "STOP trading pake perasaan! 🛑\n\nGw baru nemu AI yang bisa baca chart 24 jam non-stop.\nHasilnya? Profit gw naik 20% minggu ini tanpa capek analisa.\n\nCek link di bio sebelum aksesnya ditutup! 🚀\n\n#AItrading #PassiveIncome #CopyTrade",
        "📖 TARGET: Usia 25-35, interest trading/crypto.\n⏰ WAKTU POST: 7-9 PM WIB (peak engagement).\n🎯 GOAL: Trigger curiosity → link click."
    ),
    (
        "The 'Secret Tool' (Twitter Thread)",
        "✖️ Twitter / X",
        "1/5 Manual trading is DEAD. 💀\n\nHere is why Wall Street banks always win: ALGORITHMS.\n\n2/5 I found a retail-friendly AI Copytrade tool consistent with institutional standards.\n\n3/5 No emotional decisions. Pure data execution.\n\n4/5 Join the syndicate here: [YOUR LINK]\n\n5/5 Don't get left behind. #Crypto #Forex #Fintech",
        "📖 TARGET: English-speaking traders.\n⏰ WAKTU POST: 2-4 PM EST.\n🎯 GOAL: Authority building → thread engagement."
    ),
    (
        "The 'Lifestyle' Flex (IG Story)",
        "📸 Instagram Story",
        "Lagi liburan tapi duit ngalir terus? 🏖️💸\n\nThanks to AI Copytrade system yang jalan otomatis.\n\nDM 'MAU' kalau lo pengen tau caranya! 👇",
        "📖 TARGET: Lifestyle-oriented, 20-30.\n⏰ WAKTU POST: 10 AM-12 PM (weekend).\n🎯 GOAL: DM leads → personal conversion."
    ),
    (
        "The 'Authority Play' (LinkedIn)",
        "💼 LinkedIn Post",
        "Excited to share a breakthrough in portfolio management.\n\nAfter 6 months testing AI-powered copytrade algorithms:\n→ 87% reduction in emotional trading decisions\n→ 24/7 market monitoring without manual intervention\n→ Consistent risk-adjusted returns\n\nThe future of retail trading isn't manual charting.\nIt's intelligent automation.\n\n#Fintech #AlgorithmicTrading #AIInvesting\n\n[YOUR LINK]",
        "📖 TARGET: Professionals, 30-50, finance.\n⏰ WAKTU POST: Tue-Thu 8-10 AM.\n🎯 GOAL: Credibility → website visit."
    ),
    (
        "The 'Testimonial Bait' (WhatsApp)",
        "💬 WhatsApp Status",
        "Baru 2 minggu pake AI trading ini...\n\n✅ Ga perlu buka chart tiap jam\n✅ Profit jalan sementara gw kerja\n✅ Bisa dicek dari HP\n\nYang mau tau caranya, chat gw aja. Gratis kok nanya 😄\n\n[YOUR LINK]",
        "📖 TARGET: Teman & kenalan langsung.\n⏰ WAKTU POST: 6-8 PM WIB.\n🎯 GOAL: Trust → referral sign-up."
    ),
    (
        "The 'Urgency Close' (Telegram)",
        "✈️ Telegram Group",
        "🔥 ATTENTION ALL MEMBERS 🔥\n\nSlot terbatas untuk AI Copytrade bulan ini.\n\nSisa 23 slot dari 100.\n\nSiapa cepat, dia dapat.\n\nDaftar → [YOUR LINK]\n\n❌ Setelah penuh, pendaftaran DITUTUP sampai bulan depan.",
        "📖 TARGET: Community members.\n⏰ WAKTU POST: Kapan saja (urgency).\n🎯 GOAL: Scarcity → immediate action."
    )
]

# Static AI Prompts Data (non-video)
STATIC_PROMPTS = [
    (
        "📅 30-Day Content Calendar",
        "ChatGPT",
        "https://chat.openai.com/",
        json.dumps({
            "platform": "ChatGPT / GPT-4",
            "type": "content_plan",
            "prompt": "Act as a professional financial influencer with 100K followers. Create a 30-day social media content calendar for TikTok & Twitter focusing on 'AI Trading Benefits'. Structure: Week 1 = Problem Awareness, Week 2 = Solution Introduction, Week 3 = Social Proof, Week 4 = FOMO & Urgency. Output as table: Day, Platform, Content Type, Caption, Hashtags.",
            "brand": "ITC Intelligence Copy Trading",
            "website": "www.TelegramCopyTrading.com"
        }, indent=2),
        "💡 Copy → paste di ChatGPT → dapatkan kalender 30 hari."
    ),
    (
        "🖼️ Futuristic Dashboard Visual",
        "Midjourney",
        "https://www.midjourney.com/",
        json.dumps({
            "platform": "Midjourney v6",
            "type": "image",
            "prompt": "/imagine prompt: sleek futuristic holographic trading dashboard interface floating in dark room, neon green and gold data streams, candlestick charts with glowing profit indicators, text 'ITC Intelligence Copy Trading', cyberpunk aesthetic, ultra detailed, 8k, cinematic volumetric lighting --ar 16:9 --v 6",
            "use_case": "Social media banner, website hero image"
        }, indent=2),
        "💡 Gunakan sebagai banner IG, header Twitter, atau hero image."
    ),
    (
        "📊 IG Story Profit Banner",
        "DALL-E / ChatGPT",
        "https://chat.openai.com/",
        json.dumps({
            "platform": "DALL-E 3 (via ChatGPT)",
            "type": "image",
            "prompt": "Sleek dark-themed IG Story (1080x1920) showing smartphone with green profit chart, text 'ITC Intelligence Copy Trading' and 'www.TelegramCopyTrading.com', minimalist, black and neon green, professional fintech aesthetic",
            "resolution": "1080x1920 (IG Story)"
        }, indent=2),
        "💡 Buka ChatGPT → aktifkan DALL-E → paste → save."
    ),
    (
        "📺 YouTube Thumbnail",
        "Midjourney",
        "https://www.midjourney.com/",
        json.dumps({
            "platform": "Midjourney v6",
            "type": "image",
            "prompt": "/imagine prompt: YouTube thumbnail, confident trader in dark hoodie looking at camera, glowing green holographic trading chart behind, text space on right, dramatic lighting, ultra realistic, vibrant neon green on dark background, text 'ITC' --ar 16:9 --v 6",
            "resolution": "1280x720"
        }, indent=2),
        "💡 Tambahkan judul video di Canva setelah generate."
    ),
    (
        "✍️ WhatsApp Copywriting Pack",
        "ChatGPT",
        "https://chat.openai.com/",
        json.dumps({
            "platform": "ChatGPT / GPT-4",
            "type": "copywriting",
            "prompt": "Write 10 WhatsApp broadcast messages to promote ITC Intelligence Copy Trading (www.TelegramCopyTrading.com). Each: max 3 lines, casual Indonesian, 1-2 emojis, soft CTA. Vary angles: curiosity, social proof, urgency, lifestyle, authority.",
            "language": "Bahasa Indonesia (casual)"
        }, indent=2),
        "💡 10 template WA broadcast siap kirim."
    )
]

# Arsenal Tools Data
ARSENAL_TOOLS = [
    ("Google Veo", "https://deepmind.google/technologies/veo/", "AI Video Generator — buat video 8s dari prompt teks", "🎬"),
    ("CapCut", "https://www.capcut.com/", "Video Editor terbaik di HP — edit, subtitle, efek", "✂️"),
    ("Canva", "https://www.canva.com/", "Design banner, poster, IG Story template", "🎨"),
    ("ChatGPT", "https://chat.openai.com/", "Copywriting, content calendar, brainstorming", "🤖"),
    ("Midjourney", "https://www.midjourney.com/", "Generate gambar premium untuk marketing visual", "🖼️"),
    ("Remove.bg", "https://www.remove.bg/", "Hapus background foto — untuk screenshot & mockup", "🧹"),
    ("ElevenLabs", "https://elevenlabs.io/", "AI Voiceover — narasi video tanpa rekam suara", "🎙️"),
    ("Opus Clip", "https://www.opus.pro/", "Auto-potong video panjang jadi short clips viral", "📱")
]


class MarketingVaultView(ctk.CTkFrame):
    """Marketing Vault — Academy of Titans v5.3.2"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#101014")
        self.controller = controller
        self._is_generating = False
        
        try:
            self._setup_ui()
        except Exception as e:
            print(f"ERROR INIT MARKETING VAULT: {e}")
            import traceback
            traceback.print_exc()
            ctk.CTkLabel(self, text=f"Error loading Vault: {e}", text_color="red").pack(pady=20)
        
    def _setup_ui(self):
        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color="#1A1B22", height=60)
        header.pack(fill="x", padx=20, pady=20)
        
        btn_back = ctk.CTkButton(header, text="← BACK", width=80, fg_color="transparent", 
                                 text_color="gray", hover_color="#222", 
                                 command=lambda: self.controller.show_page("merchant"))
        btn_back.pack(side="left", padx=10)
        
        ctk.CTkLabel(header, text="ACADEMY OF TITANS 🏛️", font=("Roboto", 16, "bold"), text_color="#FFD700").pack(side="left", padx=10)
        ctk.CTkLabel(header, text="| MARKETING WAR CHEST", font=("Roboto", 12), text_color="gray").pack(side="left")

        # --- FLOATING PILLS TAB NAVIGATION (Luxury Edition) ---
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.tab_selector = ctk.CTkSegmentedButton(nav_frame, 
                                                   values=["🔥 VIRAL SCRIPTS", "🤖 AI PROMPTS", "🛠️ ARSENAL"],
                                                   font=("Segoe UI Bold", 13),
                                                   height=45,
                                                   fg_color="#1A1B22",
                                                   selected_color="#FFD700", # Gold selection
                                                   selected_hover_color="#E5C400",
                                                   unselected_color="#1A1B22",
                                                   unselected_hover_color="#2A2A2F",
                                                   text_color="#888",
                                                   command=self._on_tab_change)
        self.tab_selector.pack(fill="x")
        self.tab_selector.set("🔥 VIRAL SCRIPTS")
        
        # --- CONTENT AREA ---
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Build individual tab frames (initially hidden)
        self.frame_scripts = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.frame_prompts = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.frame_tools = ctk.CTkFrame(self.content_container, fg_color="transparent")
        
        self._build_scripts_tab(self.frame_scripts)
        self._build_prompts_tab(self.frame_prompts)
        self._build_tools_tab(self.frame_tools)
        
        # Default show first
        self.frame_scripts.pack(fill="both", expand=True)

    def _on_tab_change(self, value):
        """Switches content frames based on segmented button selection"""
        # Hide all
        self.frame_scripts.pack_forget()
        self.frame_prompts.pack_forget()
        self.frame_tools.pack_forget()
        
        # Show selected
        if "SCRIPTS" in value:
            self.frame_scripts.pack(fill="both", expand=True)
        elif "PROMPTS" in value:
            self.frame_prompts.pack(fill="both", expand=True)
        elif "ARSENAL" in value:
            self.frame_tools.pack(fill="both", expand=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1: VIRAL SCRIPTS
    # ══════════════════════════════════════════════════════════════════════════
    def _build_scripts_tab(self, parent):
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        for title, platform_badge, content, brief in VIRAL_SCRIPTS:
            card = ctk.CTkFrame(scroll, fg_color="#1A1B22", corner_radius=10)
            card.pack(fill="x", pady=8, padx=10)
            
            # Title Row
            title_row = ctk.CTkFrame(card, fg_color="transparent")
            title_row.pack(fill="x", padx=15, pady=(15, 5))
            ctk.CTkLabel(title_row, text=title, font=("Roboto", 12, "bold"), text_color="#2CC985").pack(side="left")
            ctk.CTkLabel(title_row, text=platform_badge, font=("Consolas", 10), text_color="#888").pack(side="right")
            
            # Script Content
            box = ctk.CTkTextbox(card, height=100, fg_color="#111", text_color="#ccc", font=("Consolas", 11))
            box.insert("1.0", content)
            box.configure(state="disabled")
            box.pack(fill="x", padx=15, pady=5)
            
            # Marketing Brief
            ctk.CTkLabel(card, text=brief, font=("Segoe UI", 10), text_color="#666",
                         justify="left", anchor="w", wraplength=500).pack(fill="x", padx=15, pady=(0, 5))
            
            # Copy Button
            ctk.CTkButton(card, text="📋 COPY SCRIPT", width=130, height=30, fg_color="#333", hover_color="#444",
                          font=("Segoe UI Bold", 10),
                          command=lambda c=content: self._copy_to_clipboard(c)).pack(anchor="e", padx=15, pady=(0, 15))

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2: AI PROMPTS (AI VIDEO GENERATOR + STATIC PROMPTS)
    # ══════════════════════════════════════════════════════════════════════════
    def _build_prompts_tab(self, parent):
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        # --- AI VIDEO PROMPT GENERATOR (Featured Card) ---
        self._build_veo_generator_card(scroll)
        
        # --- Separator ---
        ctk.CTkLabel(scroll, text="━━━━ OTHER AI PROMPTS ━━━━", font=("Consolas", 10), 
                     text_color="#333").pack(pady=15)
        
        # --- Static Prompts ---
        for title, platform, link, prompt_json, how_to in STATIC_PROMPTS:
            card = ctk.CTkFrame(scroll, fg_color="#1A1B22", corner_radius=10)
            card.pack(fill="x", pady=8, padx=10)
            
            # Title Row
            title_row = ctk.CTkFrame(card, fg_color="transparent")
            title_row.pack(fill="x", padx=15, pady=(15, 5))
            ctk.CTkLabel(title_row, text=title, font=("Roboto", 12, "bold"), text_color="#3B8ED0").pack(side="left")
            ctk.CTkLabel(title_row, text=f"via {platform}", font=("Consolas", 10), text_color="#888").pack(side="left", padx=10)
            
            ctk.CTkButton(title_row, text="OPEN ↗", width=70, height=24, fg_color="#444", hover_color="#555",
                          font=("Segoe UI", 9, "bold"),
                          command=lambda l=link: webbrowser.open(l)).pack(side="right")
            
            # Prompt Content
            box = ctk.CTkTextbox(card, height=120, fg_color="#0A0A0A", text_color="#FFD700", font=("Consolas", 10))
            box.insert("1.0", prompt_json)
            box.configure(state="disabled")
            box.pack(fill="x", padx=15, pady=5)
            
            # How To Use
            ctk.CTkLabel(card, text=how_to, font=("Segoe UI", 10), text_color="#666",
                         justify="left", anchor="w", wraplength=500).pack(fill="x", padx=15, pady=(0, 5))
            
            # Actions
            ctk.CTkButton(card, text="📋 COPY PROMPT", width=130, height=30, fg_color="#333", hover_color="#444",
                          font=("Segoe UI Bold", 10),
                          command=lambda p=prompt_json: self._copy_to_clipboard(p)).pack(anchor="e", padx=15, pady=(0, 15))

    def _build_veo_generator_card(self, parent):
        """Interactive AI Video Prompt Generator — Featured Card"""
        card = ctk.CTkFrame(parent, fg_color="#0D1117", corner_radius=12, 
                            border_width=2, border_color="#FFD700")
        card.pack(fill="x", pady=10, padx=10)
        
        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(header, text="🎬 AI VIDEO PROMPT GENERATOR", 
                     font=("Roboto", 14, "bold"), text_color="#FFD700").pack(side="left")
        ctk.CTkLabel(header, text="Powered by ITC AI Engine", 
                     font=("Consolas", 9), text_color="#555").pack(side="right")
        
        ctk.CTkLabel(card, text="Generate unique branded video prompts for Google Veo, RunwayML, Kling AI & more",
                     font=("Segoe UI", 10), text_color="#888").pack(anchor="w", padx=15, pady=(0, 10))
        
        # Prompt Display Textbox
        self.veo_textbox = ctk.CTkTextbox(card, height=250, fg_color="#0A0A0A", 
                                          text_color="#00FFAA", font=("Consolas", 10),
                                          wrap="word")
        self.veo_textbox.insert("1.0", '{\n  "title": "Click 🎲 GENERATE to create a unique video prompt",\n  "brand": "ITC Intelligence Copy Trading",\n  "website": "www.TelegramCopyTrading.com",\n  "hint": "Each click generates a completely different prompt!"\n}')
        self.veo_textbox.configure(state="disabled")
        self.veo_textbox.pack(fill="x", padx=15, pady=5)
        
        # Status Label
        self.veo_status = ctk.CTkLabel(card, text="", font=("Segoe UI", 10), text_color="#FFD700")
        self.veo_status.pack(anchor="w", padx=15)
        
        # Action Row
        action_row = ctk.CTkFrame(card, fg_color="transparent")
        action_row.pack(fill="x", padx=15, pady=(5, 10))
        
        self.btn_generate = ctk.CTkButton(action_row, text="🎲 GENERATE NEW", width=150, height=36,
                                          fg_color="#FFD700", text_color="black", hover_color="#E5C400",
                                          font=("Segoe UI Bold", 11),
                                          command=self._generate_veo_prompt)
        self.btn_generate.pack(side="left", padx=(0, 10))
        
        self.btn_copy_veo = ctk.CTkButton(action_row, text="📋 COPY PROMPT", width=140, height=36,
                                          fg_color="#333", text_color="white", hover_color="#444",
                                          font=("Segoe UI Bold", 11),
                                          command=self._copy_veo_prompt)
        self.btn_copy_veo.pack(side="left")
        
        ctk.CTkButton(action_row, text="OPEN VEO ↗", width=100, height=36,
                      fg_color="#1A1A2E", text_color="#888", hover_color="#222",
                      font=("Segoe UI", 10),
                      command=lambda: webbrowser.open("https://deepmind.google/technologies/veo/")).pack(side="right")
        
        # Audio Note
        ctk.CTkLabel(card, text="ℹ️ Prompt sudah include audio (musik, voiceover, SFX). Veo 3+ akan generate audio native.\n    Untuk Veo 2 atau AI video lain, tambahkan audio via CapCut / ElevenLabs setelah generate video.",
                     font=("Segoe UI", 9), text_color="#555", justify="left", anchor="w",
                     wraplength=550).pack(fill="x", padx=15, pady=(0, 15))

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3: ARSENAL (TOOLS + LINKS)
    # ══════════════════════════════════════════════════════════════════════════
    def _build_tools_tab(self, parent):
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        for title, link, desc, emoji in ARSENAL_TOOLS:
            card = ctk.CTkFrame(scroll, fg_color="#1A1B22", corner_radius=10)
            card.pack(fill="x", pady=5, padx=10)
            
            left = ctk.CTkFrame(card, fg_color="transparent")
            left.pack(side="left", fill="x", expand=True, padx=15, pady=12)
            
            ctk.CTkLabel(left, text=f"{emoji}  {title}", font=("Roboto", 12, "bold"), text_color="white",
                         anchor="w").pack(anchor="w")
            ctk.CTkLabel(left, text=desc, font=("Segoe UI", 10), text_color="#888",
                         anchor="w").pack(anchor="w", pady=(2, 0))
            
            ctk.CTkButton(card, text="OPEN LINK ↗", width=110, height=32, fg_color="#444", hover_color="#555",
                          font=("Segoe UI Bold", 10),
                          command=lambda l=link: webbrowser.open(l)).pack(side="right", padx=15, pady=12)

    # ══════════════════════════════════════════════════════════════════════════
    # HANDLERS
    # ══════════════════════════════════════════════════════════════════════════
    def _copy_to_clipboard(self, text):
        """Copy text to system clipboard."""
        self.clipboard_clear()
        self.clipboard_append(text)
        CTkMessagebox(title="Copied", message="Content copied to clipboard!", icon="check")

    def _copy_veo_prompt(self):
        """Copy current Veo prompt from textbox."""
        content = self.veo_textbox.get("1.0", "end-1c")
        if content and "Click" not in content[:20]:
            self.clipboard_clear()
            self.clipboard_append(content)
            CTkMessagebox(title="Copied", message="Video prompt copied to clipboard!", icon="check")
        else:
            CTkMessagebox(title="Info", message="Generate a prompt first!", icon="info")

    def _generate_veo_prompt(self):
        """Generate a unique AI video prompt using the AI waterfall engine."""
        if self._is_generating:
            return
        
        self._is_generating = True
        self.btn_generate.configure(state="disabled", text="⏳ Generating...")
        self.veo_status.configure(text="🔄 Connecting to AI Engine...", text_color="#FFD700")
        
        def _task():
            try:
                # Import AI waterfall from index
                from index import execute_ai_waterfall
                
                self.veo_status.configure(text="🧠 AI is crafting your video prompt...")
                
                # Call the AI waterfall with the video prompt system context
                result = execute_ai_waterfall(
                    "COMPANION_CHAT",
                    VEO_USER_PROMPT,
                    VEO_SYSTEM_PROMPT
                )
                
                if not result or "Error" in str(result) or "Exhausted" in str(result):
                    self._update_veo_display(None, f"AI Error: {result}")
                    return
                
                # Clean & validate JSON
                cleaned = self._clean_json_response(result)
                
                try:
                    parsed = json.loads(cleaned)
                    # Ensure branding is present
                    if "text_overlay" not in parsed:
                        parsed["text_overlay"] = "ITC Intelligence Copy Trading\nwww.TelegramCopyTrading.com"
                    
                    formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
                    self._update_veo_display(formatted, None)
                except json.JSONDecodeError:
                    # AI returned non-JSON, display raw but warn
                    self._update_veo_display(cleaned, "⚠️ AI returned non-standard format. Content may need manual adjustment.")
                    
            except Exception as e:
                self._update_veo_display(None, f"Error: {e}")
            finally:
                self._is_generating = False
                if self.winfo_exists():
                    self.btn_generate.configure(state="normal", text="🎲 GENERATE NEW")
        
        threading.Thread(target=_task, daemon=True).start()

    def _clean_json_response(self, raw_text):
        """Clean AI response to extract valid JSON."""
        text = str(raw_text).strip()
        
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json", 1)[1]
            if "```" in text:
                text = text.split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1]
            if "```" in text:
                text = text.split("```", 1)[0]
        
        # Try to find JSON object boundaries
        text = text.strip()
        start = text.find("{")
        end = text.rfind("}")
        
        if start != -1 and end != -1 and end > start:
            text = text[start:end + 1]
        
        return text.strip()

    def _update_veo_display(self, json_text, error_msg):
        """Thread-safe update of the Veo textbox."""
        def _ui():
            if not self.winfo_exists():
                return
            self.veo_textbox.configure(state="normal")
            self.veo_textbox.delete("1.0", "end")
            
            if json_text:
                self.veo_textbox.configure(text_color="#00FFAA")
                self.veo_textbox.insert("1.0", json_text)
                self.veo_status.configure(text="✅ Prompt generated! Click COPY or GENERATE NEW for a different one.", 
                                          text_color="#00FFAA")
            elif error_msg:
                self.veo_textbox.configure(text_color="#FF4444")
                self.veo_textbox.insert("1.0", error_msg)
                self.veo_status.configure(text="❌ Generation failed. Try again.", text_color="#FF4444")
            
            self.veo_textbox.configure(state="disabled")
        
        try:
            self.after(0, _ui)
        except Exception:
            pass
