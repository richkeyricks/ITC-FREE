# src/modules/chart/chart_data.py

# --- IMPORTS ---
from modules.mt5.mt5_service import MT5Service
import pandas as pd
from datetime import datetime

# --- LOGIC ---
class ChartDataManager:
    """Manages fetching OHLC data from MetaTrader 5 via MT5Service (thread-safe)"""
    
    @staticmethod
    def fetch_ohlc(symbol: str, timeframe=None, count=100):
        """
        Fetches OHLC data for a symbol from MT5.
        
        Args:
            symbol (str): Trading symbol (e.g., 'XAUUSD')
            timeframe: MT5 timeframe constant (default: TIMEFRAME_M15)
            count (int): Number of candles to fetch
            
        Returns:
            pd.DataFrame: OHLC data or None if failed
        """
        service = MT5Service.instance()
        
        # Default timeframe
        if timeframe is None:
            timeframe = service.TIMEFRAME_M15
        
        if not service.initialize():
            print("MT5 initialization failed for chart data")
            return None
            
        # Ensure symbol is valid
        # Try base symbol first, then suffixes if needed
        target_symbol = symbol
        symbol_info = service.symbol_info(symbol)
        
        if symbol_info is None:
            # Try common suffixes
            suffixes = ["m", "pro", ".pro", "ecn", ".ecn"]
            for suffix in suffixes:
                check_sym = f"{symbol}{suffix}"
                info = service.symbol_info(check_sym)
                if info is not None:
                    target_symbol = check_sym
                    symbol_info = info
                    print(f"// MT5: Auto-corrected {symbol} -> {target_symbol}")
                    break

        if symbol_info is None:
            print(f"Symbol {symbol} (or variants) not found")
            return None
            
        # If symbol not visible in Market Watch, add it
        if not symbol_info.visible:
            if not service.symbol_select(target_symbol, True):
                print(f"Failed to select symbol {target_symbol}")
                return None
                
        # Fetch rates
        rates = service.copy_rates_from_pos(target_symbol, timeframe, 0, count)
        
        if rates is None or len(rates) == 0:
            print(f"No rates found for {symbol}")
            return None
            
        # Convert to DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        
        # Rename columns to match mplfinance requirements
        df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'tick_volume': 'Volume'
        }, inplace=True)
        
        return df

    @staticmethod
    def calculate_ema(df, period=50):
        """Calculates EMA manually to avoid heavy extras"""
        if df is None or len(df) < period: return None
        return df['Close'].ewm(span=period, adjust=False).mean()

    @staticmethod
    def calculate_rsi(df, period=14):
        """Calculates RSI manually"""
        if df is None or len(df) < period + 1: return None
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def get_technical_summary(symbol):
        """Returns a dict of key tech indicators for AI Context"""
        service = MT5Service.instance()
        df = ChartDataManager.fetch_ohlc(symbol, service.TIMEFRAME_M15, 100)
        if df is None: return {}
        
        try:
            ema25 = ChartDataManager.calculate_ema(df, 25).iloc[-1]
            ema50 = ChartDataManager.calculate_ema(df, 50).iloc[-1]
            rsi = ChartDataManager.calculate_rsi(df, 14).iloc[-1]
            
            # Trend Detection
            trend = "BULLISH" if ema25 > ema50 else "BEARISH"
            
            return {
                "TREND": trend,
                "RSI": f"{int(rsi)} ({'Overbought' if rsi>70 else 'Oversold' if rsi<30 else 'Neutral'})",
                "EMA_CROSS": "EMA(25) > EMA(50)" if ema25 > ema50 else "EMA(25) < EMA(50)",
                "VOLATILITY": "High" # Simplified
            }
        except:
            return {}

if __name__ == "__main__":
    # Test
    service = MT5Service.instance()
    if service.initialize():
        data = ChartDataManager.fetch_ohlc("XAUUSD", service.TIMEFRAME_H1, 50)
        if data is not None:
            print(data.tail())
        service.shutdown()
