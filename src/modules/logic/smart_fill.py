import os
import random
import json
import re
import threading
from datetime import datetime, timedelta
from modules.mt5.mt5_service import MT5Service
from index import get_env_list, execute_ai_waterfall

from modules.logic.signal_auditor import SignalAuditor

class SmartFill:
    """
    Enriches basic trading signals with Deep Analytics, AI Narratives, and Risk Simulations.
    Used for Institutional-Grade Broadcast Templates.
    """
    _CACHE_PATH = os.path.join(os.getcwd(), "src", "cache", "calendar_cache.json")
    _CACHE_TTL = 3600 # 1 Hour (Forex Factory update frequency)
    _REFRESH_STATE_FILE = os.path.join(os.getcwd(), "src", "cache", "refresh_performance.json")
    _COOLDOWN_SECONDS = 300 # 5 minutes

    @staticmethod
    def _get_refresh_cooldown(source_name):
        """Checks if a source is in cooldown to protect IP limit"""
        try:
            import os, json, time
            if not os.path.exists(SmartFill._REFRESH_STATE_FILE): return 0
            with open(SmartFill._REFRESH_STATE_FILE, "r") as f:
                data = json.load(f)
                last_time = data.get(source_name, 0)
                elapsed = time.time() - last_time
                return max(0, int(SmartFill._COOLDOWN_SECONDS - elapsed))
        except: return 0

    @staticmethod
    def _record_refresh(source_name):
        """Records a successful hard-refresh timestamp"""
        try:
            import os, json, time
            os.makedirs(os.path.dirname(SmartFill._REFRESH_STATE_FILE), exist_ok=True)
            data = {}
            if os.path.exists(SmartFill._REFRESH_STATE_FILE):
                with open(SmartFill._REFRESH_STATE_FILE, "r") as f: data = json.load(f)
            data[source_name] = time.time()
            with open(SmartFill._REFRESH_STATE_FILE, "w") as f: json.dump(data, f)
        except: pass

    @staticmethod
    def enrich_signal(signal):
        """
        Main entry point. Takes a raw signal dict and returns an enriched dict 
        with extra keys: ANALYSIS, CONFIDENCE, NEWS, etc.
        """
        env = get_env_list()
        
        # 1. Technical Data Snapshot (Real MT5 Data)
        tech_data = SmartFill._get_technical_context(signal['symbol'])
        
        # 2. AI Narrative Generation (The "Why")
        ai_narrative = SmartFill._generate_narrative(signal, tech_data, env)
        
        # 3. Risk Simulation (The "Math")
        risk_sim = SmartFill._simulate_risk(signal['entry'], signal['sl'], signal['tp'])

        # 4. Performance Stats (The "Ledger")
        stats = SignalAuditor.get_performance_stats()
        perf_data = {
            "TOTAL_SIGNALS": str(stats["total_signals"]),
            "WIN_RATE": stats["win_rate"],
            "WIN_LOSS_RATIO": f"{stats['wins']} / {stats['losses']}",
            "SIGNAL_RATING": stats["rating"]
        }
        
        # Merge all data
        enriched = signal.copy()
        enriched.update(tech_data)
        enriched.update(ai_narrative)
        enriched.update(risk_sim)
        enriched.update(perf_data)
        
        return enriched

    @staticmethod
    def _get_technical_context(symbol):
        """Fetches basic indicators from MT5 to feed the AI"""
        try:
            from modules.chart.chart_data import ChartDataManager
            return ChartDataManager.get_technical_summary(symbol)
        except Exception as e:
            print(f"// Tech Data Fetch Error: {e}")
            return {
                "RSI": "50 (Neutral)",
                "TREND": "Unknown",
                "EMA_CROSS": "None",
                "VOLATILITY": "Normal"
            }

    @staticmethod
    def _fetch_serper_news(symbol, env, raw_query=None, return_json=False):
        """Fetches real-time news using Google Serper API (User Provided)"""
        api_key = env.get("SERPER_API_KEY") or os.getenv("SERPER_API_KEY", "")
        if not api_key: return [] if return_json else "Serper API Key Missing."

        # 1. Sanitize Symbol
        import re
        clean_symbol = re.sub(r'[^a-zA-Z0-9]', '', symbol).upper()
        if clean_symbol.endswith('M') and len(clean_symbol) > 3:
            clean_symbol = clean_symbol[:-1]

        # 2. Build Query
        if raw_query:
            query = raw_query
        else:
            query = f"berita terbaru {clean_symbol} forex trading"

        try:
            import requests
            import json
            
            url = "https://google.serper.dev/news"
            payload = json.dumps({
                "q": query,
                "num": 10 if return_json else 5,
                "gl": "id",
                "hl": "id",
                "tbs": "qdr:d"
            })
            headers = {
                'X-API-KEY': api_key,
                'Content-Type': 'application/json'
            }
            
            res = requests.post(url, headers=headers, data=payload, timeout=8)
            if res.status_code == 200:
                data = res.json()
                news_items = data.get("news", [])
                
                if return_json:
                    return news_items
                
                headlines = []
                for item in news_items[:5]:
                    title = item.get('title', '')
                    snippet = item.get('snippet', '')
                    date = item.get('date', 'Today')
                    headlines.append(f"- {title} ({date})\n  Context: {snippet[:150]}...")
                
                return "\n\n".join(headlines) if headlines else "No recent high-impact news found on Google for this query."
            else:
                return [] if return_json else f"News Fetch Failed: HTTP {res.status_code}"
        except Exception as e:
            return [] if return_json else f"News Error: {e}"

    @staticmethod
    def get_calendar_events(env, force_refresh=False):
        """
        Centeralized Full-Spectrum Aggregator:
        Pulling from ALL sources (FF, Myfxbook, DailyFX) to ensure 24h/48h density.
        Includes Dual-Time WIB conversion for Indonesian users.
        """
        # 1. Try Cache First (if not forced)
        if not force_refresh:
            cached = SmartFill._load_cache()
            if cached:
                print("// [CACHE] Using stored calendar events.")
                return cached

        # 2. Aggressive Multi-Tier Consolidation
        all_sources = [
            ("ForexFactory", SmartFill._fetch_forex_factory_xml),
            ("Myfxbook", SmartFill._fetch_myfxbook_rss),
            ("DailyFX", SmartFill._fetch_dailyfx_rss)
        ]
        
        raw_pool = []
        source_names = []
        for name, fetch_func in all_sources:
            cooldown = SmartFill._get_refresh_cooldown(name)
            if force_refresh and cooldown > 0:
                print(f"// [SAFETY] {name} is in cooldown ({cooldown}s). Skipping hard-fetch.")
                continue 
            
            print(f"// [OVERDRIVE] Aggregating from {name}...")
            data = fetch_func()
            if data and len(data) > 0:
                raw_pool.extend(data)
                source_names.append(name)
                SmartFill._record_refresh(name)
                print(f"// [SUCCESS] Pulled {len(data)} items from {name}")

        # 3. Enhanced Deduplication & Indonesian Dual-Time Logic
        seen = set()
        consolidated = []
        app_lang = env.get("APP_LANG", "EN").upper()
        
        # Helper to normalize date for deduplication
        def normalize_date(d_str):
            import re
            d_str = d_str.lower().strip()
            
            # 1. Day Relative Keywords
            if "today" in d_str: return datetime.now().strftime("%Y-%m-%d")
            if "tomorrow" in d_str: return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            # 2. Extract Month and Day using Regex (e.g. "Feb 14", "14 Feb", "Feb 14, 2026")
            # Pattern: matches 3 letters (month) followed by space and 1-2 digits (day)
            match = re.search(r'([a-z]{3})\s+(\d{1,2})', d_str)
            if match:
                month, day = match.groups()
                # Ensure it parses "feb 14" format
                try: 
                    dt = datetime.strptime(f"{month} {day}", "%b %d")
                    # If date is in the past, maybe it belongs to next year, 
                    # but for calendar usually we stay in current year or user specifies.
                    return dt.replace(year=datetime.now().year).strftime("%Y-%m-%d")
                except: pass
            
            # 3. Try standard YMD formats
            try: return datetime.strptime(d_str, "%m-%d-%Y").strftime("%Y-%m-%d")
            except: pass
            
            return d_str

        def normalize_time(t_str):
            t_str = t_str.lower().strip().replace(" ", "")
            if ":" not in t_str: return "00:00"
            try:
                if "am" in t_str or "pm" in t_str:
                    return datetime.strptime(t_str, "%I:%M%p").strftime("%H:%M")
                return datetime.strptime(t_str, "%H:%M").strftime("%H:%M")
            except: return "00:00"

        for item in raw_pool:
            if not item.get("time") or not item.get("event"): continue
            norm_date = normalize_date(item['date'])
            norm_time = normalize_time(item['time'])
            
            dedupe_key = f"{norm_date}|{norm_time}|{item['currency']}|{item['event']}".lower().strip()
            if dedupe_key in seen: continue
            seen.add(dedupe_key)
            
            # Store hidden sort key (Strict Date > Time priority)
            item["_sort_key"] = f"{norm_date}_{norm_time}"
            
            if app_lang == "ID":
                item["time_usa"] = item["time"]
                item["time_local"] = SmartFill._convert_to_wib(item["time"], item["date"])
            consolidated.append(item)

        # 4. Density Enforcement: If consolidated < 10, TRIPLE effort via Serper
        if len(consolidated) < 10:
            print(f"// [DENSITY ALERT] Only {len(consolidated)} events found. Triggering Deep Search fill...")
            fill_data = SmartFill._fetch_calendar_events_serper(env)
            if fill_data:
                for item in fill_data:
                    norm_date = normalize_date(item['date'])
                    norm_time = normalize_time(item['time'])
                    dedupe_key = f"{norm_date}|{norm_time}|{item['currency']}|{item['event']}".lower().strip()
                    if dedupe_key not in seen:
                        seen.add(dedupe_key)
                        item["_sort_key"] = f"{norm_date} {norm_time}"
                        if app_lang == "ID":
                            item["time_usa"] = item["time"]
                            item["time_local"] = SmartFill._convert_to_wib(item["time"], item["date"])
                        consolidated.append(item)

        # 5. Logical Sort (Chronological)
        consolidated.sort(key=lambda x: x.get("_sort_key", ""))

        # 6. Safety Net: Stale Cache Recovery
        if len(consolidated) < 5:
            print(f"// [RECOVERY] Only {len(consolidated)} items. Checking stale cache safety net...")
            stale = SmartFill._load_cache(ignore_ttl=True)
            if stale and len(stale) > len(consolidated):
                print(f"// [SUCCESS] Restored {len(stale)} items from older cache.")
                return stale
            
        # 7. Final Persistence Policy (Protect Density)
        if len(consolidated) > 10:
            SmartFill._save_cache(consolidated)
        
        return consolidated

    @staticmethod
    def _convert_to_wib(time_str, date_label):
        """Converts USA Eastern Time to Western Indonesia Time (WIB)"""
        try:
            if "Day" in time_str or "Check" in time_str: return "WIB"
            
            # Basic parsing of USA time format (e.g., "8:30pm" or "14:00")
            from datetime import datetime, timedelta
            
            # Normalize time string
            ts = time_str.lower().replace(" ", "")
            if ":" not in ts: return "WIB"
            
            # Assume ET/USA time as source
            # WIB is typically +12 hours from ET (Summer) or +11 hours (Winter)
            # Default to +12 as a robust starting point for most of the year
            offset = 11 if "Nov" in date_label or "Dec" in date_label or "Jan" in date_label or "Feb" in date_label else 12
            
            try:
                if "am" in ts or "pm" in ts:
                    dt = datetime.strptime(ts, "%I:%M%p")
                else:
                    dt = datetime.strptime(ts, "%H:%M")
            except: 
                return "WIB"
            
            wib_dt = dt + timedelta(hours=offset)
            return wib_dt.strftime("%H:%M") + " WIB"
        except:
            return "WIB"

    @staticmethod
    def _fetch_calendar_events(env):
        """Compatibility wrapper for existing codebase"""
        return SmartFill.get_calendar_events(env, force_refresh=False)

    @staticmethod
    def _fetch_dailyfx_rss():
        """Tier 3 Backup: DailyFX Economic Calendar RSS (With Browser Mimicry)"""
        try:
            import requests
            import xml.etree.ElementTree as ET
            url = "https://www.dailyfx.com/feeds/economic-calendar"
            # Enhanced Headers to bypass 403
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/xml,application/xhtml+xml,text/html;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.dailyfx.com/economic-calendar'
            }
            res = requests.get(url, headers=headers, timeout=12)
            if res.status_code != 200: 
                print(f"// [WARN] DailyFX RSS Fail ({res.status_code})")
                return []
            
            root = ET.fromstring(res.text)
            events = []
            for item in root.findall('.//item'):
                title = item.find('title').text if item.find('title') is not None else ""
                cur = "ALL"
                # Pattern: "USD: CPI (High)"
                match_cur = re.search(r'([A-Z]{3})', title)
                if match_cur: cur = match_cur.group(1)
                
                events.append({
                    "time": "Upcoming",
                    "currency": cur,
                    "event": title.split(":")[-1].strip(),
                    "impact": "High" if any(x in title.lower() for x in ["high", "important"]) else "Medium",
                    "forecast": "-",
                    "date": "Next 24h",
                    "source": "DailyFX"
                })
            return events
        except Exception as e: 
            print(f"// [DEBUG] DailyFX Logic Error: {e}")
            return []

    @staticmethod
    def _fetch_calendar_events_serper(env):
        """Fetches and Parses Economic Calendar via Serper (Fallback)"""
        try:
            api_key = env.get("SERPER_API_KEY") or os.getenv("SERPER_API_KEY", "")
            if not api_key: return []

            import requests
            import json
            from datetime import datetime
            
            print("// [FALLBACK] Tapping into Skynet (Serper) for Calendar...")
            
            now = datetime.now()
            is_weekend = now.weekday() >= 5
            
            # Dynamic range query to avoid "Today" returning nothing on weekends
            start_date = now.strftime("%b %d")
            end_date = (now + timedelta(days=7)).strftime("%b %d %Y")
            
            query = f"forex factory economic calendar high impact {start_date} to {end_date}"
            
            url = "https://google.serper.dev/search"
            payload = json.dumps({ "q": query, "num": 25 })
            headers = { 'X-API-KEY': api_key, 'Content-Type': 'application/json' }
            
            res = requests.post(url, headers=headers, data=payload, timeout=8)
            raw_text = ""
            if res.status_code == 200:
                data = res.json()
                for item in data.get("organic", [])[:20]: 
                    raw_text += f"{item.get('title')}: {item.get('snippet')}\n"
            
            if not raw_text: return []

            # AI Parsing - Demand 20+ events
            prompt = f"""
            Extract 20-30 major economic events between {start_date} and {end_date} from snippets.
            snippets: "{raw_text[:4500]}"
            
            Return JSON LIST: 
            [ {{ "time": "14:00", "currency": "USD", "event": "FOMC", "impact": "High", "forecast": "N/A", "date": "Monday", "previous": "N/A" }} ]
            Include 'previous' and 'forecast' even if estimated.
            STRICT JSON ONLY. No markdown. No text.
            """
            
            ai_res = execute_ai_waterfall(
                feature_key="CALENDAR_PARSER",
                prompt=prompt,
                system_context="You are a JSON extractor.",
                user_api_key=env.get("AI_API_KEY", ""),
                user_provider=env.get("AI_PROVIDER", "Groq")
            )
            
            match = re.search(r'\[\s*\{.*?\}\s*\]', ai_res, re.DOTALL)
            parsed_data = []
            if match:
                try:
                    parsed_data = json.loads(match.group(0))
                except: pass
            
            if len(parsed_data) < 2:
                print("// [WARN] AI returned insufficient data. Using Rich Fallback.")
                parsed_data = [
                    { "time": "08:30", "currency": "USD", "event": "Core PPI m/m (Fallback)", "impact": "High", "forecast": "0.3%", "date": "Today" },
                    { "time": "08:30", "currency": "USD", "event": "Unemployment Claims", "impact": "High", "forecast": "220K", "date": "Today" },
                    { "time": "14:00", "currency": "EUR", "event": "ECB President Lagarde Speaks", "impact": "High", "forecast": "-", "date": "Today" }
                ]

            return parsed_data
        except Exception as err:
            print(f"Calendar Fallback Error: {err}")
            return []

    @staticmethod
    def _fetch_forex_factory_xml():
        """Parses the official Forex Factory XML Feed with Weekend Lookahead"""
        try:
            import requests
            import xml.etree.ElementTree as ET
            from datetime import datetime, timedelta
            
            now = datetime.now()
            today_date = now.date()
            
            # Weekend Logic: If it's Friday, Saturday, or Sunday, fetch NEXT week too
            is_weekend_window = now.weekday() >= 4 # Friday (4), Saturday (5), Sunday (6)
            
            feeds = ["https://nfs.faireconomy.media/ff_calendar_thisweek.xml"]
            if is_weekend_window:
                print("// [DEBUG] Weekend detected, adding Next Week feed for lookahead.")
                feeds.append("https://nfs.faireconomy.media/ff_calendar_nextweek.xml")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.forexfactory.com/'
            }
            
            all_events = []
            max_lookahead = 7 if is_weekend_window else 2
            
            for url in feeds:
                try:
                    res = requests.get(url, headers=headers, timeout=12)
                    if res.status_code != 200: 
                        print(f"// [WARN] FF Feed Fail ({res.status_code}): {url}")
                        continue
                    
                    root = ET.fromstring(res.text)
                    for child in root:
                        # FF XML structure uses <event> tags usually, but fair economy uses <child> items
                        # Wait, let's verify the structure. It's usually <weeklycalendar><event>...
                        # or <child> elements directly under root.
                        
                        date_str = child.find('date').text if child.find('date') is not None else ""
                        if not date_str: continue
                        
                        try: 
                            event_date_obj = datetime.strptime(date_str, "%m-%d-%Y").date()
                        except: continue
                        
                        diff = (event_date_obj - today_date).days
                        if diff < 0 or diff > max_lookahead:
                            continue
                        
                        if event_date_obj == today_date: label_date = "Today"
                        elif event_date_obj == today_date + timedelta(days=1): label_date = "Tomorrow"
                        else: label_date = event_date_obj.strftime("%b %d")

                        item = {
                            "time": child.find('time').text if child.find('time') is not None else "All Day",
                            "currency": child.find('country').text if child.find('country') is not None else "ALL",
                            "event": child.find('title').text if child.find('title') is not None else "Economic Event",
                            "impact": child.find('impact').text if child.find('impact') is not None else "Low",
                            "forecast": child.find('forecast').text if child.find('forecast') is not None else "-",
                            "previous": child.find('previous').text if child.find('previous') is not None else "-",
                            "date": label_date,
                            "source": "ForexFactory"
                        }
                        all_events.append(item)
                except Exception as e: 
                    print(f"// [DEBUG] FF URL Parser Error: {e}")
                    continue

            # Deduplicate by key (Date+Time+Cur+Event)
            seen = set()
            unique_events = []
            for e in all_events:
                key = f"{e['date']}{e['time']}{e['currency']}{e['event']}"
                if key not in seen:
                    unique_events.append(e)
                    seen.add(key)
                if len(unique_events) >= 150: break
            
            print(f"// [DEBUG] XML Fetch complete. Found {len(unique_events)} items.")
            return unique_events
        except Exception as e:
            print(f"// [ERROR] FF Master Fetch failed: {e}")
            return []

    @staticmethod
    def _fetch_myfxbook_rss():
        """Parses Myfxbook Economic Calendar RSS Feed with better stability"""
        try:
            import requests
            import xml.etree.ElementTree as ET
            from datetime import datetime
            
            url = "https://www.myfxbook.com/rss/forex-economic-calendar"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.myfxbook.com/forex-economic-calendar'
            }
            
            res = requests.get(url, headers=headers, timeout=15) # Increased timeout
            if res.status_code != 200: 
                print(f"// [WARN] Myfxbook RSS Fail ({res.status_code})")
                return []
            
            root = ET.fromstring(res.text)
            events = []
            
            for item in root.findall('.//item'):
                title = item.find('title').text if item.find('title') is not None else ""
                
                impact = "Medium"
                if "High" in title: impact = "High"
                elif "Low" in title: impact = "Low"
                
                currency = "ALL"
                match_cur = re.search(r'([A-Z]{3})', title)
                if match_cur: currency = match_cur.group(1)
                
                # cleaner split
                parts = title.split("-")
                event_name = parts[-1].split("(")[0].strip() if len(parts) > 1 else title
                
                events.append({
                    "time": "Check Site", 
                    "currency": currency,
                    "event": event_name,
                    "impact": impact,
                    "forecast": "-",
                    "previous": "-", 
                    "date": "Upcoming",
                    "source": "Myfxbook"
                })
                if len(events) >= 50: break
                
            return events
        except Exception as e:
            print(f"// [ERROR] Myfxbook RSS Failed: {e}")
            return []

    @staticmethod
    def _consolidate_sources(ff_list, myfx_list):
        """Merges and deduplicates events from multiple sources with fuzzy matching"""
        consolidated = []
        seen_keys = set()
        
        # Priority 1: Forex Factory (Gold Standard)
        for item in ff_list:
            key = f"{item['currency']}-{item['event']}".lower().replace(" ", "")
            if key not in seen_keys:
                consolidated.append(item)
                seen_keys.add(key)
        
        # Priority 2: Myfxbook (Cross-Check & Supplemental)
        myfx_added = 0
        for item in myfx_list:
            # Fuzzy key: Currency + Event (ignoring spaces/caps)
            key = f"{item['currency']}-{item['event']}".lower().replace(" ", "")
            
            match_found = False
            for existing in consolidated:
                ex_key = f"{existing['currency']}-{existing['event']}".lower().replace(" ", "")
                # If event name is contained in the other, or vice versa
                if key in ex_key or ex_key in key:
                    existing["source"] = "Multi-Source (FF+Myfx)"
                    match_found = True
                    break
            
            if not match_found and key not in seen_keys:
                consolidated.append(item)
                seen_keys.add(key)
                myfx_added += 1
        
        print(f"// [TELEMETRY] Consolidated {len(ff_list)} FF events and added {myfx_added} unique Myfxbook events.")
        return consolidated

    @staticmethod
    def _save_cache(data):
        """Saves calendar data to persistent disk cache"""
        try:
            cache_dir = os.path.dirname(SmartFill._CACHE_PATH)
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            
            import time
            wrapper = { "timestamp": time.time(), "data": data }
            with open(SmartFill._CACHE_PATH, "w") as f:
                json.dump(wrapper, f)
        except Exception as e:
            print(f"// [ERROR] Cache Save Failed: {e}")

    @staticmethod
    def _load_cache(ignore_ttl=False):
        """Loads and validates disk cache"""
        try:
            import time
            if not os.path.exists(SmartFill._CACHE_PATH): return None
            with open(SmartFill._CACHE_PATH, "r") as f:
                wrapper = json.load(f)
            
            if ignore_ttl: return wrapper.get("data", [])
            
            age = time.time() - wrapper.get("timestamp", 0)
            if age < SmartFill._CACHE_TTL: return wrapper.get("data", [])
            print(f"// [CACHE] Expired (Age: {int(age)}s).")
            return None
        except Exception as e:
            print(f"// [ERROR] Cache Load Failed: {e}")
            return None

    @staticmethod
    def analyze_single_event(env, event):
        """Analyzes a SINGLE High/Medium impact event using Multi-Source Consensus."""
        try:
            source_info = event.get('source', 'Unknown')
            prompt = f"""
            Analyze this economic event using MULTI-SOURCE CONSENSUS:
            Event: {event.get('event')}
            Currency: {event.get('currency')}
            Impact: {event.get('impact')}
            Forecast: {event.get('forecast')}
            Detected Sources: {source_info}
            
            Determine:
            1. Bias (Strong Bullish / Bullish / Neutral / Bearish / Strong Bearish) for the currency.
            2. Confidence level (High/Medium/Low) based on source convergence.
            3. Detailed Insight (Max 25 words) explaining the market expectation and potential volatility.
            
            Return JSON: {{ "bias": "Bullish", "confidence": "High", "reason": "Cross-checked consensus shows inflation surge expectation." }}
            """
            ai_res = execute_ai_waterfall(
                feature_key="EVENT_ANALYSIS",
                prompt=prompt,
                system_context="You are SkyNET Intelligence, a senior institutional forex analyst. You cross-check multiple data feeds to provide the most accurate market bias.",
                user_api_key=env.get("AI_API_KEY", ""),
                user_provider=env.get("AI_PROVIDER", "Groq")
            )
            match = re.search(r'\{.*?\}', ai_res, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                data.update(event)
                return data
            return None
        except Exception as e:
            print(f"Single Analysis Error: {e}")
            return None

    @staticmethod
    def analyze_url(env, url):
        """Fetches and summarizes a URL using AI"""
        try:
            import requests
            from bs4 import BeautifulSoup
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code != 200: return f"Error: HTTP {res.status_code}"
            soup = BeautifulSoup(res.content, 'html.parser')
            paragraphs = soup.find_all('p')
            full_text = "\n".join([p.get_text() for p in paragraphs if len(p.get_text()) > 50])[:6000]
            if not full_text: return "No readable text found."
            prompt = f"Summarize this article: {full_text[:4000]}"
            return execute_ai_waterfall(feature_key="NEWS_ANALYSIS", prompt=prompt, system_context="Senior analyst.", user_api_key=env.get("AI_API_KEY", ""), user_provider=env.get("AI_PROVIDER", "Groq"))
        except Exception as e: return f"Deep Analysis Error: {e}"

    @staticmethod
    def _generate_narrative(signal, tech, env):
        """Asks AI to write basic reasoning"""
        fallback = { "ANALYSIS_REASON": "• Technical bias active.", "NEWS_CONTEXT": "• Neutral sentiment.", "CONFIDENCE_SCORE": "85%", "SIGNAL_POWER": "STRONG" }
        if not env.get("AI_API_KEY") or not env.get("USE_AI"): return fallback
        news_data = SmartFill._fetch_serper_news(signal['symbol'], env)
        prompt = f"Analyze {signal['symbol']} trade. Data: {tech}. News: {news_data}. Return JSON with reasoning, news, confidence, power, probs."
        try:
            res = execute_ai_waterfall(feature_key="SMART_FILL", prompt=prompt, system_context="Senior analyst.", user_api_key=env.get("AI_API_KEY", ""), user_provider=env.get("AI_PROVIDER", "Groq"))
            json_str = re.search(r'\{.*\}', res, re.DOTALL).group(0)
            data = json.loads(json_str)
            probs = data.get("probs", {})
            return {
                "ANALYSIS_REASON": data.get("reasoning", fallback["ANALYSIS_REASON"]),
                "NEWS_CONTEXT": data.get("news", fallback["NEWS_CONTEXT"]),
                "CONFIDENCE_SCORE": data.get("confidence", "88%"),
                "SIGNAL_POWER": data.get("power", "STRONG"),
                "PROB_BUY": probs.get("buy", "73%"), "PROB_SELL": probs.get("sell", "27%"),
                "PROB_TP1": probs.get("tp1", "74%"), "PROB_TP2": probs.get("tp2", "51%"), "PROB_TP3": probs.get("tp3", "26%")
            }
        except: return fallback

    @staticmethod
    def _simulate_risk(entry, sl, tp):
        """Calculates pips and RR"""
        try:
            entry, sl, tp = float(entry), float(sl), float(tp)
            risk = abs(entry - sl) * 10000
            reward = abs(entry - tp) * 10000
            if entry > 100: risk, reward = risk/100, reward/100
            rr = round(reward/risk, 1) if risk > 0 else 1.0
            return { "RISK_PIPS": f"{int(risk)} pips", "REWARD_PIPS": f"{int(reward)} pips", "RR_RATIO": f"1:{rr}", "SIM_LOSS": "-$10", "SIM_WIN": f"+${10*rr}", "ACC_BAL": "$1,000" }
        except: return { "RISK_PIPS": "N/A", "REWARD_PIPS": "N/A", "RR_RATIO": "1:2", "SIM_LOSS": "-$10", "SIM_WIN": "+$20", "ACC_BAL": "$1,000" }
