import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))

from modules.logic.smart_fill import SmartFill
from index import get_env_list, execute_ai_waterfall

def verify_ai_briefing():
    env = get_env_list()
    print("Testing AI Waterfall (Feature: EVENT_ANALYSIS)...")
    
    mock_event = {
        "event": "FOMC Interest Rate Decision",
        "currency": "USD",
        "impact": "High",
        "forecast": "5.5%",
        "previous": "5.5%"
    }
    
    prompt = (
        f"Act as an Elite Hedge Fund Trader. Provide a TACTICAL BRIEFING for this event:\n"
        f"EVENT: {mock_event['event']}\n"
        f"CURRENCY: {mock_event['currency']}\n"
        f"IMPACT: {mock_event['impact']}\n\n"
        f"Requirements:\n"
        f"1. Tactical Scenario.\n"
        f"Keep it concise (Markdown)."
    )
    
    try:
        result = execute_ai_waterfall(
            feature_key="EVENT_ANALYSIS",
            prompt=prompt,
            system_context="You are a senior hedge fund trader providing high-end tactical briefings.",
            user_api_key=env.get("AI_API_KEY", ""),
            user_provider=env.get("AI_PROVIDER", "Groq")
        )
        print("\n--- AI RESPONSE ---")
        print(result)
        print("-------------------\n")
        
        if "Invalid Feature Key" in result:
            print("FAILURE: Still getting Invalid Feature Key error.")
        elif "All AI Tiers Exhausted" in result:
             print("WARNING: All AI Tiers Exhausted (Key issue or Rate limit).")
        else:
            print("SUCCESS: AI response received.")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    verify_ai_briefing()
