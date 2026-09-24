"""Генераторы случайных тестовых данных на базе Faker.

Faker.seed() фиксируется для воспроизводимости прогона.
"""

from datetime import date, timedelta

from faker import Faker

# Фиксируем seed -> данные воспроизводимы между запусками.
Faker.seed(42)
fake = Faker("ru_RU")

COLOR_BLACK = "BLACK"
COLOR_GREY = "GREY"
COLOR_BOTH = [COLOR_BLACK, COLOR_GREY]


def generate_courier_credentials() -> dict:
    """Возвращает уникальные login / password / firstName для курьера.

    Логин уникален за счёт суффикса из Faker.uuid4(), чтобы
    избежать коллизий между тестами и повторными прогонами.
    """
    unique_suffix = fake.uuid4()[:8]
    return {
        "login": f"courier_{unique_suffix}",
        "password": fake.password(length=12),
        "firstName": fake.first_name(),
    }


def generate_order_payload(address: str = "Москва", color: list[str] | None = None) -> dict:
    """Формирует тело запроса на создание заказа.

    :param address: Строка с названием города, по умолчанию "Москва"
    :param color: Список цветов, например ["BLACK"], ["GREY"],
        ["BLACK", "GREY"] либо None, чтобы не передавать поле color вовсе
    """
    payload = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": address,
        "metroStation": str(fake.random_int(min=1, max=20)),
        "phone": generate_phone(),
        "rentTime": fake.random_int(min=1, max=7),
        "deliveryDate": generate_delivery_date(days_from_today=3),
        "comment": fake.text(max_nb_chars=40),
    }
    if color:
        payload["color"] = color
    return payload


def generate_phone() -> str:
    """Возвращает валидный телефон в формате +7XXXXXXXXXX (11 цифр)."""
    ten_digits = f"{fake.random_int(min=0, max=999999999):09d}"
    return f"+7{ten_digits}"


def generate_delivery_date(days_from_today: int) -> str:
    """Возвращает дату доставки в формате YYYY-MM-DD (сегодня + N дней)."""
    return (date.today() + timedelta(days=days_from_today)).isoformat()
