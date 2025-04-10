"""Главный модуль приложения для анализа транзакций."""

import argparse
import logging

from src.utils import load_transactions
from src.views import main_page
from src.services import cashback_categories
from src.reports import spending_by_category

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description='Анализ транзакций')
    parser.add_argument('--file', type=str, default='data/Operations (1).xlsx',
                        help='Путь к файлу с транзакциями')
    subparsers = parser.add_subparsers(dest='command', help='Команда для выполнения')
    main_parser = subparsers.add_parser('main', help='Генерация данных для главной страницы')
    main_parser.add_argument('--datetime', type=str, required=True,
                             help='Дата и время в формате YYYY-MM-DD HH:MM:SS')
    cashback_parser = subparsers.add_parser('cashback', help='Анализ выгодных категорий кешбэка')
    cashback_parser.add_argument('--year', type=int, required=True,
                                 help='Год для анализа')
    cashback_parser.add_argument('--month', type=int, required=True,
                                 help='Месяц для анализа')
    category_parser = subparsers.add_parser('category', help='Отчет по тратам по категории')
    category_parser.add_argument('--category', type=str, required=True,
                                 help='Название категории')
    category_parser.add_argument('--date', type=str, default=None,
                                 help='Дата в формате YYYY-MM-DD')
    return parser.parse_args()


def main():
    """Основная функция приложения."""
    args = parse_args()
    if args.command:
        transactions_df = load_transactions(args.file)
        transactions_list = transactions_df.to_dict('records')
        if args.command == 'main':
            result = main_page(args.datetime)
            print(result)
        elif args.command == 'cashback':
            result = cashback_categories(transactions_list, args.year, args.month)
            print(result)
        elif args.command == 'category':
            result = spending_by_category(transactions_df, args.category, args.date)
            print(result.to_json(orient='records', date_format='iso'))
    else:
        print("Укажите команду для выполнения. Используйте --help для получения справки.")


if __name__ == "__main__":
    main()
