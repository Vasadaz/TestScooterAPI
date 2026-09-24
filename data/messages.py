"""Ожидаемые сообщения об ошибках (взято дословно из документации Ez-scooter)."""

class CourierMessages:
    """Сообщения ручек создания/логина/удаления курьера."""

    CREATE_MISSING_FIELDS = "Недостаточно данных для создания учетной записи"
    LOGIN_ALREADY_USED = "Этот логин уже используется"
    LOGIN_MISSING_FIELDS = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
    DELETE_MISSING_ID = "Недостаточно данных для удаления курьера"
    DELETE_NOT_FOUND = "Курьера с таким id нет"


class OrderMessages:
    """Сообщения ручек списка/приёма/поиска заказа."""

    COURIER_NOT_FOUND_TEMPLATE = "Курьер с идентификатором {courier_id} не найден"
    ORDER_NOT_FOUND = "Заказ не найден"
    ORDER_ID_NOT_FOUND = "Заказа с таким id не существует"
    COURIER_ID_NOT_FOUND = "Курьера с таким id не существует"
    NOT_ENOUGH_SEARCH_DATA = "Недостаточно данных для поиска"
    ORDER_ALREADY_IN_PROGRESS = "Этот заказ уже в работе"
