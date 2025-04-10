import warnings
from urllib3.exceptions import NotOpenSSLWarning
import pytest
import pandas as pd

warnings.filterwarnings("ignore", category=Warning, module="urllib3")
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


@pytest.fixture(autouse=True)
def ignore_urllib3_warnings():
    warnings.filterwarnings("ignore", category=Warning, module="urllib3")


def pytest_configure(config):
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


@pytest.fixture
def real_transactions():
    """Фикстура с реальными данными транзакций из файла."""
    return pd.read_excel('data/Operations (1).xlsx')
