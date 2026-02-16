import os
import sys
import json
from datetime import datetime, timedelta

# Mock App Environment context
sys.path.append(os.path.join(os.getcwd(), "src"))
from modules.logic.smart_fill import SmartFill
from index import get_env_list

def test_sorting():
    print("// --- TUHAN GRADE SORTING & ALIGNMENT TEST --- //")
    env = get_env_list()
    
    print("// [DEBUG] Fetching fresh data...")
    events = SmartFill.get_calendar_events(env, force_refresh=True)
    
    print(f"\n// [RESULT] Total Events: {len(events)}")
    
    print("\n// --- CHRONOLOGICAL VERIFICATION --- //")
    last_key = ""
    sorted_correctly = True
    for i, e in enumerate(events[:15]):
        current_key = e.get("_sort_key", "")
        print(f"{i+1:2d}. [{current_key}] {e.get('currency'):3s} - {e.get('event')}")
        if current_key < last_key:
            sorted_correctly = False
        last_key = current_key
    
    if sorted_correctly:
        print("\n// [SUCCESS] Chronological order verified.")
    else:
        print("\n// [FAILURE] Sorting drift detected!")

if __name__ == "__main__":
    test_sorting()
