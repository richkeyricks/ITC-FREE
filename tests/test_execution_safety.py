import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

class TestExecutionSafety(unittest.TestCase):
    """
    Unit tests for core trading safety and execution logic in index.py.
    Uses extensive mocking to avoid real MT5 connections.
    """

    def setUp(self):
        # Mock Config and DB managers that are instantiated at module level
        self.patcher_db = patch('index.db_manager')
        self.mock_db = self.patcher_db.start()
        
        self.patcher_mt5 = patch('index.mt5')
        self.mock_mt5 = self.patcher_mt5.start()
        
        # Reset mocks
        self.mock_mt5.initialize.return_value = True
        self.mock_mt5.terminal_info.return_value.connected = True
        
    def tearDown(self):
        self.patcher_db.stop()
        self.patcher_mt5.stop()

    @patch('index.LimitManager')
    @patch('index.get_env_list')
    def test_daily_limit_reached(self, mock_get_env, mock_limit_manager, mock_check_limit=None):
        """Verify that trade is BLOCKED when daily limit is reached."""
        from index import execute_trade
        
        # Scenario: LimitManager says NO
        mock_limit_manager.check_limit_strict.return_value = (False, "Daily Limit Reached")
        mock_get_env.return_value = {"REPORT_BOT_TOKEN": "", "REPORT_CHAT_ID": ""}
        
        signal = {"symbol": "GOLD", "type": "BUY", "entry": 2000, "sl": 1990, "tp": 2020}
        
        execute_trade(signal)
        
        # Verify order_send was NEVER called
        self.mock_mt5.order_send.assert_not_called()

    @patch('index.check_equity_guard')
    @patch('index.LimitManager')
    @patch('index.get_env_list')
    def test_equity_guard_block(self, mock_get_env, mock_limit_manager, mock_equity_guard):
        """Verify that trade is BLOCKED when equity guard (drawdown) is triggered."""
        from index import execute_trade
        
        mock_limit_manager.check_limit_strict.return_value = (True, "OK")
        mock_equity_guard.return_value = False # Drawdown too high
        mock_get_env.return_value = {
            "MT5_LOGIN": 123, "MT5_PASSWORD": "abc", "MT5_SERVER": "sec",
            "DAILY_LOSS_LIMIT": 5.0, "TRADE_START_HOUR": 0, "TRADE_END_HOUR": 24,
            "REPORT_BOT_TOKEN": "", "REPORT_CHAT_ID": ""
        }
        
        signal = {"symbol": "GOLD", "type": "BUY", "entry": 2000, "sl": 1990, "tp": 2020}
        
        execute_trade(signal)
        
        # Verify order_send was NEVER called
        self.mock_mt5.order_send.assert_not_called()

    @patch('index.LimitManager')
    @patch('index.get_env_list')
    def test_lot_calculation_standard(self, mock_get_env, mock_limit_manager):
        """Verify dynamic lot calculation logic."""
        from index import execute_trade
        
        mock_limit_manager.check_limit_strict.return_value = (True, "OK")
        mock_get_env.return_value = {
            "MT5_LOGIN": 123, "MT5_PASSWORD": "abc", "MT5_SERVER": "sec",
            "FIXED_LOT": 0.0, # Dynamic
            "RISK_PERCENT": 1.0,
            "SYMBOL_SUFFIX": "",
            "MAGIC_NUMBER": 123456,
            "DAILY_LOSS_LIMIT": 10.0, "TRADE_START_HOUR": 0, "TRADE_END_HOUR": 24,
            "REPORT_BOT_TOKEN": "", "REPORT_CHAT_ID": ""
        }
        
        # Mock Account Info
        mock_acc = MagicMock()
        mock_acc.balance = 10000.0 # 1.0% risk = $100
        self.mock_mt5.account_info.return_value = mock_acc
        
        # Mock Symbol Info
        mock_sym = MagicMock()
        mock_sym.point = 0.01
        mock_sym.trade_tick_value = 1.0
        mock_sym.trade_tick_size = 0.01
        mock_sym.volume_step = 0.01
        mock_sym.volume_min = 0.01
        mock_sym.volume_max = 100.0
        mock_sym.filling_mode = 1
        self.mock_mt5.symbol_info.return_value = mock_sym
        
        # Mock Tick
        mock_tick = MagicMock()
        mock_tick.ask = 2000.0
        mock_tick.bid = 1999.0
        self.mock_mt5.symbol_info_tick.return_value = mock_tick
        
        # Signal: Entry 2000, SL 1990 -> Distance 10.0 (1000 points)
        # Risk $100 / (1000 points * tick_value_per_point)
        # In this code's formula: lot = risk_money / ((distance / tick_size) * tick_value)
        # lot = 100 / ((10.0 / 0.01) * 1.0) = 100 / 1000 = 0.10
        
        signal = {"symbol": "XAUUSD", "type": "BUY", "entry": 2000.0, "sl": 1990.0, "tp": 2020.0}
        
        execute_trade(signal)
        
        # Verify order_send was called with roughly 0.10 lot
        self.mock_mt5.order_send.assert_called()
        sent_request = self.mock_mt5.order_send.call_args[0][0]
        self.assertEqual(sent_request["volume"], 0.10)

    @patch('index.LimitManager.check_limit_strict')
    @patch('index.get_env_list')
    def test_symbol_aliasing(self, mock_get_env, mock_check_limit):
        """Verify that GOLD maps to XAUUSD and other aliases work."""
        from index import execute_trade
        
        mock_check_limit.return_value = (True, "OK")
        mock_get_env.return_value = {
            "MT5_LOGIN": 123, "FIXED_LOT": 0.1, "SYMBOL_SUFFIX": "",
            "DAILY_LOSS_LIMIT": 10.0, "TRADE_START_HOUR": 0, "TRADE_END_HOUR": 24,
            "REPORT_BOT_TOKEN": "", "REPORT_CHAT_ID": "", "MAGIC_NUMBER": 123
        }
        
        # Mock Symbol Info to only succeed for XAUUSD
        def sym_info_side_effect(sym):
            if sym == "XAUUSD": return MagicMock(filling_mode=1)
            return None
            
        self.mock_mt5.symbol_info.side_effect = sym_info_side_effect
        self.mock_mt5.symbol_info_tick.return_value = MagicMock(ask=2000)
        
        signal = {"symbol": "GOLD", "type": "BUY", "entry": 2000, "sl": 1990, "tp": 2020}
        
        execute_trade(signal)
        
        # Verify it tried to trade XAUUSD
        self.mock_mt5.symbol_select.assert_called_with("XAUUSD", True)
        sent_request = self.mock_mt5.order_send.call_args[0][0]
        self.assertEqual(sent_request["symbol"], "XAUUSD")

if __name__ == "__main__":
    unittest.main()
