from datetime import datetime
from typing import Optional, Union


def format_date(date_obj: Optional[datetime], fmt: str = "%Y-%m-%d") -> Optional[str]:
    """
    Форматирует объект datetime в строку согласно формату.
    Возвращает None, если date_obj is None.
    """
    if date_obj is None:
        return None
    return date_obj.strftime(fmt)


def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    Парсит строку в datetime согласно формату.
    Возвращает None при ошибке.
    """
    try:
        return datetime.strptime(date_str, fmt)
    except (ValueError, TypeError):
        return None


def is_positive_int(value: Union[int, float, str]) -> bool:
    """
    Проверяет, что значение можно интерпретировать как положительное целое число.
    """
    try:
        int_value = int(value)
        return int_value > 0
    except (ValueError, TypeError):
        return False


def safe_get(dct: dict, key: str, default=None):
    """
    Безопасно получает значение из словаря по ключу, возвращая default если ключа нет.
    """
    return dct.get(key, default)
