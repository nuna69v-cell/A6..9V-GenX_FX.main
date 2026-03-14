import os
import unittest
from unittest.mock import MagicMock, Mock, patch

from core.execution.bybit import BybitAPI


class TestBybitAPI(unittest.TestCase):

    @patch("core.execution.bybit.HTTP")
    def test_get_market_data(self, mock_http):
        # Mock the session instance returned by HTTP
        mock_session = MagicMock()
        mock_http.return_value = mock_session

        # Mock the API response
        mock_session.get_kline.return_value = {"result": {"list": [1, 2, 3]}}

        # Initialize the API and call the method
        with patch.dict(
            os.environ,
            {"BYBIT_API_KEY": "test", "BYBIT_API_SECRET": "test"},
            clear=True,
        ):
            bybit_api = BybitAPI()
            data = bybit_api.get_market_data("BTCUSDT", "60", 3)

            # Assertions
            self.assertEqual(data, {"result": {"list": [1, 2, 3]}})
            mock_session.get_kline.assert_called_once_with(
                category="spot", symbol="BTCUSDT", interval="60", limit=3
            )

    @patch("core.execution.bybit.HTTP")
    def test_execute_order(self, mock_http):
        # Mock the session instance returned by HTTP
        mock_session = MagicMock()
        mock_http.return_value = mock_session

        # Mock the API response
        mock_session.place_order.return_value = {
            "retCode": 0,
            "result": {"orderId": "12345"},
        }

        with patch.dict(
            os.environ,
            {"BYBIT_API_KEY": "test", "BYBIT_API_SECRET": "test"},
            clear=True,
        ):
            bybit_api = BybitAPI()
            response = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

            # Assertions
            self.assertEqual(response, {"retCode": 0, "result": {"orderId": "12345"}})
            mock_session.place_order.assert_called_once_with(
                category="spot",
                symbol="BTCUSDT",
                side="Buy",
                orderType="Market",
                qty="0.01",
            )


if __name__ == "__main__":
    unittest.main()
