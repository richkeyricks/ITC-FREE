import MetaTrader5 as mt5
import threading
import time
import os

class MT5Service:
    """
    Singleton Service for MetaTrader 5 Integration.
    Ensures thread-safe access to the MT5 terminal API.
    """
    _instance = None
    _lock = threading.RLock() # Re-entrant lock for thread safety

    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self):
        if MT5Service._instance is not None:
            raise Exception("This class is a singleton!")
        self.connected = False
        self.login_id = 0
    
    def initialize(self, login=None, password=None, server=None, allow_launch=True):
        """Thread-safe initialization with optional auto-launch control"""
        with self._lock:
            try:
                # If already initialized with same login, just return True
                info = mt5.terminal_info()
                if self.connected and info is not None:
                    # Optional: Check if login matches if provided
                    if login and self.login_id == login:
                        return True

                # --- PASSIVE CHECK ---
                if not allow_launch and info is None:
                    # Do not trigger mt5.initialize() which launches the binary
                    return False

                # Attempt Init (Active)
                if login and password and server:
                    self.connected = mt5.initialize(login=login, password=password, server=server)
                    if self.connected: 
                        self.login_id = login
                else:
                    self.connected = mt5.initialize()
                
                if not self.connected:
                    # Only log error if we were actually TRYING to launch/connect
                    if allow_launch:
                        print(f"// MT5Service: Init failed. Error: {mt5.last_error()}")
                
                return self.connected
            except Exception as e:
                if allow_launch:
                    print(f"// MT5Service: Init Exception: {e}")
                return False

    def shutdown(self):
        with self._lock:
            mt5.shutdown()
            self.connected = False

    def get_terminal_info(self, passive=False):
        with self._lock:
            info = mt5.terminal_info()
            if info is None and not passive:
                # Re-init attempt (Active)
                if mt5.initialize():
                    info = mt5.terminal_info()
            return info

    def get_terminal_state(self):
        """Returns simplified state: Algo On/Off, Broker Connected, etc."""
        with self._lock:
            if not self.initialize(): return {"error": "Not Initialized"}
            info = mt5.terminal_info()
            if not info: return {"error": "Terminal Fail"}
            
            return {
                "algo_trading": info.trade_allowed,
                "connected": info.connected,
                "dll_allowed": info.dlls_allowed,
                "path": info.path
            }

    def get_mt5_status_deep(self, passive=False):
        """
        Returns 3-State Connection Status:
        0: Offline (Red) - Terminal not running or critical failure.
        1: Standby (Yellow) - Terminal running, but account not connected.
        2: Active (Green) - Valid account trade session established.
        
        Args:
            passive (bool): If True, will NOT launch MT5 if it's currently closed.
        """
        with self._lock:
            try:
                # 1. Check if terminal is initialized/running
                info = mt5.terminal_info()
                if info is None:
                    # If passive, we just return Offline instead of triggering a launch
                    if passive: return 0
                    
                    # Active attempt (Warning: this launches the terminal)
                    if not mt5.initialize(): return 0
                    info = mt5.terminal_info()
                
                if not info: return 0
                
                # 2. Check Broker Connection
                if not info.connected: return 1
                
                # 3. Check Account Auth
                acc = mt5.account_info()
                if acc is None: return 1
                
                return 2
            except:
                return 0

    def get_account_info(self):
        with self._lock:
            return mt5.account_info() if self.initialize(allow_launch=False) else None

    def get_positions(self, symbol=None):
        with self._lock:
            if not self.initialize(allow_launch=False): return None
            if symbol:
                return mt5.positions_get(symbol=symbol)
            return mt5.positions_get()

    def get_orders(self, symbol=None):
        with self._lock:
            if not self.initialize(allow_launch=False): return None
            if symbol:
                return mt5.orders_get(symbol=symbol)
            return mt5.orders_get()

    def history_deals_get(self, date_from, date_to, group="*"):
        with self._lock:
            if not self.initialize(): return None
            try:
                return mt5.history_deals_get(date_from, date_to, group=group)
            except Exception as e:
                print(f"// MT5Service History Error: {e}")
                return None

    def symbol_info(self, symbol):
        with self._lock:
            if not self.initialize(allow_launch=False): return None
            return mt5.symbol_info(symbol)

    def symbol_info_tick(self, symbol):
        with self._lock:
            if not self.initialize(allow_launch=False): return None
            return mt5.symbol_info_tick(symbol)

    def get_recent_rates(self, symbol, timeframe, count=5):
        """Fetches OHLC data for the last X candles."""
        with self._lock:
            if not self.initialize(): return None
            
            # Map timeframe string if needed (M1, H1 etc)
            tf_map = {
                "M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5, "M15": mt5.TIMEFRAME_M15,
                "M30": mt5.TIMEFRAME_M30, "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4,
                "D1": mt5.TIMEFRAME_D1, "W1": mt5.TIMEFRAME_W1, "MN1": mt5.TIMEFRAME_MN1
            }
            tf = tf_map.get(timeframe, mt5.TIMEFRAME_H1)
            
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
            if rates is None: return []
            
            # Convert to list of dicts for AI convenience
            result = []
            for r in rates:
                result.append({
                    "time": r[0],
                    "open": r[1],
                    "high": r[2],
                    "low": r[3],
                    "close": r[4],
                    "tick_volume": r[5]
                })
            return result

    def order_send(self, request):
        """Sends an order with locking"""
        with self._lock:
            if not self.initialize(): 
                # Create a specific return object or None to indicate failure before send
                # Returning a dummy object with retcode != DONE to simulate fail
                class FailResult:
                    retcode = -1
                    comment = "MT5 Not Initialized"
                return FailResult()
                
            return mt5.order_send(request)

    def login(self, login, password, server):
        with self._lock:
            if not  mt5.initialize(): return False
            res = mt5.login(login=login, password=password, server=server)
            if res:
                self.connected = True
                self.login_id = login
            return res
    
    def last_error(self):
        with self._lock:
            return mt5.last_error()
    
    # Constants exposure for convenience
    ORDER_TYPE_BUY = mt5.ORDER_TYPE_BUY
    ORDER_TYPE_SELL = mt5.ORDER_TYPE_SELL
    TRADE_ACTION_DEAL = mt5.TRADE_ACTION_DEAL
    ORDER_TIME_GTC = mt5.ORDER_TIME_GTC
    ORDER_FILLING_IOC = mt5.ORDER_FILLING_IOC
    ORDER_FILLING_FOK = mt5.ORDER_FILLING_FOK
    ORDER_FILLING_RETURN = mt5.ORDER_FILLING_RETURN
    TRADE_RETCODE_DONE = mt5.TRADE_RETCODE_DONE
    DEAL_ENTRY_OUT = mt5.DEAL_ENTRY_OUT
    DEAL_TYPE_BUY = mt5.DEAL_TYPE_BUY
    DEAL_TYPE_SELL = mt5.DEAL_TYPE_SELL
    POSITION_TYPE_BUY = mt5.POSITION_TYPE_BUY
    POSITION_TYPE_SELL = mt5.POSITION_TYPE_SELL

    # Timeframe constants
    TIMEFRAME_M1 = mt5.TIMEFRAME_M1
    TIMEFRAME_M5 = mt5.TIMEFRAME_M5
    TIMEFRAME_M15 = mt5.TIMEFRAME_M15
    TIMEFRAME_M30 = mt5.TIMEFRAME_M30
    TIMEFRAME_H1 = mt5.TIMEFRAME_H1
    TIMEFRAME_H4 = mt5.TIMEFRAME_H4
    TIMEFRAME_D1 = mt5.TIMEFRAME_D1
    TIMEFRAME_W1 = mt5.TIMEFRAME_W1

    # Account mode constants
    ACCOUNT_TRADE_MODE_DEMO = mt5.ACCOUNT_TRADE_MODE_DEMO

    # --- ADDITIONAL THREAD-SAFE METHODS ---
    def account_info(self):
        """Alias for get_account_info (thread-safe)"""
        with self._lock:
            return mt5.account_info() if self.initialize() else None

    def copy_rates_from_pos(self, symbol, timeframe, start_pos, count):
        """Thread-safe wrapper for mt5.copy_rates_from_pos"""
        with self._lock:
            if not self.initialize(): return None
            return mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)

    def symbol_select(self, symbol, enable=True):
        """Thread-safe wrapper for mt5.symbol_select"""
        with self._lock:
            if not self.initialize(): return False
            return mt5.symbol_select(symbol, enable)

    def get_all_open_charts(self):
        """
        Scans all MT5 windows and children to find EVERY open chart.
        Returns: List of {symbol: str, timeframe: str}
        """
        with self._lock:
            all_charts = []
            seen = set()
            
            try:
                import win32gui
                import re
                
                def enum_handler(hwnd, ctx):
                    cls = win32gui.GetClassName(hwnd)
                    if "MetaTrader" in cls:
                        title = win32gui.GetWindowText(hwnd)
                        # Check main title
                        m = re.search(r"\[\s*([^,\]]+)\s*,\s*([^,\]]+)\s*\]", title)
                        if m:
                            s, t = m.group(1).strip(), m.group(2).strip()
                            if (s, t) not in seen:
                                all_charts.append({"symbol": s, "timeframe": t})
                                seen.add((s, t))
                        
                        # Check children (individual chart windows)
                        def child_handler(chwnd, cctx):
                            ctitle = win32gui.GetWindowText(chwnd)
                            if ctitle and "," in ctitle:
                                cm = re.search(r"([^,\]]+)\s*,\s*([^,\]]+)", ctitle)
                                if cm:
                                    s, t = cm.group(1).strip(), cm.group(2).strip()
                                    if len(s) >= 3 and len(t) >= 2 and (s, t) not in seen:
                                        all_charts.append({"symbol": s, "timeframe": t})
                                        seen.add((s, t))
                        
                        win32gui.EnumChildWindows(hwnd, child_handler, None)
                    return True

                win32gui.EnumWindows(enum_handler, None)
            except Exception as e:
                print(f"// MT5 Multi-Chart Scrape Failed: {e}")
            
            return all_charts

    def get_active_chart(self):
        """
        Retrieves the Symbol and Timeframe of the active chart.
        Uses MT5 API if available, falls back to Win32 scraping if needed.
        """
        with self._lock:
            # 1. Try Native MT5 API first (If attributes exist)
            if self.initialize():
                try:
                    if hasattr(mt5, 'ChartFirst'):
                        chart_id = mt5.ChartFirst()
                        if chart_id >= 0:
                            symbol = mt5.ChartSymbol(chart_id)
                            period = mt5.ChartPeriod(chart_id)
                            
                            # Map Period to String
                            tf_map = {
                                mt5.TIMEFRAME_M1: "M1", mt5.TIMEFRAME_M5: "M5", mt5.TIMEFRAME_M15: "M15",
                                mt5.TIMEFRAME_M30: "M30", mt5.TIMEFRAME_H1: "H1", mt5.TIMEFRAME_H4: "H4",
                                mt5.TIMEFRAME_D1: "D1", mt5.TIMEFRAME_W1: "W1", mt5.TIMEFRAME_MN1: "MN1"
                            }
                            
                            tick = mt5.symbol_info_tick(symbol)
                            return {
                                "symbol": symbol,
                                "timeframe": tf_map.get(period, f"Unknown ({period})"),
                                "price": tick.last if tick else 0.0
                            }
                except Exception as e_api:
                    print(f"// MT5 API Chart Detection Failed: {e_api}")

            # 2. Fallback: Win32 Scraping (GOD MODE RECOVERY)
            try:
                import win32gui
                import re
                
                # Search for MT5 Main Window
                chart_info = {"symbol": None, "tf": None}
                mt5_windows_found = 0
                
                def enum_handler(hwnd, ctx):
                    nonlocal mt5_windows_found
                    cls = win32gui.GetClassName(hwnd)
                    if "MetaTrader" in cls:
                        mt5_windows_found += 1
                        title = win32gui.GetWindowText(hwnd)
                        # Pattern: [\w\.,]+,[\w\.,]+ (Supports symbols with dots or other chars)
                        # Flexible pattern to catch [BTCUSDm,M15] or [EURUSD, H1]
                        match = re.search(r"\[\s*([^,\]]+)\s*,\s*([^,\]]+)\s*\]", title)
                        
                        if match:
                            chart_info["symbol"] = match.group(1).strip()
                            chart_info["tf"] = match.group(2).strip()
                            print(f"// MT5 Win32: SUCCESS! Detected {chart_info['symbol']} on {chart_info['tf']} from Title")
                            return False # Stop enumerating
                        
                        # Pattern 2: Search children (if charts are tiled/floating)
                        def child_handler(chwnd, cctx):
                            ctitle = win32gui.GetWindowText(chwnd)
                            if ctitle and "," in ctitle:
                                cmatch = re.search(r"([^,\]]+)\s*,\s*([^,\]]+)", ctitle)
                                if cmatch:
                                    # Basic sanity check: Symbol usually uppercase or includes m/pro/etc
                                    s = cmatch.group(1).strip()
                                    t = cmatch.group(2).strip()
                                    if len(s) >= 3 and len(t) >= 2:
                                        chart_info["symbol"] = s
                                        chart_info["tf"] = t
                                        return False
                            return True
                        
                        win32gui.EnumChildWindows(hwnd, child_handler, None)
                        if chart_info["symbol"]:
                            print(f"// MT5 Win32: SUCCESS! Detected {chart_info['symbol']} on {chart_info['tf']} from Child Window")
                            return False # Stop
                    return True # Continue enumeration

                win32gui.EnumWindows(enum_handler, None)
                
                if chart_info["symbol"]:
                    symbol = chart_info["symbol"]
                    # Get price if possible
                    price = 0.0
                    try:
                        if self.initialize():
                            tick = mt5.symbol_info_tick(symbol)
                            price = tick.last if tick else 0.0
                    except: pass
                        
                    return {
                        "symbol": symbol,
                        "timeframe": chart_info["tf"],
                        "price": price
                    }
                else:
                    if mt5_windows_found > 0:
                        print(f"// MT5 Win32: Found {mt5_windows_found} MT5 windows but none had active chart patterns in Title.")
            except Exception as e_win32:
                print(f"// MT5 Win32 Fallback Failed: {e_win32}")

    def get_visible_symbols(self):
        """Returns a list of all symbols currently visible in Market Watch"""
        with self._lock:
            if not self.initialize(): return []
            try:
                symbols = mt5.symbols_get(group="*", visible=True)
                return [s.name for s in symbols] if symbols else []
            except Exception as e:
                print(f"// MT5 Visible Symbols Error: {e}")
                return []
