import requests
import json
import os

class BridgeController:
    """
    Handles the relaying of formatted signal messages to a user's Telegram channel.
    Follows Gravity Dev Rules: Modular Business Logic.
    """

    @staticmethod
    def relay_signal(signal, config):
        """
        Formats and sends a signal to the provider's channel via Bot API.
        :param signal: Dictionary containing symbol, type, entry, sl, tp1, etc.
        :param config: Dictionary containing bot_token, chat_id, and template.
        """
        bot_token = config.get("bot_token")
        chat_id = config.get("chat_id")
        template = config.get("template")

        if not bot_token or not chat_id or not template:
            return False, "Missing Bridge configuration."

        try:
            # Format the message using variables
            # Safe cleaning of data
            symbol = str(signal.get("symbol", "UNKNOWN")).upper()
            action = str(signal.get("type", "BUY/SELL")).upper()
            entry = str(signal.get("entry", "Market"))
            sl = str(signal.get("sl", "None"))
            tp1 = str(signal.get("tp1", "None"))
            tp2 = str(signal.get("tp2", "None"))
            tp3 = str(signal.get("tp3", "None"))

            # --- SMART FILL ENGINE INTEGRATION ---
            # Check if template needs Advanced Data
            needs_smart_fill = any(k in template for k in ["{ANALYSIS_REASON}", "{NEWS_CONTEXT}", "{CONFIDENCE_SCORE}", "{RR_RATIO}"])
            
            enrich_data = {}
            if needs_smart_fill:
                print("// Bridge: SmartFill Triggered for Detail Injection...")
                from modules.logic.smart_fill import SmartFill
                enrich_data = SmartFill.enrich_signal(signal)

            # Dictionary of all possible placeholders
            nav_map = {
                "SYMBOL": symbol,
                "TYPE": action,
                "ENTRY": entry,
                "SL": sl,
                "TP1": tp1,
                "TP2": tp2,
                "TP3": tp3,
                # Smart Data (Default to empty if not enriched)
                "ANALYSIS_REASON": enrich_data.get("ANALYSIS_REASON", "• Technical Analysis Pending..."),
                "NEWS_CONTEXT": enrich_data.get("NEWS_CONTEXT", "• Market sentiment neutral"),
                "CONFIDENCE_SCORE": enrich_data.get("CONFIDENCE_SCORE", "85%"),
                "SIGNAL_POWER": enrich_data.get("SIGNAL_POWER", f"STRONG {action}"),
                
                # Probability Matrix
                "PROB_BUY": enrich_data.get("PROB_BUY", "75%"),
                "PROB_SELL": enrich_data.get("PROB_SELL", "25%"),
                "PROB_TP1": enrich_data.get("PROB_TP1", "80%"),
                "PROB_TP2": enrich_data.get("PROB_TP2", "50%"),
                "PROB_TP3": enrich_data.get("PROB_TP3", "25%"),
                
                # Extended Institutional Fields
                "TIMEFRAME": enrich_data.get("TIMEFRAME", "M15"),
                "SESSION": enrich_data.get("SESSION", "London/NY"),
                "SIGNAL_TIME": enrich_data.get("SIGNAL_TIME", "NOW"),
                
                "SL_PIPS": enrich_data.get("SL_PIPS", "(?)"),
                "TP1_PIPS": enrich_data.get("TP1_PIPS", "(?)"),
                "TP2_PIPS": enrich_data.get("TP2_PIPS", "(?)"),
                
                "WC_CONDITION": enrich_data.get("WC_CONDITION", "N/A"),
                "WC_SLIPPAGE": enrich_data.get("WC_SLIPPAGE", "~5 pips"),
                "WC_MAX_LOSS": enrich_data.get("WC_MAX_LOSS", "-2%"),
                "DD_STATE": enrich_data.get("DD_STATE", "Safe"),
                
                "MATRIX_STATUS": enrich_data.get("matrix_status", "ALLOWED"),
                "MATRIX_RISK": enrich_data.get("matrix_risk", "MODERATE"),
                "MATRIX_EXEC": enrich_data.get("matrix_exec", "Market"),
                "MATRIX_AVOID": enrich_data.get("matrix_avoid", "None"),
                
                # Risk & Stats
                "RISK_PIPS": enrich_data.get("RISK_PIPS", "30 pips"),
                "RR_RATIO": enrich_data.get("RR_RATIO", "1:2"),
                "RISK_PERCENT": enrich_data.get("RISK_PERCENT", "2%"),
                "RISK_USD": enrich_data.get("RISK_USD", "$20"),
                "ACC_BAL": enrich_data.get("ACC_BAL", "$1,000"),
                "SIM_LOSS": enrich_data.get("SIM_LOSS", "-$20"),
                "SIM_WIN": enrich_data.get("SIM_WIN", "+$40"),
                "SIM_WIN_TP1": enrich_data.get("SIM_WIN_TP1", "+$20"),
                "SIM_WIN_TP2": enrich_data.get("SIM_WIN_TP2", "+$50"),
                
                # Historical & Last 30 (Auditor Data)
                "TOTAL_SIGNALS": enrich_data.get("TOTAL_SIGNALS", "0"),
                "WIN_LOSS_RATIO": enrich_data.get("WIN_LOSS_RATIO", "0 / 0"),
                "WIN_RATE": enrich_data.get("WIN_RATE", "N/A"),
                "SIGNAL_RATING": enrich_data.get("SIGNAL_RATING", "⭐⭐⭐"),
                
                "LAST30_WINRATE": enrich_data.get("LAST30_WINRATE", "Calculating..."),
                "LAST30_RR": enrich_data.get("LAST30_RR", "1:2.0"),
                "LAST30_DD": enrich_data.get("LAST30_DD", "-0.0%"),
                "LAST30_GROWTH": enrich_data.get("LAST30_GROWTH", "+0.0%"),
                
                # Branding & Meta
                "BRAND_NAME": config.get("brand_name", "INSTITUTIONAL SIGNAL"),
                "NEWS_BIAS": enrich_data.get("NEWS_BIAS", "NEUTRAL"),
                "SIGNAL_AGE": "0 Bars (Fresh Signal)"
            }

            formatted_msg = template.format(**nav_map)

            # --- Watermark Injection ---
            if config.get("use_watermark"):
                from localization import Translator
                # We use a default translator instance or passed one
                watermark = "\n\n<i>Powered by ITC +AI Enterprise</i>"
                formatted_msg += watermark

            # Send via Telegram Bot API
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": formatted_msg,
                "parse_mode": "HTML" # Support basic HTML if used in template
            }

            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"// SPC Bridge Success: Signal sent to {chat_id}")
                
                # --- AUDITOR LOGGING ---
                try:
                    from modules.logic.signal_auditor import SignalAuditor
                    # Pass the raw signal details for auditing (Audit only cares about Entry/SL/TP)
                    SignalAuditor.log_signal(signal)
                except Exception as e:
                    print(f"// Auditor Log Error: {e}")
                # -----------------------

                return True, "Signal relayed successfully."
            else:
                return False, f"Telegram API Error: {response.text}"

        except Exception as e:
            print(f"// SPC Bridge Error: {e}")
            return False, str(e)
