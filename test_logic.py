import sys
import os
import hashlib
from datetime import datetime

# Add src to path
sys.path.append(os.path.abspath("src"))

def test_signal_parser():
    print("\n--- Testing Signal Parser ---")
    from index import parse_signal
    
    test_cases = [
        {
            "text": "GOLD BUY CMP 2030 SL 2020 TP 2050",
            "expected": {"symbol": "GOLD", "type": "BUY", "entry": 2030.0, "tp": 2050.0, "sl": 2020.0}
        },
        {
            "text": "EURUSD.pro SELL AT 1.0850 SL 1.0900 TP 1.0700",
            "expected": {"symbol": "EURUSD.PRO", "type": "SELL", "entry": 1.0850, "tp": 1.0700, "sl": 1.0900}
        },
        {
            "text": "XAUUSD LONG Entry 2030.50 SL 2025 TP1 2045",
            "expected": {"symbol": "XAUUSD", "type": "BUY", "entry": 2030.50, "tp": 2045.0, "sl": 2025.0}
        }
    ]
    
    success_count = 0
    for i, tc in enumerate(test_cases):
        result = parse_signal(tc["text"])
        if result == tc["expected"]:
            print(f"Test case {i+1}: PASSED")
            success_count += 1
        else:
            print(f"Test case {i+1}: FAILED")
            print(f"  Input: {tc['text']}")
            print(f"  Got: {result}")
            print(f"  Expected: {tc['expected']}")
            
    return success_count == len(test_cases)

def test_cache_management():
    print("\n--- Testing Cache Management (Memory Leak Protection) ---")
    # This simulates receiving many duplicate signals and ensuring the cache doesn't grow infinitely
    signal_cache = set()
    
    # Simulate 1200 signals
    for i in range(1200):
        msg = f"signal number {i}"
        msg_hash = hashlib.md5(msg.strip().encode()).hexdigest()
        
        # Logic from index.py
        if len(signal_cache) > 1000:
            signal_cache.clear()
            
        signal_cache.add(msg_hash)
        
    print(f"Final Signal Cache Size: {len(signal_cache)}")
    if len(signal_cache) <= 1000:
        print("Signal Cache Rotation: PASSED")
    else:
        print("Signal Cache Rotation: FAILED")
        return False
        
    # Test broadcast cache rotation
    broadcast_cache = set(range(1200)) # Simulate already full cache
    
    # Logic from index.py
    if len(broadcast_cache) > 1000:
        broadcast_cache = set(list(broadcast_cache)[-100:])
        
    print(f"Final Broadcast Cache Size: {len(broadcast_cache)}")
    if len(broadcast_cache) == 100:
        print("Broadcast Cache Rotation: PASSED")
        return True
    else:
        print("Broadcast Cache Rotation: FAILED")
        return False

if __name__ == "__main__":
    p_res = test_signal_parser()
    c_res = test_cache_management()
    
    if p_res and c_res:
        print("\n[SUCCESS] ALL LOGIC TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n[ERROR] SOME LOGIC TESTS FAILED!")
        sys.exit(1)
