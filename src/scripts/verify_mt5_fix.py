
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from modules.mt5.mt5_service import MT5Service

def verify_detection():
    service = MT5Service.instance()
    print("Testing MT5Service.get_active_chart()...")
    
    chart = service.get_active_chart()
    
    if chart:
        print("\nSUCCESS!")
        print(f"Detected Symbol: {chart['symbol']}")
        print(f"Detected Timeframe: {chart['timeframe']}")
        print(f"Current Price: {chart['price']}")
    else:
        print("\nFAILURE: Still no chart detected.")

if __name__ == "__main__":
    verify_detection()
