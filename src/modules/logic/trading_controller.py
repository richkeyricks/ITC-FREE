# src/modules/logic/trading_controller.py
import threading
import os
from index import execute_trade
from modules.chart.chart_data import ChartDataManager
from modules.chart.chart_renderer import ChartRenderer

class TradingController:
    """
    Handles Signal Analysis Pipeline and Trade Execution Logic.
    Follows Gravity Dev Rules: Business Logic separation.
    """
    
    @staticmethod
    def perform_analysis(parent, symbol, signal_type, entry, tp, sl):
        """Full pipeline: Data -> Render -> AI Analysis -> UI Update"""
        parent.show_page("analysis")
        parent.log("INFO", parent.translator.get("analysis_analyzing").replace("...", f": {signal_type} {symbol}..."))
        
        # Reset UI (Analysis Page elements)
        if hasattr(parent, 'verdict_val'):
            parent.verdict_val.configure(text=parent.translator.get("analysis_analyzing"), text_color="orange")
            parent.acc_val.configure(text="0%")
            parent.reason_text.configure(state="normal")
            parent.reason_text.delete("0.0", "end")
            parent.reason_text.insert("0.0", f"Analyzing {symbol} {signal_type} at {entry}...\nPlease wait 5-10 seconds.")
            parent.reason_text.configure(state="disabled")
        
        def _task():
            try:
                # 1. Fetch Data
                df = ChartDataManager.fetch_ohlc(symbol)
                if df is None:
                    parent.log("ERROR", "Failed to fetch chart data from MT5")
                    return
                
                # 2. Render Chart
                chart_path = ChartRenderer.save_candlestick_chart(df, symbol, signal_type, entry, tp, sl)
                if not chart_path:
                    parent.log("ERROR", "Failed to render candlestick chart")
                    return
                
                # 3. Update Chart UI
                parent.after(0, lambda: TradingController._update_chart_image(parent, chart_path))
                
                # 4. AI Analysis
                parent.log("INFO", "🤖 Requesting AI technical analysis...")
                result = parent.analyzer.analyze_chart(chart_path, symbol, signal_type, entry, tp, sl)
                
                # 5. Update Results
                parent.after(0, lambda: TradingController._update_analysis_results(parent, result, symbol, signal_type, entry, tp, sl))
                
            except Exception as e:
                parent.log("ERROR", f"Analysis pipeline failed: {e}")

        threading.Thread(target=_task, daemon=True).start()

    @staticmethod
    def _update_chart_image(parent, path):
        """Updates the chart label with a PIL Image"""
        from PIL import Image
        import customtkinter as ctk
        try:
            img = Image.open(path)
            w, h = parent.chart_frame.winfo_width(), parent.chart_frame.winfo_height()
            if w < 100: w = 600 
            if h < 100: h = 400
            
            img.thumbnail((w-20, h-20))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            parent.chart_label.configure(image=ctk_img, text="")
        except Exception as e:
            parent.log("ERROR", f"Failed to display chart image: {e}")

    @staticmethod
    def _update_analysis_results(parent, result, symbol, signal_type, entry, tp, sl):
        """Updates the analysis cards with results from AI"""
        parent.last_analysis = result
        if "error" in result:
            parent.verdict_val.configure(text="ERROR", text_color="red")
            parent.acc_val.configure(text="--")
            parent.reason_text.configure(state="normal")
            parent.reason_text.delete("0.0", "end")
            parent.reason_text.insert("0.0", f"AI Error: {result['error']}")
            parent.reason_text.configure(state="disabled")
            
            if "quota" in str(result["error"]).lower():
                parent.show_quota_warning()
            return

        verdict = result.get("verdict", "UNKNOWN")
        v_color = "#27AE60" if verdict == "VALID" else "#EB5757"
        parent.verdict_val.configure(text=verdict, text_color=v_color)
        parent.acc_val.configure(text=f"{result.get('accuracy', 0)}%")
        
        reason = result.get("reasoning", "No reasoning provided.")
        parent.reason_text.configure(state="normal")
        parent.reason_text.delete("0.0", "end")
        parent.reason_text.insert("0.0", f"TREND: {result.get('trend', 'N/A')}\n\nREASONING:\n{reason}")
        parent.reason_text.configure(state="disabled")
        
        parent.btn_execute.configure(state="normal", command=lambda: TradingController.confirm_trade(parent, symbol, signal_type, entry, tp, sl))
        parent.btn_skip.configure(state="normal", command=lambda: parent.show_page("dashboard"))
        
        parent.log("INFO", parent.translator.get("analysis_manual_approval").format(type=signal_type, symbol=symbol))
        
        if hasattr(parent, 'chk_auto_exec') and parent.chk_auto_exec.get() and verdict == "VALID":
             # Legacy Auto Exec Support
             parent.log("INFO", f"⚡ Auto-Executing Signal (AI Verified): {symbol} {signal_type}")
             TradingController.confirm_trade(parent, symbol, signal_type, entry, tp, sl)
        
        # New Execution Mode Support
        mode = "AI-ASSISTED (Manual)"
        if hasattr(parent, 'execution_mode'):
             mode = parent.execution_mode.get()
             
        if mode == "AI-FILTER (Auto)" and verdict == "VALID":
             parent.log("INFO", f"⚡ Auto-Executing Signal (AI Filter Passed): {symbol} {signal_type}")
             TradingController.confirm_trade(parent, symbol, signal_type, entry, tp, sl)
        elif mode == "AI-FILTER (Auto)" and verdict != "VALID":
             parent.log("WARN", f"🛑 Auto-Execution Blocked by AI Filter: {verdict}")


    @staticmethod
    def on_signal_detected(parent, signal):
        """Callback from Telegram listener thread"""
        
        # Determine Execution Mode
        mode = "AI-ASSISTED (Manual)" # Default
        if hasattr(parent, 'execution_mode'):
            mode = parent.execution_mode.get()
        # Fallback for old switch
        elif hasattr(parent, 'chk_auto_exec') and parent.chk_auto_exec.get(): 
             mode = "DIRECT (Turbo)"
             
        # 1. DIRECT (Turbo) MODE
        if "DIRECT" in mode:
            parent.log("INFO", f"⚡ Auto-Executing Signal (Direct Mode): {signal['symbol']} {signal['type']}")
            # Execute directly in background
            threading.Thread(target=lambda: execute_trade(signal), daemon=True).start()
            return

        # 2. AI MODES (Filter or Assisted) -> Both require Analysis First
        parent.after(0, lambda: parent.perform_analysis(
            symbol=signal.get("symbol"),
            signal_type=signal.get("type"),
            entry=signal.get("entry"),
            tp=signal.get("tp"),
            sl=signal.get("sl")
        ))

    @staticmethod
    def confirm_trade(parent, symbol, signal_type, entry, tp, sl):
        """Executes the trade after user confirmation"""
        parent.log("INFO", parent.translator.get("analysis_manual_approval").format(type=signal_type, symbol=symbol))
        
        signal_dict = {
            "symbol": symbol,
            "type": signal_type,
            "entry": entry,
            "tp": tp,
            "sl": sl
        }
        
        parent.show_page("dashboard")
        try:
            from index import execute_trade
            threading.Thread(target=lambda: execute_trade(signal_dict), daemon=True).start()
        except ImportError:
            # Fallback if index not immediately importable
            import sys
            if "index" not in sys.modules:
                 import index
            index.execute_trade(signal_dict)
