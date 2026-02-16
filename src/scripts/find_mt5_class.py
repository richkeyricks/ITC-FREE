
import win32gui

def find_windows():
    print("Listing windows containing 'MetaTrader' in Title or Class...")
    def enum_handler(hwnd, ctx):
        title = win32gui.GetWindowText(hwnd)
        cls = win32gui.GetClassName(hwnd)
        if "MetaTrader" in title or "MetaTrader" in cls or "MT5" in title:
            is_visible = win32gui.IsWindowVisible(hwnd)
            is_minimized = win32gui.IsIconic(hwnd)
            print(f"HWND: {hwnd} | Visible: {is_visible} | Minimized: {is_minimized} | Class: {cls} | Title: {title}")

    win32gui.EnumWindows(enum_handler, None)

if __name__ == "__main__":
    find_windows()
