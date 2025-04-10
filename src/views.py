"""Модуль для генерации представлений данных."""

import json
import logging

from src.utils import (
    get_greeting, get_card_info, get_top_transactions,
    get_currency_rates, get_stock_prices
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)


def main_page(datetime_str: str) -> str:
    """Генерирует данные для главной страницы."""
    logger.info(f"Generating main page data for {datetime_str}")
    try:
        greeting = get_greeting(datetime_str)
        cards = get_card_info(datetime_str)
        transactions = get_top_transactions(datetime_str)
        currencies = get_currency_rates()
        stocks = get_stock_prices()
        result = {
            "greeting": greeting,
            "cards": cards,
            "transactions": transactions,
            "currencies": currencies,
            "stocks": stocks
        }
        logger.info("Main page data generated successfully")
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error generating main page data: {e}")
        return json.dumps({"error": str(e)})
