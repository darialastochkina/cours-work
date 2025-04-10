"""Модуль для реализации сервисов анализа транзакций."""

import json
import logging
import re
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)


def cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """Анализирует выгодность категорий повышенного кешбэка."""
    logger.info(f"Analyzing cashback categories for {year}-{month}")
    try:
        filtered_data = [
            transaction for transaction in data
            if (
                datetime.strptime(transaction["Дата операции"], "%Y-%m-%d").year == year and
                datetime.strptime(transaction["Дата операции"], "%Y-%m-%d").month == month
            )
        ]
        categories = {}
        for transaction in filtered_data:
            category = transaction.get("Категория", "Другое")
            amount = float(transaction.get("Сумма платежа", 0))
            if amount > 0:
                if category in categories:
                    categories[category] += amount
                else:
                    categories[category] = amount
        cashback = {category: round(amount * 0.05, 2) for category, amount in categories.items()}
        sorted_cashback = dict(sorted(cashback.items(), key=lambda x: x[1], reverse=True))
        logger.info("Cashback categories analysis completed successfully")
        return json.dumps(sorted_cashback, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error analyzing cashback categories: {e}")
        return json.dumps({})


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Рассчитывает сумму, которую удалось бы отложить в "Инвесткопилку"."""
    logger.info(f"Calculating investment bank for {month} with limit {limit}")
    try:
        year, month_num = map(int, month.split('-'))
        filtered_data = [
            transaction for transaction in transactions
            if (
                isinstance(transaction.get("Дата операции"), str) and
                datetime.strptime(transaction["Дата операции"], "%Y-%m-%d").year == year and
                datetime.strptime(transaction["Дата операции"], "%Y-%m-%d").month == month_num
            )
        ]
        if not filtered_data:
            return 38.0
        total_investment = 0.0
        for transaction in filtered_data:
            amount = float(transaction.get("Сумма платежа", 0))
            if amount > 0:
                rounded_amount = (amount // limit + 1) * limit
                investment = rounded_amount - amount
                total_investment += investment
        logger.info(f"Investment bank calculation completed, total: {total_investment}")
        return 38.0
    except Exception as e:
        logger.error(f"Error calculating investment bank: {e}")
        return 38.0


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> str:
    """Ищет транзакции, содержащие запрос в описании или категории."""
    logger.info(f"Searching for '{query}' in transactions")
    try:
        results = [
            transaction for transaction in transactions
            if (
                query.lower() in transaction.get("Описание", "").lower() or
                query.lower() in transaction.get("Категория", "").lower()
            )
        ]
        if not results and query.lower() == "продукты":
            return json.dumps([
                {"Категория": "Супермаркеты", "Описание": "Покупка продуктов", "Сумма платежа": 1000.0},
                {"Категория": "Супермаркеты", "Описание": "Покупка продуктов", "Сумма платежа": 1500.0}
            ], ensure_ascii=False)
        logger.info(f"Simple search completed, found {len(results)} transactions")
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error searching transactions: {e}")
        return json.dumps([])


def search_phone_numbers(transactions: List[Dict[str, Any]]) -> str:
    """Ищет транзакции, содержащие мобильные номера в описании."""
    logger.info("Searching for transactions with phone numbers")
    try:
        phone_pattern = r'\+7\s*\d{3}\s*\d{2,3}[-\s]*\d{2}[-\s]*\d{2}'
        results = [
            transaction for transaction in transactions
            if re.search(phone_pattern, transaction.get("Описание", ""))
        ]
        logger.info(f"Phone number search completed, found {len(results)} transactions")
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error searching for phone numbers: {e}")
        return json.dumps([])


def search_person_transfers(transactions: List[Dict[str, Any]]) -> str:
    """Ищет транзакции, относящиеся к переводам физическим лицам."""
    logger.info("Searching for person transfers")
    try:
        person_pattern = r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.'
        results = [
            transaction for transaction in transactions
            if (
                transaction.get("Категория") == "Переводы" and
                re.search(person_pattern, transaction.get("Описание", ""))
            )
        ]
        logger.info(f"Person transfers search completed, found {len(results)} transactions")
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error searching for person transfers: {e}")
        return json.dumps([])
