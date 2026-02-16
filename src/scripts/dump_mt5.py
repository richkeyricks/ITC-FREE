
import MetaTrader5 as mt5
import os
from dotenv import load_dotenv

def dump_mt5():
    load_dotenv()
    print(f"MT5 Library Version: {getattr(mt5, '__version__', 'unknown')}")
    
    attrs = sorted(dir(mt5))
    print("\nAll MT5 Attributes:")
    for a in attrs:
        print(f" - {a}")

if __name__ == "__main__":
    dump_mt5()
