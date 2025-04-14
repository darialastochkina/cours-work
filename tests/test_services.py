import json
import unittest
from datetime import datetime

import pytest

from src.services import (
    cashback_categories,
    investment_bank,
    search_person_transfers,
    search_phone_numbers,
    simple_search,
)


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными транзакций."""
    return [
        {
            'Дата операции': '2023-01-01',
            'Дата платежа': '2023-01-01',
            'Номер карты': '1234',
            'Статус': 'OK',
            'Сумма операции': 100.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': 100.0,
            'Валюта платежа': 'RUB',
            'Кешбэк': 1.0,
            'Категория': 'Супермаркеты',
            'MCC': 5411,
            'Описание': 'Пятерочка',
            'Бонусы (включая кешбэк)': 1.0,
            'Округление на Инвесткопилку': 0.0,
            'Сумма операции с округлением': 100.0
        },
        {
            'Дата операции': '2023-01-02',
            'Дата платежа': '2023-01-02',
            'Номер карты': '5678',
            'Статус': 'OK',
            'Сумма операции': 200.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': 200.0,
            'Валюта платежа': 'RUB',
            'Кешбэк': 2.0,
            'Категория': 'Рестораны',
            'MCC': 5812,
            'Описание': 'Макдоналдс',
            'Бонусы (включая кешбэк)': 2.0,
            'Округление на Инвесткопилку': 0.0,
            'Сумма операции с округлением': 200.0
        },
        {
            'Дата операции': '2023-01-03',
            'Дата платежа': '2023-01-03',
            'Номер карты': '1234',
            'Статус': 'OK',
            'Сумма операции': 300.0,
            'Валюта операции': 'USD',
            'Сумма платежа': 22500.0,
            'Валюта платежа': 'RUB',
            'Кешбэк': 0.0,
            'Категория': 'Переводы',
            'MCC': 4829,
            'Описание': 'Перевод Иван И.',
            'Бонусы (включая кешбэк)': 0.0,
            'Округление на Инвесткопилку': 0.0,
            'Сумма операции с округлением': 300.0
        },
        {
            'Дата операции': '2023-01-15',
            'Дата платежа': '2023-01-15',
            'Номер карты': '9012',
            'Статус': 'OK',
            'Сумма операции': 150.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': 150.0,
            'Валюта платежа': 'RUB',
            'Кешбэк': 1.5,
            'Категория': 'Супермаркеты',
            'MCC': 5411,
            'Описание': 'Магнит',
            'Бонусы (включая кешбэк)': 1.5,
            'Округление на Инвесткопилку': 0.0,
            'Сумма операции с округлением': 150.0
        },
        {
            'Дата операции': '2023-01-20',
            'Дата платежа': '2023-01-20',
            'Номер карты': '5678',
            'Статус': 'OK',
            'Сумма операции': 250.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': 250.0,
            'Валюта платежа': 'RUB',
            'Кешбэк': 2.5,
            'Категория': 'Связь',
            'MCC': 4814,
            'Описание': 'МТС +7 921 11-22-33',
            'Бонусы (включая кешбэк)': 2.5,
            'Округление на Инвесткопилку': 0.0,
            'Сумма операции с округлением': 250.0
        },
        {
            'Дата операции': '2023-01-25',
            'Дата платежа': '2023-01-25',
            'Номер карты': '1234',
            'Статус': 'OK',
            'Сумма операции': 1712.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': 1712.0,
            'Валюта платежа': 'RUB',
            'Кешбэк': 17.12,
            'Категория': 'Одежда и обувь',
            'MCC': 5651,
            'Описание': 'Zara',
            'Бонусы (включая кешбэк)': 17.12,
            'Округление на Инвесткопилку': 0.0,
            'Сумма операции с округлением': 1712.0
        },
        {
            'Дата операции': '2023-01-30',
            'Дата платежа': '2023-01-30',
            'Номер карты': '9012',
            'Статус': 'OK',
            'Сумма операции': 500.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': 500.0,
            'Валюта платежа': 'RUB',
            'Кешбэк': 5.0,
            'Категория': 'Развлечения',
            'MCC': 7832,
            'Описание': 'Кинотеатр',
            'Бонусы (включая кешбэк)': 5.0,
            'Округление на Инвесткопилку': 0.0,
            'Сумма операции с округлением': 500.0
        },
        {
            'Дата операции': '2023-01-31',
            'Дата платежа': '2023-01-31',
            'Номер карты': '5678',
            'Статус': 'OK',
            'Сумма операции': 350.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': 350.0,
            'Валюта платежа': 'RUB',
            'Кешбэк': 3.5,
            'Категория': 'Переводы',
            'MCC': 4829,
            'Описание': 'Перевод Сергей З.',
            'Бонусы (включая кешбэк)': 3.5,
            'Округление на Инвесткопилку': 0.0,
            'Сумма операции с округлением': 350.0
        }
    ]


@pytest.mark.parametrize("search_term,expected_count,expected_item", [
    ("Пятерочка", 1, "Пятерочка"),
    ("продукты", 2, "Супермаркеты"),
    ("Макдоналдс", 1, "Макдоналдс"),
    ("несуществующий_запрос", 0, None),
])
def test_simple_search_parametrized(sample_transactions, search_term, expected_count, expected_item):
    """Параметризованный тест функции simple_search."""
    result = simple_search(search_term, sample_transactions)
    result_list = json.loads(result)
    assert len(result_list) == expected_count
    if expected_count > 0:
        if expected_item in ["Пятерочка", "Макдоналдс"]:
            assert result_list[0]["Описание"] == expected_item
        elif expected_item == "Супермаркеты":
            assert result_list[0]["Категория"] == expected_item


@pytest.mark.parametrize("year,month,expected_categories", [
    (2023, 1, ["Рестораны", "Супермаркеты", "Одежда и обувь"]),
    (2022, 12, []),
    (2023, 2, []),
])
def test_cashback_categories_parametrized(sample_transactions, year, month, expected_categories):
    """Параметризованный тест функции анализа выгодных категорий для кешбэка."""
    for transaction in sample_transactions:
        if "Дата операции" in transaction:
            date_str = transaction["Дата операции"]
            if "-" in date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                transaction["Дата операции"] = date_obj.strftime("%d.%m.%Y %H:%M:%S")
    result = cashback_categories(sample_transactions, year, month)
    result_dict = json.loads(result)
    if not expected_categories:
        assert result_dict == {}
    else:
        for category in expected_categories:
            assert category in result_dict
            assert result_dict[category] > 0


def test_investment_bank(sample_transactions):
    """Тест функции расчета суммы для инвесткопилки."""
    result = investment_bank("2023-01", sample_transactions, 50)
    assert isinstance(result, float)
    assert result > 0
    assert result == 38.0


def test_search_phone_numbers(sample_transactions):
    """Тест функции search_phone_numbers."""
    result = search_phone_numbers(sample_transactions)
    result_list = json.loads(result)
    assert len(result_list) > 0
    assert "МТС" in result_list[0]["Описание"]


def test_search_person_transfers(sample_transactions):
    """Тест функции search_person_transfers."""
    result = search_person_transfers(sample_transactions)
    result_list = json.loads(result)
    assert len(result_list) > 0
    assert "Перевод" in result_list[0]["Описание"]


class TestServices(unittest.TestCase):
    """Тесты для сервисов анализа транзакций."""

    def setUp(self):
        """Подготовка данных для тестов."""
        self.test_transactions = [
            {
                "Дата операции": "2023-01-15",
                "Категория": "Супермаркеты",
                "Сумма платежа": 1000.0,
                "Описание": "Покупка продуктов"
            },
            {
                "Дата операции": "2023-01-20",
                "Категория": "Рестораны",
                "Сумма платежа": 2000.0,
                "Описание": "Ужин в ресторане"
            },
            {
                "Дата операции": "2023-02-10",
                "Категория": "Супермаркеты",
                "Сумма платежа": 1500.0,
                "Описание": "Покупка продуктов"
            },
            {
                "Дата операции": "2023-01-25",
                "Категория": "Переводы",
                "Сумма платежа": 3000.0,
                "Описание": "Перевод Иван П."
            },
            {
                "Дата операции": "2023-01-30",
                "Категория": "Связь",
                "Сумма платежа": 500.0,
                "Описание": "МТС +7 921 123-45-67"
            }
        ]

    def test_cashback_categories(self):
        """Тест функции cashback_categories."""
        for transaction in self.test_transactions:
            if "Дата операции" in transaction:
                date_str = transaction["Дата операции"]
                if "-" in date_str:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    transaction["Дата операции"] = date_obj.strftime("%d.%m.%Y %H:%M:%S")
        result = cashback_categories(self.test_transactions, 2023, 1)
        result_dict = json.loads(result)
        self.assertIn("Рестораны", result_dict)
        self.assertIn("Супермаркеты", result_dict)
        self.assertIn("Переводы", result_dict)
        self.assertEqual(result_dict["Рестораны"], 100.0)
        self.assertEqual(result_dict["Супермаркеты"], 50.0)

    def test_investment_bank(self):
        """Тест функции investment_bank."""
        result = investment_bank("2023-01", self.test_transactions, 100)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_simple_search(self):
        """Тест функции simple_search."""
        result = simple_search("продукты", self.test_transactions)
        result_list = json.loads(result)
        self.assertEqual(len(result_list), 2)
        self.assertEqual(result_list[0]["Категория"], "Супермаркеты")

    def test_search_phone_numbers(self):
        """Тест функции search_phone_numbers."""
        result = search_phone_numbers(self.test_transactions)
        result_list = json.loads(result)
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0]["Категория"], "Связь")

    def test_search_person_transfers(self):
        """Тест функции search_person_transfers."""
        result = search_person_transfers(self.test_transactions)
        result_list = json.loads(result)
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0]["Категория"], "Переводы")
