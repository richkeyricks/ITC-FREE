# src/configs/ai_config.py
"""
Centralized configuration for AI services.
Follows Gravity Dev Rules: Centralized & Structured.
"""

# Master Fallback Key
MASTER_GROQ_KEY = ""
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"

# 3-TIER WATERFALL MATRIX
# T1: Groq, T2: OpenRouter (for Gemini), T3: Cloudflare/Ollama
AI_WATERFALL_MATRIX = {
    "SIGNAL_PARSING": {
        "T1": {"provider": "Groq", "model": "llama-3.3-70b-versatile"},
        "T2": {"provider": "OpenRouter", "model": "google/gemini-pro-1.5"},
        "T3": {"provider": "Cloudflare", "model": "@cf/meta/llama-3.1-70b-instruct"}
    },
    "SMART_FILL": {
        "T1": {"provider": "Groq", "model": "llama-3.3-70b-versatile"},
        "T2": {"provider": "OpenRouter", "model": "google/gemini-pro-1.5"},
        "T3": {"provider": "Cloudflare", "model": "@cf/meta/llama-3.1-70b-instruct"}
    },
    "COMPANION_CHAT": {
        "T1": {"provider": "Groq", "model": "llama-3.1-8b-instant"},
        "T2": {"provider": "OpenRouter", "model": "google/gemini-flash-1.5"},
        "T3": {"provider": "Ollama", "model": "llama3.2"}
    },
    "QUIZ_GEN": {
        "T1": {"provider": "Groq", "model": "llama-3.3-70b-versatile"},
        "T2": {"provider": "OpenRouter", "model": "google/gemini-pro-1.5"},
        "T3": {"provider": "Cloudflare", "model": "@cf/meta/llama-3.1-8b-instant"}
    },
    "VISION_ANALYSIS": {
        "T1": {"provider": "Groq", "model": "llama-3.2-11b-vision-preview"},
        "T2": {"provider": "OpenRouter", "model": "google/gemini-flash-1.5"},
        "T3": {"provider": "OpenRouter", "model": "anthropic/claude-3-haiku"}
    },
    "CALENDAR_PARSER": {
        "T1": {"provider": "Groq", "model": "llama-3.3-70b-versatile"},
        "T2": {"provider": "OpenRouter", "model": "google/gemini-pro-1.5"},
        "T3": {"provider": "Cloudflare", "model": "@cf/meta/llama-3.1-70b-instruct"}
    },
    "NEWS_ANALYSIS": {
        "T1": {"provider": "Groq", "model": "llama-3.3-70b-versatile"},
        "T2": {"provider": "OpenRouter", "model": "google/gemini-pro-1.5"},
        "T3": {"provider": "Cloudflare", "model": "@cf/meta/llama-3.1-70b-instruct"}
    },
    "EVENT_ANALYSIS": {
        "T1": {"provider": "Groq", "model": "llama-3.3-70b-versatile"},
        "T2": {"provider": "OpenRouter", "model": "google/gemini-pro-1.5"},
        "T3": {"provider": "Cloudflare", "model": "@cf/meta/llama-3.1-70b-instruct"}
    }
}

# AI Limits
AI_TRIAL_LIMIT = 3
AI_QUIZ_REWARD = 3
