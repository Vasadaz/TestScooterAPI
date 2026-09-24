"""URL-константы ручек учебного сервиса Яндекс Самокат.

Все пути собраны в одном месте, чтобы при смене стенда править
только BASE_URL.
"""

BASE_URL = "https://qa-scooter.praktikum-services.ru"

# --- Courier ---
COURIER_CREATE_PATH = "/api/v1/courier"
COURIER_LOGIN_PATH = "/api/v1/courier/login"
COURIER_DELETE_PATH = "/api/v1/courier/{courier_id}"

# --- Orders ---
ORDERS_CREATE_PATH = "/api/v1/orders"
ORDERS_LIST_PATH = "/api/v1/orders"
ORDERS_TRACK_PATH = "/api/v1/orders/track"
ORDERS_ACCEPT_PATH = "/api/v1/orders/accept/{order_id}"
ORDERS_CANCEL_PATH = "/api/v1/orders/cancel"
ORDERS_FINISH_PATH = "/api/v1/orders/finish/{order_id}"
