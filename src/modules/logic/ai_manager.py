# src/modules/logic/ai_manager.py
import os
import threading
import time
import datetime
from index import (get_account_meta, get_positions, get_history_orders, chat_with_ai, get_env_list)
from configs.ai_config import MASTER_GROQ_KEY, DEFAULT_GROQ_MODEL, AI_TRIAL_LIMIT

class AIManager:
    """
    Handles AI chat responses, context fetching from MT5, and chat history management.
    Follows Gravity Dev Rules: Business Logic separation.
    """
    
    @staticmethod
    def animate_thinking(parent):
        """Shows a typing animation while AI is processing"""
        dots = 1
        while getattr(parent, "ai_thinking", False):
            text = "✨ Thinking" + "." * dots
            AIManager._update_chat_log(parent, f"{text}\n", replace_last_line=True)
            dots = (dots % 3) + 1
            time.sleep(0.5)
            
    @staticmethod
    def get_ai_response(parent, msg, user_name, force_search=False):
        """Processes user message and gets response from AI with MT5 context."""
        
        # --- KEY & PROVIDER LOGIC ---
        api_key = os.getenv("AI_API_KEY", "")
        provider = os.getenv("AI_PROVIDER", "Groq")
        model = os.getenv("OR_MODEL", DEFAULT_GROQ_MODEL)
        
        if not api_key:
            api_key = MASTER_GROQ_KEY
            provider = "Groq"
            model = DEFAULT_GROQ_MODEL
        
        # 1. Fetch Deep Context from MT5
        try:
            # A. Account & Positions (Refined Risk)
            acc_info = get_account_meta()
            positions = get_positions()
            history = get_history_orders(limit=5)
            
            from modules.mt5.mt5_service import MT5Service
            mt5_service = MT5Service.instance()
            
            # Health & Risk Metrics
            health = mt5_service.get_terminal_state()
            health_str = f"Algo Trading: {'ON' if health.get('algo_trading') else 'OFF'}, Broker: {'CONNECTED' if health.get('connected') else 'DISCONNECTED'}"
            risk_str = f"Margin Level: {acc_info.get('margin_level', 0):,.2f}%, Drawdown: {acc_info.get('drawdown_pct', 0)}%, Win Rate: {acc_info.get('win_rate', 0)}%"
            
            acc_str = f"Balance: ${acc_info.get('balance', 0):,.2f}, Equity: ${acc_info.get('equity', 0):,.2f}, Live Profit: ${acc_info.get('profit', 0):,.2f}"
            pos_str = "None"
            if positions:
                pos_str = ", ".join([f"{p['symbol']} ({p['type']}) P/L: {p['profit']} [EA: {p['comment']}|M:{p['magic']}]" for p in positions])
            
            hist_str_mt5 = "None"
            if history:
                hist_str_mt5 = ", ".join([f"{h['symbol']} ({h['type']}) Profit: {h['profit']}" for h in history])
            
            # B. GOD MODE: Multi-Chart Detection
            from modules.chart.chart_data import ChartDataManager
            
            open_charts = mt5_service.get_all_open_charts()
            active_chart = mt5_service.get_active_chart() # Primary focus
            
            chart_ctx = "User is not looking at any chart (MT5 Minimized)"
            tech_ctx = ""
            
            if open_charts:
                chart_list = ", ".join([f"{c['symbol']} ({c['timeframe']})" for c in open_charts])
                chart_ctx = f"Open Charts: [{chart_list}]"
                
                if active_chart:
                    symbol = active_chart['symbol']
                    tf = active_chart['timeframe']
                    price = active_chart['price']
                    
                    # Fetch Technicals & Momentum (OHLC)
                    techs = ChartDataManager.get_technical_summary(symbol)
                    rates = mt5_service.get_recent_rates(symbol, tf, count=5)
                    
                    chart_ctx += f" | Focused: {symbol} ({tf}) @ {price}"
                    
                    momentum_ctx = "Historical Momentum (Last 5 Candles):\n"
                    if rates:
                        momentum_ctx += " | ".join([f"C:{r['close']}" for r in rates])
                    else:
                        momentum_ctx = "Momentum data unavailable"

                    if techs:
                        tech_ctx = f"Technical Summary ({symbol}): Trend: {techs.get('TREND', 'Unknown')}, RSI: {techs.get('RSI', 'N/A')}, EMA: {techs.get('EMA_CROSS', 'N/A')}\n{momentum_ctx}"
            else:
                health_str = "Unknown"
                risk_str = "Unknown"
                tech_ctx = "No market data available"
                chart_ctx = "No charts detected (MT5 Minimized)"
                
        except Exception as e:
            print(f"Context Fetch Error: {e}")
            acc_str = "Unavailable (MT5 Disconnected)"
            pos_str = "Unknown"
            hist_str_mt5 = "Unknown"
            chart_ctx = "Unknown"
            tech_ctx = "Unknown"

        # 2. Build Personalized System Prompt
        # 2. Build Personalized System Prompt (TERMINAL MODE)
        system_prompt = f"""
        You are SkyNET v9, a Real-Time Financial Data Terminal.
        User: {user_name}
        
        == SYSTEM HEALTH ==
        {health_str}
        
        == TRADING CONTEXT ==
        {acc_str}
        {risk_str}
        Open Positions: {pos_str}
        
        == VISUAL CONTEXT ==
        {chart_ctx}
        {tech_ctx}
        
        INSTRUCTIONS:
        - You are a DATA TERMINAL, not a chatbot. Do not have a personality.
        - You process incoming DATA STREAMS and user queries.
        - If [SYSTEM DATA STREAM] is present, SUMMARIZE the 'DATA' section relative to the 'USER QUERY'.
        - If the stream returns "No recent... news", inform the user that no real-time data matched their specific query.
        - Do not apologize. Do not say "I don't have internet". Use the provided stream as your live feed.
        - **TIME SENSITIVITY**: Always refer to the `== CURRENT TIME ==` for temporal context.
        """
        
        # 3. Chat History
        chat_hist = parent.db_manager.get_chat_history(limit=5)
        
        # --- NEWS ENGINE INTEGRATION (DATA STREAM INJECTION) ---
        context_msg = msg
        news_keywords = ["berita", "news", "terbaru", "today", "hari ini", "update", "kejadian"]
        
        # Check Force Search (from Chips) or Toggle
        is_search_active = force_search or (hasattr(parent, 'search_var') and parent.search_var.get())
        
        # Auto-detect if not forced, but restrict to explicit keywords if toggle is OFF
        # If toggle is ON, we ALWAYS search.
        should_search = is_search_active or any(k in msg.lower() for k in news_keywords)
        
        if should_search:
            try:
                from modules.logic.smart_fill import SmartFill
                env = get_env_list()
                if env.get("SERPER_API_KEY"):
                    symbol = "forex"
                    if active_chart: symbol = active_chart['symbol']
                    
                    print(f"// AI News Search Triggered: {symbol} (Active={is_search_active})")
                    
                    # If manually toggled, use the raw message as query (don't append symbol if generic)
                    # If auto-detected, maybe safer to use smart logic
                    search_query = msg
                    
                    news_stream = SmartFill._fetch_serper_news(symbol, env, raw_query=search_query)
                    
                    if news_stream:
                        # INJECT INTO USER MESSAGE STREAM
                        context_msg = f"""
[SYSTEM DATA STREAM]
SOURCE: GOOGLE NEWS REAL-TIME FEED
DATA:
{news_stream}
[END STREAM]

USER QUERY: {msg}

INSTRUCTION: Answer the user's query using the data above. DO NOT mention "SYSTEM DATA STREAM" or output raw logs. just answer naturally.
"""
                        # OVERRIDE PROVIDER TO CLOUDFLARE FOR SEARCH TASKS
                        # This saves OpenRouter credits and uses the higher limit Cloudflare model
                        cf_token = os.getenv("CLOUDFLARE_API_TOKEN")
                        if cf_token:
                            print("// Switching to Cloudflare for Search Task")
                            provider = "Cloudflare"
                            api_key = cf_token
                        else:
                            print("// Cloudflare Token Missing. Falling back to configured provider.")

            except Exception as e:
                print(f"// AI News Error: {e}")

        # Add Time Awareness to System Prompt
        curr_time = datetime.datetime.now().strftime("%A, %d %B %Y %H:%M")
        system_prompt += f"\n\n== CURRENT TIME ==\n{curr_time}"

        if chat_hist:
            prev_chat = "\n".join([f"{h['role']}: {h['content']}" for h in chat_hist])
            context_msg = f"Previous Chat:\n{prev_chat}\n\nCurrent Question: {msg}"

        # 4. Call AI Core (Simplified routing via Waterfall)
        try:
            response = chat_with_ai(
                user_prompt=context_msg, 
                user_api_key=api_key if api_key != MASTER_GROQ_KEY else "", 
                user_provider=provider, 
                system_context=system_prompt
            )
            
            # 5. UI Update (Stop Animation & Replace)
            if hasattr(parent, 'ai_thinking'):
                 parent.ai_thinking = False
                 time.sleep(0.6) # Wait for animation loop to clear
                 
            AIManager._update_chat_log(parent, f"🤖 ITC AI: {response}\n\n", replace_last_line=True)
            
            # Save to memory (Persist to Supabase)
            if hasattr(parent, 'db_manager'):
                threading.Thread(target=lambda: parent.db_manager.push_chat("assistant", response), daemon=True).start()
                
        except Exception as e:
            if hasattr(parent, 'ai_thinking'):
                 parent.ai_thinking = False
                 time.sleep(0.6)
                 
            err_msg = f"❌ AI Error: {str(e)}"
            AIManager._update_chat_log(parent, f"{err_msg}\n\n", replace_last_line=True)
            # Log error to DB if possible (optional, but good for debugging)
            if hasattr(parent, 'db_manager'):
                 threading.Thread(target=lambda: parent.db_manager.push_chat("system", err_msg), daemon=True).start()
            
        # Re-enable Input
        def enable_input():
            if hasattr(parent, 'ai_input'):
                parent.ai_input.configure(state="normal")
                parent.ai_input.focus_set()
        
        if hasattr(parent, 'safe_ui_update'):
            parent.safe_ui_update(enable_input)
        else:
            parent.after(0, enable_input)

    @staticmethod
    def animate_thinking(parent):
        """Shows a typing animation bubble while AI is processing"""
        if getattr(parent, "ai_thinking", False):
            # Create a temporary bubble
            dummy = parent.add_chat_bubble("✨ Thinking...", is_user=False, is_thinking=True)
            parent.thinking_bubble = dummy
            
    @staticmethod
    def _update_chat_log(parent, text, replace_last_line=False):
        """Replaces the thinking bubble with the actual response"""
        def _ui_task():
            # Remove thinking bubble if exists
            if hasattr(parent, 'thinking_bubble') and parent.thinking_bubble:
                try: parent.thinking_bubble.destroy()
                except: pass
                parent.thinking_bubble = None
            
            # Add actual message (Clean up prefixes if any)
            clean_text = text.replace("🤖 ITC AI: ", "").replace("❌ AI Error: ", "")
            parent.add_chat_bubble(clean_text, is_user=False)
            
        if hasattr(parent, 'safe_ui_update'):
            parent.safe_ui_update(_ui_task)
        else:
            parent.after(0, _ui_task)

    @staticmethod
    def send_ai_message(parent):
        from CTkMessagebox import CTkMessagebox
        
        msg = parent.ai_input.get().strip()
        if not msg: return
        
        # --- DYNAMIC TIER LIMIT CHECK ---
        limit = parent.db_manager.get_total_ai_limit()
        count = parent.db_manager.get_ai_message_count()
        
        if count >= limit:
            tier = parent.db_manager.get_user_tier()
            msg_box = f"You have reached your daily limit of {limit} AI chats for the {tier} tier.\n\nPlease upgrade to a higher tier for more access."
            if tier == "STANDARD":
                msg_box += "\n\nTip: Upgrade to GOLD to get 100 messages/day!"
            
            CTkMessagebox(title="Limit Reached", message=msg_box, icon="warning")
            AIManager._update_chat_log(parent, f"🔒 SYSTEM: {tier} daily limit reached ({limit}/{limit}).\n")
            return

        user_name = os.getenv("USER_NAME", "Trader")
        AIManager._update_chat_log(parent, f"👤 {user_name}: {msg}\n")
        parent.ai_input.delete(0, "end")
        
        # Save user message to cloud memory
        threading.Thread(target=lambda: parent.db_manager.push_chat("user", msg), daemon=True).start()
        
        threading.Thread(target=lambda: AIManager.get_ai_response(parent, msg, user_name), daemon=True).start()
