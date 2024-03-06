from datetime import datetime
import re


def validate_name(name):
    """Функция для проверки длины имени."""
    return len(name) > 1


def validate_phone_number(phone_number):
    """Функция для проверки формата номера телефона."""
    pattern = re.compile(r"^\+7 \d{3}-\d{3}-\d{2}-\d{2}$")
    return pattern.match(phone_number) is not None


def validate_quantity(value):
    """Функция для проверки колличества мяса в заказе."""
    try:
        quantity = int(value)
        return 1 <= quantity <= 200
    except Exception:
        return False


def validate_delivery_date(date_str):
    """Функция для проверки формата даты доставки."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        delivery_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        return delivery_date > today
    except ValueError:
        return False
