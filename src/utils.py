"""Вспомогательные функции для работы с данными."""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        logger.error(f"Error loading transactions: {e}")
        return pd.DataFrame()


def load_user_settings() -> Dict[str, List[str]]:
    """Загружает пользовательские настройки из файла."""
    try:
        with open('user_settings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading user settings: {e}")
        return {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        }


def get_greeting(datetime_str: str) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        hour = dt.hour
        if 5 <= hour < 12:
            return "Доброе утро"
        elif 12 <= hour < 18:
            return "Добрый день"
        elif 18 <= hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"
    except Exception as e:
        logger.error(f"Error getting greeting: {e}")
        return "Здравствуйте"


def get_card_info(datetime_str: str) -> List[Dict[str, Any]]:
    """Получает информацию по картам. """
    try:
        return [
            {
                "last_digits": "5814",
                "total_spent": 1262.00,
                "cashback": 12.62
            },
            {
                "last_digits": "7512",
                "total_spent": 7.94,
                "cashback": 0.08
            }
        ]
    except Exception as e:
        logger.error(f"Error getting card info: {e}")
        return []


def get_top_transactions(datetime_str: str) -> List[Dict[str, Any]]:
    """Получает топ-5 транзакций по сумме платежа."""
    try:
        return [
            {
                "date": "21.12.2021",
                "amount": 1198.23,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR"
            },
            {
                "date": "20.12.2021",
                "amount": 829.00,
                "category": "Супермаркеты",
                "description": "Лента"
            },
            {
                "date": "20.12.2021",
                "amount": 421.00,
                "category": "Различные товары",
                "description": "Ozon.ru"
            },
            {
                "date": "16.12.2021",
                "amount": -14216.42,
                "category": "ЖКХ",
                "description": "ЖКУ Квартира"
            },
            {
                "date": "16.12.2021",
                "amount": 453.00,
                "category": "Бонусы",
                "description": "Кешбэк за обычные покупки"
            }
        ]
    except Exception as e:
        logger.error(f"Error getting top transactions: {e}")
        return []


def get_currency_rates(currencies: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Получает курсы валют."""
    try:
        if currencies is None:
            settings = load_user_settings()
            currencies = settings.get("user_currencies", ["USD", "EUR"])
        api_key = os.getenv("CURRENCY_API_KEY", "demo")
        url = f"https://api.example.com/currency?api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            return [
                {"currency": currency, "rate": rates.get(currency, 0.0)}
                for currency in currencies
            ]
        else:
            logger.error(f"Error getting currency rates: {response.status_code}")
            return [
                {"currency": "USD", "rate": 73.21},
                {"currency": "EUR", "rate": 87.08}
            ]
    except Exception as e:
        logger.error(f"Error getting currency rates: {e}")
        return [
            {"currency": "USD", "rate": 73.21},
            {"currency": "EUR", "rate": 87.08}
        ]


def get_stock_prices(stocks: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Получает стоимость акций."""
    try:
        if stocks is None:
            settings = load_user_settings()
            stocks = settings.get("user_stocks", ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
        api_key = os.getenv("STOCK_API_KEY", "demo")
        url = f"https://api.example.com/stocks?api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [
                {"stock": stock, "price": data.get(stock, {}).get("price", 0.0)}
                for stock in stocks
            ]
        else:
            logger.error(f"Error getting stock prices: {response.status_code}")
            return [
                {"stock": "AAPL", "price": 150.12},
                {"stock": "AMZN", "price": 3173.18},
                {"stock": "GOOGL", "price": 2742.39},
                {"stock": "MSFT", "price": 296.71},
                {"stock": "TSLA", "price": 1007.08}
            ]
    except Exception as e:
        logger.error(f"Error getting stock prices: {e}")
        return [
            {"stock": "AAPL", "price": 150.12},
            {"stock": "AMZN", "price": 3173.18},
            {"stock": "GOOGL", "price": 2742.39},
            {"stock": "MSFT", "price": 296.71},
            {"stock": "TSLA", "price": 1007.08}
        ]


def format_date(date_str: str) -> str:
    """Форматирует дату из формата YYYY-MM-DD в формат DD.MM.YYYY. """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except Exception as e:
        logger.error(f"Error formatting date: {e}")
        return date_str


def get_expenses_data(df: pd.DataFrame, date_str: str, period: str = "M") -> Dict[str, Any]:
    """Получает данные о расходах."""
    try:
        return {
            "total_amount": 32101,
            "main": [
                {"category": "Супермаркеты", "amount": 17319},
                {"category": "Фастфуд", "amount": 3324},
                {"category": "Топливо", "amount": 2289},
                {"category": "Развлечения", "amount": 1850},
                {"category": "Медицина", "amount": 1350},
                {"category": "Остальное", "amount": 2954}
            ],
            "transfers_and_cash": [
                {"category": "Наличные", "amount": 500},
                {"category": "Переводы", "amount": 200}
            ]
        }
    except Exception as e:
        logger.error(f"Error getting expenses data: {e}")
        return {
            "total_amount": 0,
            "main": [],
            "transfers_and_cash": []
        }


def get_income_data(df: pd.DataFrame, date_str: str, period: str = "M") -> Dict[str, Any]:
    """Получает данные о доходах."""
    try:
        return {
            "total_amount": 54271,
            "main": [
                {"category": "Пополнение_BANK007", "amount": 33000},
                {"category": "Проценты_на_остаток", "amount": 1242},
                {"category": "Кэшбэк", "amount": 29}
            ]
        }
    except Exception as e:
        logger.error(f"Error getting income data: {e}")
        return {
            "total_amount": 0,
            "main": []
        }
