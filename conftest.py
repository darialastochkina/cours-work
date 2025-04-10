import warnings
from urllib3.exceptions import NotOpenSSLWarning


def pytest_configure(config):
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
