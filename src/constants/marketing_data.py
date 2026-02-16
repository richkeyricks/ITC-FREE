"""
ITC Marketing & Empire Builder Data
Centralized constants for the 'Viral Boost Syndicate' and 'Leaderboard Ticker'.
"""

# --- SOCIAL PLATFORMS ---
# Templates for sharing. {link} will be replaced by the user's referral link.
# {code} will be replaced by the user's referral code.

SOCIAL_PLATFORMS = [
    {
        "name": "WhatsApp",
        "icon": "💬", # Placeholder for UI logic
        "color": "#25D366",
        "url_scheme": "https://wa.me/?text={text}",
        "template_id": "Bro, gw nemu *cheat code* trading. AI ini gila banget, profit gw naik 20% minggu ini. Cek sini: {link}",
        "template_en": "Bro, I found a trading *cheat code*. This AI is insane, my profit is up 20% this week. Check it out: {link}"
    },
    {
        "name": "Telegram",
        "icon": "✈️",
        "color": "#0088cc",
        "url_scheme": "https://t.me/share/url?url={link}&text={text}",
        "template_id": "🔥 **SIGNAL ALERT** 🔥 System Copytrade MT5 berbasis AI nomor 1. Join syndicate gw disini: {link} #PassiveIncome",
        "template_en": "🔥 **SIGNAL ALERT** 🔥 #1 AI-based MT5 Copytrade System. Join my syndicate here: {link} #PassiveIncome"
    },
    {
        "name": "Twitter / X",
        "icon": "✖️",
        "color": "#000000",
        "url_scheme": "https://twitter.com/intent/tweet?text={text}&url={link}",
        "template_id": "Manual trading is dead. Long live AI. 🤖📈 Join the revolution: {link} $BTC $XAUUSD #Fintech",
        "template_en": "Manual trading is dead. Long live AI. 🤖📈 Join the revolution: {link} $BTC $XAUUSD #Fintech"
    },
    {
        "name": "Facebook",
        "icon": "f",
        "color": "#1877F2",
        "url_scheme": "https://www.facebook.com/sharer/sharer.php?u={link}",
        "template_id": "Info A1 buat yang mau nambah income sampingan tanpa ribet analisa chart. DM me or click {link}",
        "template_en": "A1 Info for those who want side income without chart analysis hassle. DM me or click {link}"
    },
    {
        "name": "LinkedIn",
        "icon": "in",
        "color": "#0077b5",
        "url_scheme": "https://www.linkedin.com/sharing/share-offsite/?url={link}",
        "template_id": "Excited to share a breakthrough in algorithmic trading portfolio management. {link}",
        "template_en": "Excited to share a breakthrough in algorithmic trading portfolio management. {link}"
    },
    {
        "name": "TikTok",
        "icon": "🎵",
        "color": "#000000", # Usually handled by copy link + manual post
        "url_scheme": "", # No direct web share api for vid
        "template_id": "Stop trading pake perasaan! Liat ini... (Link in Bio)",
        "template_en": "Stop emotional trading! Watch this... (Link in Bio)"
    },
    {
        "name": "Instagram",
        "icon": "📸",
        "color": "#E1306C",
        "url_scheme": "", # Manual
        "template_id": "DM 'MAU' buat akses bot trading ini! 🤖💸",
        "template_en": "DM 'WANT' to access this trading bot! 🤖💸"
    },
     {
        "name": "Reddit",
        "icon": "🤖",
        "color": "#FF4500",
        "url_scheme": "https://www.reddit.com/submit?url={link}&title={text}",
        "template_id": "Found a legit MT5 copytrading tool with real AI backbone. AMA. {link}",
        "template_en": "Found a legit MT5 copytrading tool with real AI backbone. AMA. {link}"
    },
    {
        "name": "Pinterest",
        "icon": "📌",
        "color": "#BD081C",
        "url_scheme": "https://pinterest.com/pin/create/button/?url={link}&description={text}",
        "template_id": "Future of Wealth: AI Trading. Pin this for later! {link}",
        "template_en": "Future of Wealth: AI Trading. Pin this for later! {link}"
    },
    {
        "name": "Discord",
        "icon": "🎮",
        "color": "#5865F2",
        "url_scheme": "", # Manual
        "template_id": "Yo gamers, let your PC pay for your skins. 🎮💸 Check this: {link}",
        "template_en": "Yo gamers, let your PC pay for your skins. 🎮💸 Check this: {link}"
    },
    {
        "name": "Threads",
        "icon": "@",
        "color": "#000000",
        "url_scheme": "", # Manual
        "template_id": "Is manual trading obsolete? Discuss. 👇 {link}",
        "template_en": "Is manual trading obsolete? Discuss. 👇 {link}"
    },
    {
        "name": "Twitch",
        "icon": "📺",
        "color": "#9146FF",
        "url_scheme": "",
        "template_id": "Stream is up! Also check my passive income rig: {link}",
        "template_en": "Stream is up! Also check my passive income rig: {link}"
    },
    {
        "name": "Snapchat",
        "icon": "👻",
        "color": "#FFFC00",
        "url_scheme": "https://www.snapchat.com/scan?attachmentUrl={link}",
        "template_id": "Don't blink. 👻 {link}",
        "template_en": "Don't blink. 👻 {link}"
    },
    {
        "name": "Quora",
        "icon": "Q",
        "color": "#B92B27",
        "url_scheme": "",
        "template_id": "What is the best AI trading bot in 2026? I found this: {link}",
        "template_en": "What is the best AI trading bot in 2026? I found this: {link}"
    },
    {
        "name": "WeChat",
        "icon": "💬",
        "color": "#7BB32E",
        "url_scheme": "",
        "template_id": "Check this out: {link}",
        "template_en": "Check this out: {link}"
    },
    {
        "name": "Copy Link",
        "icon": "🔗",
        "color": "#555555",
        "url_scheme": "COPY",
        "template_id": "{link}",
        "template_en": "{link}"
    }
]

