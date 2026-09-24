"""Сервисный слой ручек курьера."""

from data import urls

from data.generators import generate_courier_credentials
from utils.api_client import ApiClient


class CourierService:
    """Инкапсулирует запросы к /api/v1/courier."""

    def __init__(self, client: ApiClient) -> None:
        """Принимает HTTP-клиент с настроенным base_url.

        :param client: экземпляр ApiClient
        """
        self.client = client

    def create_courier(self, payload: dict):
        """POST /api/v1/courier — создание курьера.

        :param payload: тело запроса (login/password/firstName)
        :return: requests.Response
        """
        return self.client.post(urls.COURIER_CREATE_PATH, json=payload)

    def register_courier(self) -> dict:
        """Создаёт нового уникального курьера и возвращает его данные.

        :return: dict с login/password/firstName
        """
        payload = generate_courier_credentials()
        self.create_courier(payload)
        return payload

    def login_courier(self, login: str, password: str):
        """POST /api/v1/courier/login — авторизация курьера.

        :param login: логин курьера
        :param password: пароль курьера
        :return: requests.Response
        """
        return self.client.post(
            urls.COURIER_LOGIN_PATH,
            json={"login": login, "password": password},
        )

    def register_and_login_courier(self) -> dict:
        """Создаёт курьера и сразу авторизуется, возвращая id.

        :return: dict с login/password/firstName/id
        """
        payload = self.register_courier()
        payload["id"] = self.login_courier(
            payload["login"], payload["password"]
        ).json()["id"]
        return payload

    def delete_courier(self, courier_id: int | str):
        """DELETE /api/v1/courier/{id} — удаление курьера по id.

        :param courier_id: id курьера
        :return: requests.Response
        """
        path = urls.COURIER_DELETE_PATH.format(courier_id=courier_id)
        return self.client.delete(path)
