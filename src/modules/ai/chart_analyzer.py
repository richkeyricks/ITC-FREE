# src/modules/ai/chart_analyzer.py

# --- IMPORTS ---
import os
import json
import base64
import requests
from groq import Groq
from configs.ai_config import MASTER_GROQ_KEY

class AIChartAnalyzer:
    """
    Uses Multi-Provider AI Vision to analyze trading charts.
    Supports Groq (Default/Master), Gemini, and OpenRouter.
    """
    
    def __init__(self, api_key=None, provider=None, model_id=None):
        self.update_settings(api_key, provider, model_id)
            
    def update_settings(self, api_key=None, provider=None, model_id=None):
        """Updates internal settings from .env or manual input"""
        from dotenv import load_dotenv
        load_dotenv(override=True)
        self.user_api_key = api_key or os.getenv("AI_API_KEY")
        self.provider = provider or os.getenv("AI_PROVIDER", "Groq")
        self.model_id = model_id or os.getenv("OR_MODEL", "")
            
    def encode_image(self, image_path):
        """Encodes image to base64 for Groq/OpenRouter API"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_chart(self, image_path, symbol, signal_type, entry, tp, sl):
        """
        Routes the analysis to the appropriate provider via Waterfall.
        """
        from index import execute_ai_waterfall
        prompt = self._get_prompt(symbol, signal_type, entry, tp, sl)
        
        # Pass image path as extra context for vision features
        return execute_ai_waterfall(
            feature_key="VISION_ANALYSIS",
            prompt=prompt,
            system_context="You are a professional technical chart analyst.",
            user_api_key=self.user_api_key if self.user_api_key != MASTER_GROQ_KEY else "",
            user_provider=self.provider,
            image_path=image_path
        )

    def _get_prompt(self, symbol, signal_type, entry, tp, sl):
        return f"""
        Analyze this trading chart for {symbol}. 
        A signal was detected: {signal_type} at {entry}, TP: {tp}, SL: {sl}.
        
        Please provide a professional technical analysis including:
        1. Verdict: VALID or INVALID
        2. Accuracy Score: 0-100%
        3. Detailed Reasoning: Mention trend, support/resistance, and patterns.
        
        Respond strictly in JSON format:
        {{
            "verdict": "VALID",
            "accuracy": 75,
            "reasoning": "...",
            "trend": "Bullish/Bearish",
            "key_levels": ["Level 1", "Level 2"]
        }}
        """

    # --- DEPRECATED LOCAL ANALYZERS (Now handled by Waterfall in index.py) ---

    def _parse_json(self, content):
        """Robust JSON parsing for AI responses"""
        try:
            content = content.strip()
            if "{" in content and "}" in content:
                json_str = content[content.find("{"):content.rfind("}")+1]
                return json.loads(json_str)
            return {"error": "Invalid JSON format from AI"}
        except Exception as e:
            return {"error": f"JSON Parse Error: {e}"}
