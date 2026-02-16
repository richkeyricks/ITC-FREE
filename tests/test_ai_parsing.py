import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath("src"))

class TestAIParsing(unittest.TestCase):
    """
    Tests for AI-powered signal parsing in index.py.
    Mocks external AI APIs (Groq, Ollama, OpenRouter).
    """

    @patch('index.call_groq')
    def test_ai_parse_groq_success(self, mock_call_groq):
        """Verify successful signal parsing from Groq mock response."""
        from index import ai_parse_signal
        
        # Mock Groq response
        mock_call_groq.return_value = '{"symbol": "EURUSD", "type": "SELL", "entry": 1.0820, "tp": 1.0750, "sl": 1.0880}'
        
        text = "Sell EURUSD now at 1.0820, TP 1.0750, SL 1.0880"
        result = ai_parse_signal(text, api_key="fake_key", provider="Groq")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["symbol"], "EURUSD")
        self.assertEqual(result["type"], "SELL")
        self.assertEqual(result["entry"], 1.0820)

    @patch('index.call_ollama')
    def test_ai_parse_ollama_success(self, mock_call_ollama):
        """Verify successful signal parsing from Ollama mock response."""
        from index import ai_parse_signal
        
        # Mock Ollama response
        mock_call_ollama.return_value = '{"symbol": "XAUUSD", "type": "BUY", "entry": 2030, "tp": 2040, "sl": 2025}'
        
        text = "XAUUSD Buy at 2030"
        result = ai_parse_signal(text, api_key="fake_key", provider="Ollama", ollama_url="http://fake", ollama_model="llama3.2")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["symbol"], "XAUUSD")
        self.assertEqual(result["type"], "BUY")

    @patch('index.call_groq')
    def test_ai_parse_groq_normalization(self, mock_call_groq):
        """Verify that AI parsing normalizes keys to lowercase."""
        from index import ai_parse_signal
        
        # Mock Groq response with mixed case keys
        mock_call_groq.return_value = '{"Symbol": "XAUUSD", "TYPE": "BUY", "Entry": 2030, "TP": 2040, "SL": 2025}'
        
        text = "XAUUSD Buy at 2030"
        result = ai_parse_signal(text, api_key="fake_key", provider="Groq")
        
        # Should be normalized to lowercase
        self.assertIn("symbol", result)
        self.assertIn("type", result)
        self.assertEqual(result["symbol"], "XAUUSD")
        self.assertEqual(result["type"], "BUY")

    @patch('index.call_groq')
    def test_ai_parse_malformed_json(self, mock_call_groq):
        """Verify that malformed JSON from AI is handled gracefully."""
        from index import ai_parse_signal
        
        # AI returns non-JSON text
        mock_call_groq.return_value = "I couldn't find a signal in that text."
        
        text = "Hello world"
        result = ai_parse_signal(text, api_key="fake_key", provider="Groq")
        
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