# --- LEADERBOARD NAMES (70 Ghosts) ---
# Natural, globally diverse names. NO public figures. NO celebrities.
# Distribution: ~21% ID/SEA, ~14% CN/JP/KR, ~14% ME/SA, ~21% Western, ~7% LATAM/AF, ~21% Aliases
LEADERBOARD_NAMES = [
    # Indonesia / Southeast Asia (15)
    "Budi_R92", "Eka_FX", "Dewi_T", "Rizky_Pro", "Sari_28",
    "Agus_MT5", "Wati_K", "Hadi_S99", "Putri_FX", "Dewa_88",
    "Andi_M", "Rina_T7", "Fajar_Pro", "Lina_S", "Yanto_FX",

    # China / Japan / Korea (10)
    "Chen_W88", "Liu_M7", "Wang_FX", "Tanaka_K", "Sato_T",
    "Park_JH", "Kim_SY", "Lee_Pro", "Nguyen_D", "Tran_88",

    # Middle East / South Asia (10)
    "Mohammed_K7", "Ali_FX", "Omar_T", "Yusuf_Pro",
    "Ibrahim_M", "Khalid_S", "Raj_T99", "Priya_FX",
    "Amir_K", "Hassan_88",

    # Western / US / EU (15)
    "James_T29", "Sarah_M", "Alex_Pro", "Mike_FX",
    "David_K7", "Emma_W", "Chris_88", "John_R",
    "Lisa_T", "Tom_K", "Ryan_FX", "Kevin_Pro",
    "Nick_M", "Daniel_S", "Sophie_T",

    # Latin America / Africa (5)
    "Carlos_FX", "Diego_M7", "Paulo_T", "Maria_GA", "Amira_K",

    # Trading Aliases (15)
    "FX_Master_22", "Gold_King_7", "Crypto_X", "Alpha_One",
    "Signal_Pro", "Neural_T", "Apex_88", "Phoenix_FX",
    "Quantum_7", "Swift_Trade", "Iron_Bull",
    "Shadow_FX", "Storm_Pro", "Titan_99", "Viper_FX"
]
