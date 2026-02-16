import os
import sys
import json
from datetime import datetime, timedelta

# Mock App Environment context
sys.path.append(os.path.join(os.getcwd(), "src"))
from modules.logic.smart_fill import SmartFill
from index import get_env_list

def test():
    print("// --- TUHAN GRADE CALENDAR DENSITY TEST --- //")
    env = get_env_list()
    
    # 1. Force Refresh
    print("// [DEBUG] Triggering Hard-Refresh with Density Enforcement...")
    events = SmartFill.get_calendar_events(env, force_refresh=True)
    
    print(f"\n// [RESULT] Total Events Found: {len(events)}")
    
    # Check Density
    if len(events) >= 10:
        print("// [SUCCESS] Density Threshold PASSED (>10 items found).")
    else:
        print("// [FAILURE] Density Threshold FAILED (<10 items found).")
        
    print("\n// --- PREVIEW (Top 20) --- //")
    for i, e in enumerate(events[:20]):
        print(f"{i+1:2d}. [{e.get('date')}] {e.get('currency'):3s} - {e.get('impact'):6s} - {e.get('event')}")
        
    # Check for Monday items (Rollover Verification)
    monday_count = sum(1 for e in events if "Feb 16" in e.get('date') or "Monday" in e.get('date'))
    print(f"\n// [ROLLOVER Check] Monday (Feb 16) found: {monday_count} events.")

if __name__ == "__main__":
    test()
