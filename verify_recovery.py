import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))

from modules.logic.smart_fill import SmartFill
from index import get_env_list

def verify_recovery():
    env = get_env_list()
    print("Testing Data Density Recovery (Source: Skynet Deep Search)...")
    events = SmartFill.get_calendar_events(env, force_refresh=True)
    print(f"Total Events Found: {len(events)}")
    if len(events) > 0:
        for e in events[:10]:
            print(f"- {e.get('date')} {e.get('time')} | {e.get('currency')} | {e.get('event')} | Impact: {e.get('impact')} | Prev: {e.get('previous', '-')}")
    else:
        print("CRITICAL: Zero events found.")

if __name__ == "__main__":
    verify_recovery()
