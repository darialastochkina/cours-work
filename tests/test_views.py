import json
import unittest
from unittest.mock import patch

from src.views import main_page


class TestViews(unittest.TestCase):
    @patch('src.views.get_greeting')
    @patch('src.views.get_card_info')
    @patch('src.views.get_top_transactions')
    @patch('src.views.get_currency_rates')
    @patch('src.views.get_stock_prices')
    def test_main_page(self, mock_stocks, mock_currencies, mock_transactions, mock_cards, mock_greeting):
        """Тест функции main_page."""
        mock_greeting.return_value = "Добрый день"
        mock_cards.return_value = [{"last_digits": "1234", "total_spent": 1000.0, "cashback": 10.0}]
        mock_transactions.return_value = [
            {"date": "01.01.2023", "amount": 100.0, "category": "Тест", "description": "Тест"}
        ]
        mock_currencies.return_value = [{"currency": "USD", "rate": 75.0}]
        mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}]
        result = main_page("2023-01-01 12:00:00")
        result_dict = json.loads(result)
        mock_greeting.assert_called_once()
        mock_cards.assert_called_once()
        mock_transactions.assert_called_once()
        mock_currencies.assert_called_once()
        mock_stocks.assert_called_once()
        self.assertEqual(result_dict["greeting"], "Добрый день")
        self.assertEqual(len(result_dict["cards"]), 1)
        self.assertEqual(len(result_dict["transactions"]), 1)
        self.assertEqual(len(result_dict["currencies"]), 1)
        self.assertEqual(len(result_dict["stocks"]), 1)


if __name__ == '__main__':
    unittest.main()
