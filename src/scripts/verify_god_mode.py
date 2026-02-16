
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from modules.mt5.mt5_service import MT5Service
from index import get_positions

def verify_god_mode():
    print("--- VERIFYING GOD MODE FEATURES ---")
    
    service = MT5Service.instance()
    
    # 1. Multi-Chart Test
    charts = service.get_all_open_charts()
    print(f"\n[1] Open Charts Detected: {len(charts)}")
    for i, c in enumerate(charts):
        print(f"    Chart {i+1}: {c['symbol']} ({c['timeframe']})")
    
    # 3. Terminal Health Test
    state = service.get_terminal_state()
    print(f"\n[3] Terminal State: Algo Trading: {state.get('algo_trading')} | Broker: {state.get('connected')}")

    # 4. Momentum / Rates Test
    if charts:
        symbol = charts[0]['symbol']
        rates = service.get_recent_rates(symbol, "H1", count=3)
        print(f"\n[4] Momentum Test ({symbol} H1):")
        for r in rates:
            print(f"    Close: {r['close']} | Vol: {r['tick_volume']}")

if __name__ == "__main__":
    verify_god_mode()
