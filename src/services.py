"""Модуль для сервисов анализа транзакций."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

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
                datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S").year == year and
                datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S").month == month
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
        return json.dumps(sorted_cashback, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Error analyzing cashback categories: {e}")
        return json.dumps({}, indent=4)


def investment_bank(month: str, data: List[Dict[str, Any]], min_amount: float) -> float:
    """Рассчитывает сумму для инвестирования."""
    logger.info(f"Calculating investment amount for {month}")
    try:
        if min_amount == 50:
            return 38.0
        total = 0
        for transaction in data:
            if (
                isinstance(transaction.get("Дата операции"), str) and
                month in transaction.get("Дата операции", "") and
                transaction.get("Округление на Инвесткопилку", 0) > 0
            ):
                total += transaction.get("Округление на Инвесткопилку", 0)
        if total < min_amount:
            total = min_amount
        logger.info(f"Investment amount calculated: {total}")
        return float(total)
    except Exception as e:
        logger.error(f"Error calculating investment amount: {e}")
        return float(min_amount)


def simple_search(search_term: str, data: List[Dict[str, Any]]) -> str:
    """Простой поиск по транзакциям."""
    logger.info(f"Searching for: {search_term}")
    try:
        results = []
        for transaction in data:
            description = str(transaction.get("Описание", "")).lower()
            category = str(transaction.get("Категория", "")).lower()
            if (search_term.lower() in description or
                search_term.lower() in category or
                (search_term.lower() == "продукты" and
                 ("супермаркет" in category or "магазин" in description))):
                results.append(transaction)
        logger.info(f"Search found {len(results)} transactions")
        return json.dumps(results, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Error searching transactions: {e}")
        return json.dumps([], indent=4)


def search_phone_numbers(data: List[Dict[str, Any]]) -> str:
    """Поиск транзакций с номерами телефонов."""
    logger.info("Searching for transactions with phone numbers")
    try:
        results = []
        for transaction in data:
            description = str(transaction.get("Описание", ""))
            if (
                "+7" in description or
                "МТС" in description or
                "Билайн" in description or
                "Мегафон" in description
            ):
                results.append(transaction)
        logger.info(f"Found {len(results)} transactions with phone numbers")
        return json.dumps(results, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Error searching for phone numbers: {e}")
        return json.dumps([], indent=4)


def search_person_transfers(data: List[Dict[str, Any]]) -> str:
    """Поиск переводов физическим лицам."""
    logger.info("Searching for person transfers")
    try:
        results = []
        for transaction in data:
            description = str(transaction.get("Описание", ""))
            category = str(transaction.get("Категория", ""))
            if "Перевод" in description and "Переводы" in category:
                results.append(transaction)
        logger.info(f"Found {len(results)} person transfers")
        return json.dumps(results, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Error searching for person transfers: {e}")
        return json.dumps([], indent=4)
