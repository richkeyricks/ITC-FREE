# tests/verify_ai_fallback.py
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from index import ai_parse_signal, chat_with_ai, get_env_list
from modules.ai.chart_analyzer import AIChartAnalyzer
from configs.ai_config import (
    PARSING_TIER_1, PARSING_TIER_2, PARSING_TIER_3,
    VISION_TIER_1, VISION_TIER_2, VISION_TIER_3
)

def test_parsing_fallback():
    print("\n--- [TEST 1: PARSING FALLBACK] ---")
    text = "BUY GOLD AT 2300 SL 2280 TP 2350"
    print(f"Feeding signal text: {text}")
    
    # We simulate Tier 1 failure by using an invalid key momentarily or just checking the chain
    # For now, we test the robust clean extraction
    result = ai_parse_signal(text, "invalid_key")
    if result and "symbol" in result:
        print(f"✅ Parsing SUCCESS: {result}")
    else:
        print("❌ Parsing FAILED")

def test_chat_fallback():
    print("\n--- [TEST 2: CHAT FALLBACK] ---")
    prompt = "Halo ITC AI, apa kabar?"
    # chat_with_ai handles fallbacks internally
    response = chat_with_ai(prompt, "dummy_key", provider="Groq")
    print(f"🤖 AI Response: {response[:100]}...")
    if "Maaf" not in response:
        print("✅ Chat Fallback/Chain SUCCESS")
    else:
        print("❌ Chat Fallback FAILED")

def test_vision_fallback():
    print("\n--- [TEST 3: VISION FALLBACK] ---")
    analyzer = AIChartAnalyzer()
    # Mocking components for test if no image exists
    print(f"Tier 1: {VISION_TIER_1}")
    print(f"Tier 2: {VISION_TIER_2}")
    print(f"Tier 3: {VISION_TIER_3}")
    print("Logic: Groq -> OpenRouter -> Ollama")
    # This requires an actual image. We'll skip execution but verify the method exists.
    if hasattr(analyzer, 'analyze_chart'):
        print("✅ Vision Fallback Logic Method FOUND")

if __name__ == "__main__":
    load_dotenv(override=True)
    test_parsing_fallback()
    test_chat_fallback()
    test_vision_fallback()
    print("\n--- [VERIFICATION COMPLETE] ---")
