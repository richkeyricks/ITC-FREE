
import win32gui
import re

def find_mt5_chart():
    print("Searching for MetaTrader 5 windows...")
    
    found = []
    
    def win_enum_handler(hwnd, ctx):
        # We check even invisible/minimized windows
        title = win32gui.GetWindowText(hwnd)
        if title and "MetaTrader 5" in title:
                print(f"Found MT5 Main Window: '{title}' (HWND: {hwnd})")
                
                # Check main title first
                match = re.search(r"\[(\w+),(\w+)\]", title)
                if match:
                    found.append((match.group(1), match.group(2), title))
                
                # Enumerate children
                def child_enum_handler(chwnd, cctx):
                    ctitle = win32gui.GetWindowText(chwnd)
                    if ctitle and "," in ctitle:
                        # Chart titles in MT5 children are often just Symbol,Timeframe
                        print(f"  Child Window: '{ctitle}'")
                        cmatch = re.search(r"(\w+),(\w+)", ctitle)
                        if cmatch:
                            found.append((cmatch.group(1), cmatch.group(2), ctitle))
                
                win32gui.EnumChildWindows(hwnd, child_enum_handler, None)
    
    win32gui.EnumWindows(win_enum_handler, None)
    
    if found:
        print("\nSUCCESS: Found active charts via Windows API:")
        for s, t, full in found:
            print(f" - Symbol: {s}, Timeframe: {t} (Title: {full})")
    else:
        print("\nFAILURE: No MT5 window with [Symbol,TF] pattern found.")

if __name__ == "__main__":
    find_mt5_chart()
