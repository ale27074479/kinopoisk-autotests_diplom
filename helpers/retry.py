import time
from functools import wraps


def retry(max_attempts=3, delay=1):
    """
    Декоратор для повторного выполнения функции при возникновении исключений.
    
    :param max_attempts: Максимальное количество попыток
    :param delay: Задержка между попытками в секундах
    :return: Результат выполнения функции или последнее исключение
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:  # Не ждем после последней попытки
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
