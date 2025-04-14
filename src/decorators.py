"""Модуль с декораторами для проекта."""

import functools
import logging
import time
from typing import Any, Callable

logger = logging.getLogger(__name__)


def log_execution(func: Callable) -> Callable:
    """
    Декоратор для логирования выполнения функции.
    Записывает время начала, окончания и длительность выполнения.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        logger.info(f"Starting execution of {func.__name__}")
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Function {func.__name__} executed successfully in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Error in {func.__name__}: {e}, execution time: {execution_time:.4f} seconds")
            raise
    return wrapper
