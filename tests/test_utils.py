import pytest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
import unittest

from src.utils import (
    load_transactions,
    load_user_settings,
    get_currency_rates,
    get_stock_prices,
    format_date,
    get_greeting,
    get_card_info,
    get_top_transactions,
    get_expenses_data,
    get_income_data
)


@pytest.fixture
def sample_excel_data():
    """Фикстура с тестовыми данными транзакций."""
    data = {
        'Дата операции': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Дата платежа': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Номер карты': ['1234', '5678', '9012'],
        'Статус': ['OK', 'OK', 'FAILED'],
        'Сумма операции': [100.0, 200.0, 300.0],
        'Валюта операции': ['RUB', 'RUB', 'USD'],
        'Сумма платежа': [100.0, 200.0, 22500.0],
        'Валюта платежа': ['RUB', 'RUB', 'RUB'],
        'Кешбэк': [1.0, 2.0, 0.0],
        'Категория': ['Супермаркеты', 'Рестораны', 'Переводы'],
        'MCC': [5411, 5812, 4829],
        'Описание': ['Пятерочка', 'Макдоналдс', 'Перевод Иван И.'],
        'Бонусы (включая кешбэк)': [1.0, 2.0, 0.0],
        'Округление на Инвесткопилку': [0.0, 0.0, 0.0],
        'Сумма операции с округлением': [100.0, 200.0, 300.0]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_user_settings():
    """Фикстура с тестовыми пользовательскими настройками."""
    return {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }


@patch('pandas.read_excel')
def test_load_transactions(mock_read_excel, sample_excel_data):
    """Тест функции загрузки транзакций."""
    mock_read_excel.return_value = sample_excel_data
    result = load_transactions('dummy_path.xlsx')
    mock_read_excel.assert_called_once_with('dummy_path.xlsx')
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert 'Дата операции' in result.columns


@patch('builtins.open',
       new_callable=mock_open,
       read_data='{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}')
def test_load_user_settings(mock_file):
    """Тест функции загрузки пользовательских настроек."""
    result = load_user_settings()
    mock_file.assert_called_once_with('user_settings.json', 'r', encoding='utf-8')
    assert isinstance(result, dict)
    assert 'user_currencies' in result
    assert 'user_stocks' in result
    assert result['user_currencies'] == ["USD", "EUR"]
    assert result['user_stocks'] == ["AAPL", "AMZN"]


@patch('requests.get')
def test_get_currency_rates_with_pytest(mock_get):
    """Тест функции получения курсов валют с использованием pytest."""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'rates': {
            'USD': 73.21,
            'EUR': 87.08
        }
    }
    result = get_currency_rates(['USD', 'EUR'])
    assert len(result) == 2
    assert result[0]['currency'] == 'USD'
    assert result[0]['rate'] == 73.21
    assert result[1]['currency'] == 'EUR'
    assert result[1]['rate'] == 87.08


@patch('requests.get')
def test_get_stock_prices_with_pytest(mock_get):
    """Тест функции получения цен на акции с использованием pytest."""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'AAPL': {'price': 150.12},
        'AMZN': {'price': 3173.18}
    }
    result = get_stock_prices(['AAPL', 'AMZN'])
    assert len(result) == 2
    assert result[0]['stock'] == 'AAPL'
    assert result[0]['price'] == 150.12
    assert result[1]['stock'] == 'AMZN'
    assert result[1]['price'] == 3173.18


def test_format_date():
    """Тест функции форматирования даты."""
    date_str = '2023-01-15'
    result = format_date(date_str)
    assert result == '15.01.2023'


class TestUtilsWithUnittest(unittest.TestCase):
    """Тесты для вспомогательных функций с использованием unittest."""

    def test_get_greeting(self):
        """Тест функции get_greeting."""
        self.assertEqual(get_greeting("2023-01-01 08:00:00"), "Доброе утро")
        self.assertEqual(get_greeting("2023-01-01 14:00:00"), "Добрый день")
        self.assertEqual(get_greeting("2023-01-01 20:00:00"), "Добрый вечер")
        self.assertEqual(get_greeting("2023-01-01 02:00:00"), "Доброй ночи")

    def test_get_card_info(self):
        """Тест функции get_card_info."""
        result = get_card_info("2023-01-01 12:00:00")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, dict) for item in result))
        for card in result:
            self.assertIn("last_digits", card)
            self.assertIn("total_spent", card)
            self.assertIn("cashback", card)

    def test_get_top_transactions(self):
        """Тест функции get_top_transactions."""
        result = get_top_transactions("2023-01-01 12:00:00")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, dict) for item in result))
        for transaction in result:
            self.assertIn("date", transaction)
            self.assertIn("amount", transaction)
            self.assertIn("category", transaction)
            self.assertIn("description", transaction)

    @patch('src.utils.requests.get')
    def test_get_currency_rates_with_unittest(self, mock_get):
        """Тест функции get_currency_rates с использованием unittest."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"USD": 73.21, "EUR": 87.08}}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        result = get_currency_rates()
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, dict) for item in result))
        for rate in result:
            self.assertIn("currency", rate)
            self.assertIn("rate", rate)

    @patch('src.utils.requests.get')
    def test_get_stock_prices_with_unittest(self, mock_get):
        """Тест функции get_stock_prices с использованием unittest."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "AAPL": {"price": 150.12},
            "AMZN": {"price": 3173.18},
            "GOOGL": {"price": 2742.39},
            "MSFT": {"price": 296.71},
            "TSLA": {"price": 1007.08}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        result = get_stock_prices()
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, dict) for item in result))
        for stock in result:
            self.assertIn("stock", stock)
            self.assertIn("price", stock)

    def test_get_expenses_data(self):
        """Тест функции get_expenses_data."""
        df = pd.DataFrame({
            'Дата операции': ['2023-01-01', '2023-01-02'],
            'Сумма платежа': [1000, 2000],
            'Категория': ['Продукты', 'Переводы']
        })
        result = get_expenses_data(df, "2023-01-15", "M")
        self.assertIsInstance(result, dict)
        self.assertIn("total_amount", result)
        self.assertIn("main", result)
        self.assertIn("transfers_and_cash", result)

    def test_get_income_data(self):
        """Тест функции get_income_data."""
        df = pd.DataFrame({
            'Дата операции': ['2023-01-01', '2023-01-02'],
            'Сумма платежа': [-1000, -2000],
            'Категория': ['Зарплата', 'Проценты']
        })
        result = get_income_data(df, "2023-01-15", "M")
        self.assertIsInstance(result, dict)
        self.assertIn("total_amount", result)
        self.assertIn("main", result)


@patch('pandas.read_excel')
def test_load_transactions_real_file(mock_read_excel):
    """Тест загрузки реальных транзакций из файла."""
    test_df = pd.DataFrame({
        'Дата операции': ['2023-01-01', '2023-01-02'],
        'Сумма платежа': [100.0, 200.0],
        'Категория': ['Супермаркеты', 'Рестораны']
    })
    mock_read_excel.return_value = test_df
    df = load_transactions('data/Operations (1).xlsx')
    assert not df.empty
    assert 'Дата операции' in df.columns
    assert 'Сумма платежа' in df.columns
    assert 'Категория' in df.columns
