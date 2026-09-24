"""Сервисный слой ручек заказов (аналог Page Object для HTTP API)."""

from data import urls
from data.generators import generate_order_payload
from utils.api_client import ApiClient


class OrderService:
    """Инкапсулирует запросы к /api/v1/orders."""

    def __init__(self, client: ApiClient) -> None:
        """Принимает HTTP-клиент с настроенным base_url.

        :param client: Экземпляр ApiClient
        """
        self.client = client

    def create_order(self, payload: dict):
        """POST /api/v1/orders — создание заказа.

        :param payload: Тело запроса на заказ
        :return: requests.Response
        """
        return self.client.post(urls.ORDERS_CREATE_PATH, json=payload)

    def create_test_order(self, color: list[str] | None = None, address: str = "Москва") -> int:
        """Создаёт заказ с рандомными данными и возвращает его track.

        :param color: Список цветов заказа либо None
        :param address: адрес заказа
        :return: track созданного заказа
        """
        payload = generate_order_payload(address=address, color=color)
        response = self.create_order(payload)
        return response.json()["track"]

    def get_orders(self, params: dict | None = None):
        """GET /api/v1/orders — список заказов.

        :param params: query-параметры (courierId, nearestStation, limit, page)
        :return: requests.Response
        """
        return self.client.get(urls.ORDERS_LIST_PATH, params=params)

    def get_order_by_track(self, track: int | str):
        """GET /api/v1/orders/track?t= — заказ по трек-номеру.

        :param track: трекинговый номер заказа
        :return: requests.Response
        """
        return self.client.get(urls.ORDERS_TRACK_PATH, params={"t": track})

    def accept_order(self, order_id: int | str, courier_id: int | str | None = None):
        """PUT /api/v1/orders/accept/{id}?courierId= — принять заказ.

        Внимание: по факту id заказа — в пути, courierId — в query-параметрах
        (в доке для других ручек указание в теле некорректно).

        :param order_id: id заказа
        :param courier_id: id курьера, если None — параметр не передаётся
        :return: requests.Response
        """
        path = urls.ORDERS_ACCEPT_PATH.format(order_id=order_id)
        params = {}
        if courier_id is not None:
            params["courierId"] = courier_id
        return self.client.put(path, params=params)

    def cancel_order(self, track: int | str):
        """PUT /api/v1/orders/cancel?track= — отмена заказа.

        Дока ошибочно показывает track в теле — фактически нужен query-параметр.

        :param track: Трекинговый номер заказа
        :return: requests.Response
        """
        return self.client.put(urls.ORDERS_CANCEL_PATH, params={"track": track})

    def finish_order(self, order_id: int | str):
        """PUT /api/v1/orders/finish/{id} — завершить заказ.

        Доступно только для заказов в статусе «в работе».

        :param order_id: id заказа
        :return: requests.Response
        """
        path = urls.ORDERS_FINISH_PATH.format(order_id=order_id)
        return self.client.put(path)
