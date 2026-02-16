# src/modules/chart/chart_renderer.py
import mplfinance as mpf
import pandas as pd
import os
import matplotlib.pyplot as plt

class ChartRenderer:
    """Renders candlestick charts with technical indicators and signal markers"""
    
    # Custom theme based on Haineo AI Style
    HAINEO_STYLE = mpf.make_mpf_style(
        base_mpf_style='charles',
        marketcolors=mpf.make_marketcolors(
            up='#27AE60', down='#EB5757',
            edge='inherit', wick='inherit',
            volume='inherit'
        ),
        gridcolor='#2F363F',
        facecolor='#121417',
        edgecolor='#2F363F',
        gridstyle='--',
        y_on_right=True
    )
    
    @classmethod
    def save_candlestick_chart(cls, df, symbol, signal_type=None, entry=None, tp=None, sl=None, output_path="temp_chart.png"):
        """
        Renders and saves a candlestick chart.
        
        Args:
            df (pd.DataFrame): OHLC data
            symbol (str): Symbol name
            signal_type (str): 'BUY' or 'SELL'
            entry (float): Entry price level
            tp (float): Take Profit level
            sl (float): Stop Loss level
            output_path (str): File path to save the image
            
        Returns:
            str: Path to the saved image or None if failed
        """
        try:
            # Prepare additional plots (horizontal lines for Entry, TP, SL)
            hlines = []
            hcolors = []
            
            if entry:
                hlines.append(entry)
                hcolors.append('#2F80ED') # Blue for entry
            if tp:
                hlines.append(tp)
                hcolors.append('#27AE60') # Green for TP
            if sl:
                hlines.append(sl)
                hcolors.append('#EB5757') # Red for SL
            
            # Decoration
            title = f"{symbol} Analysis"
            if signal_type:
                title += f" - {signal_type} SIGNAL"
            
            # Create a larger figure for better AI analysis
            fig, axlist = mpf.plot(
                df,
                type='candle',
                style=cls.HAINEO_STYLE,
                title=title,
                ylabel='Price',
                hlines=dict(hlines=hlines, colors=hcolors, linestyle='-.', linewidths=1.5),
                mav=(20, 50), # Add Moving Averages for AI to see trend
                volume=True,
                show_nontrading=False,
                savefig=output_path,
                figsize=(12, 8),
                returnfig=True
            )
            
            plt.close(fig) # Prevent GUI freezing
            return os.path.abspath(output_path)
            
        except Exception as e:
            print(f"Error rendering chart: {e}")
            return None

if __name__ == "__main__":
    # Test with dummy data
    import numpy as np
    dates = pd.date_range("2023-01-01", periods=100, freq="H")
    data = pd.DataFrame({
        'Open': np.random.uniform(1900, 2000, 100),
        'High': np.random.uniform(2000, 2100, 100),
        'Low': np.random.uniform(1800, 1900, 100),
        'Close': np.random.uniform(1900, 2000, 100),
        'Volume': np.random.uniform(100, 1000, 100)
    }, index=dates)
    
    path = ChartRenderer.save_candlestick_chart(data, "GOLD_TEST", "BUY", 1950, 1980, 1920)
    if path:
        print(f"Chart saved at: {path}")
        # os.startfile(path)
