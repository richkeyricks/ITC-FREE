import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.join(os.getcwd(), "src"))
from modules.logic.smart_fill import SmartFill
from index import get_env_list

def verify():
    print("// --- GOD GRADE FINAL PERFECTION VERIFICATION --- //")
    env = get_env_list()
    # Force refresh
    events = SmartFill.get_calendar_events(env, force_refresh=True)
    
    print(f"\nTotal Clean Events: {len(events)}")
    print("-" * 65)
    print(f"{'#':<3} | {'Status':<10} | {'Sort Key':<20} | {'Cur':<5} | {'Event'}")
    print("-" * 65)
    
    garbage_keywords = ["calendar", "market", "volatility", "indicator", "forex", "daily", "weekly"]
    has_garbage = False
    sorting_error = False
    last_key = ""
    
    for i, e in enumerate(events[:20]):
        evt_name = e.get("event", "")
        sort_key = e.get("_sort_key", "??")
        cur = e.get("currency", "??")
        
        # Check Purity
        is_clean = not any(kw in evt_name.lower() for kw in garbage_keywords)
        purity_status = "CLEAN" if is_clean else "DIRTY!"
        if not is_clean: has_garbage = True
        
        # Check Sorting (Chronological)
        if last_key and sort_key < last_key:
            sorting_error = True
            sort_status = "ERR!"
        else:
            sort_status = "OK"
        
        last_key = sort_key
        
        print(f"{i+1:<3} | {purity_status:<10} | {sort_key:<20} | {cur:<5} | {evt_name[:40]}")

    print("-" * 65)
    if not has_garbage and not sorting_error and len(events) >= 10:
        print("\n// [SUCCESS] Purity & Chronological Sorting Verified.")
        print("// [INFO] Grid alignment must be verified visually via GUI.")
    else:
        if has_garbage: print("// [FAILURE] Garbage data detected!")
        if sorting_error: print("// [FAILURE] Sorting drift detected!")
        if len(events) < 10: print("// [FAILURE] Low data density!")

if __name__ == "__main__":
    verify()
