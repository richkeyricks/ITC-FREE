
import MetaTrader5 as mt5
import os
from dotenv import load_dotenv

def debug_charts():
    load_dotenv()
    
    login = int(os.getenv("MT5_LOGIN", 0))
    password = os.getenv("MT5_PASSWORD", "")
    server = os.getenv("MT5_SERVER", "")
    
    print(f"Connecting to MT5: {server} as {login}...")
    
    if not mt5.initialize(login=login, password=password, server=server):
        print(f"Failed to initialize MT5: {mt5.last_error()}")
        return

    print("Success: Connected to MT5.")
    
    # 1. Check Terminal Info
    info = mt5.terminal_info()
    if info:
        print(f"Terminal Info: {info.name} {info.path}")
    
    # 2. Check available chart methods
    attrs = dir(mt5)
    chart_methods = [a for a in attrs if 'chart' in a.lower()]
    print(f"Chart-related attributes in mt5: {chart_methods}")
    
    # Try chart_id if available
    if 'chart_first' in chart_methods:
        print(f"mt5.chart_first(): {mt5.chart_first()}")
    elif 'ChartFirst' in chart_methods:
        print(f"mt5.ChartFirst(): {mt5.ChartFirst()}")
    else:
        print("Neither chart_first nor ChartFirst found!")

    # 3. Try charts_get
    if 'charts_get' in attrs:
        all_charts = mt5.charts_get()
        print(f"mt5.charts_get(): Found {len(all_charts) if all_charts else 0} charts")
    elif 'ChartsGet' in attrs:
        all_charts = mt5.ChartsGet()
        print(f"mt5.ChartsGet(): Found {len(all_charts) if all_charts else 0} charts")
    
    if all_charts:
        for c in all_charts:
            print(f" - Chart ID: {c.id}, Symbol: {c.symbol}, Period: {c.period}")
    
    # 4. Check if we can get active chart (foreground)
    # Note: MT5 API doesn't have a direct 'get active chart' (foreground) method 
    # except iterating or using ChartFirst.
    
    mt5.shutdown()

if __name__ == "__main__":
    debug_charts()
