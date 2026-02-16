
import sys
from datetime import datetime

def test_parse():
    # The string reporting the error
    date_str = "2026-03-18T11:06:05.82435+00:00"
    print(f"Testing string: '{date_str}'")
    print(f"Python version: {sys.version}")

    try:
        # Standard check
        dt = datetime.fromisoformat(date_str)
        print(f"✅ Success (fromisoformat): {dt}")
    except Exception as e:
        print(f"❌ Failed (fromisoformat): {e}")

    try:
        from dateutil import parser
        dt = parser.isoparse(date_str)
        print(f"✅ Success (dateutil): {dt}")
    except ImportError:
        print("⚠️ dateutil not installed")
    except Exception as e:
        print(f"❌ Failed (dateutil): {e}")

    try:
        # Manual Padding Logic
        # 1. Normalize Z
        s = date_str.replace("Z", "+00:00")
        # 2. Check for microseconds
        if "." in s:
            head, tail = s.split(".")
            # tail is like "82435+00:00" or "82435"
            if "+" in tail:
                micros, tz = tail.split("+")
                tz = "+" + tz
            elif "-" in tail: # Handle negative offset? Complex if just date
                # Simplified for +00:00 case
                parts = tail.split("-")
                micros = parts[0]
                tz = "-" + parts[1] if len(parts) > 1 else ""
            else:
                micros = tail
                tz = ""
            
            # Pad micros to 6 digits
            micros = micros.ljust(6, "0")[:6]
            fixed_str = f"{head}.{micros}{tz}"
            print(f"Fixed String: {fixed_str}")
            dt = datetime.fromisoformat(fixed_str)
            print(f"✅ Success (Manual Pad): {dt}")
        else:
            # No fractional seconds
            dt = datetime.fromisoformat(s)
            print(f"✅ Success (No Micros): {dt}")
            
    except Exception as e:
        print(f"❌ Failed (Manual Pad): {e}")

if __name__ == "__main__":
    test_parse()
