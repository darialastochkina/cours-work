import unittest
import pandas as pd

from src.reports import spending_by_category


class TestReports(unittest.TestCase):
    def test_spending_by_category(self):
        """Тест функции spending_by_category."""
        data = {
            'Дата операции': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-02-01'],
            'Сумма платежа': [100.0, 200.0, 300.0, 400.0],
            'Категория': ['Супермаркеты', 'Супермаркеты', 'Рестораны', 'Супермаркеты']
        }
        df = pd.DataFrame(data)
        result = spending_by_category(df, 'Супермаркеты', '2023-03-01')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)
        self.assertIn('date', result.columns)
        self.assertIn('amount', result.columns)
        total_amount = result['amount'].sum()
        self.assertEqual(total_amount, 700.0)


if __name__ == '__main__':
    unittest.main()
