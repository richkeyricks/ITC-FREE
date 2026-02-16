# tests/verify_smart_fill.py
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from modules.logic.smart_fill import SmartFill
from index import get_env_list

def test_smart_fill_fallback():
    print("\n--- [TEST: SMARTFILL FALLBACK] ---")
    load_dotenv(override=True)
    env = get_env_list()
    
    mock_signal = {
        "symbol": "XAUUSD",
        "type": "BUY",
        "entry": 2600.0,
        "sl": 2580.0,
        "tp": 2650.0
    }
    
    mock_tech = {
        "TREND": "Bullish",
        "RSI": "60 (Strong)",
        "EMA_CROSS": "EMA 50/100 Bullish Cross"
    }
    
    # Test _generate_narrative chain
    print("Generating Narrative via SmartFill...")
    result = SmartFill._generate_narrative(mock_signal, mock_tech, env)
    
    if result and "ANALYSIS_REASON" in result:
        print(f"✅ SmartFill SUCCESS: {result['SIGNAL_POWER']}")
        print(f"Confidence: {result['CONFIDENCE_SCORE']}")
    else:
        print("❌ SmartFill FAILED to return expected keys")

if __name__ == "__main__":
    test_smart_fill_fallback()
    print("\n--- [VERIFICATION COMPLETE] ---")
