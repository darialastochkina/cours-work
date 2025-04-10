"""Модуль для генерации отчетов по транзакциям."""

import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями.
        category: Название категории.
        date: Дата, от которой отсчитываются три месяца. Если None, используется текущая дата.

    Returns:
        DataFrame с тратами по категории.
    """
    logger.info(f"Generating spending by category report for {category}")
    try:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        end_date = datetime.strptime(date, "%Y-%m-%d")
        start_date = end_date - timedelta(days=90)
        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
        filtered_df = transactions[
            (transactions['Дата операции'] >= start_date) &
            (transactions['Дата операции'] <= end_date) &
            (transactions['Категория'] == category)
        ]
        result = filtered_df.groupby(pd.Grouper(key='Дата операции', freq='D'))[['Сумма платежа']].sum().reset_index()
        result = result.rename(columns={'Дата операции': 'date', 'Сумма платежа': 'amount'})
        logger.info(f"Spending by category report generated for {category}")
        return result
    except Exception as e:
        logger.error(f"Error generating spending by category report: {e}")
        return pd.DataFrame(columns=['date', 'amount'])
