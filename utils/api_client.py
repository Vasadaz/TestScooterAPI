"""Тонкая обёртка над requests.Session с логированием и Allure-аттачами."""

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ApiClient:
    """Обёртка над requests.Session: базовый URL, единый timeout, retry, Allure-аттачи."""

    DEFAULT_TIMEOUT: int = 30

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Настраивает сессию с базовым URL, таймаутом и авто-ретраями.

        :param base_url: Базовый URL стенда
        :param timeout: Таймаут на один запрос (сек)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        # Ретраи только на «сетевые» сбои и коды 5xx — не на бизнес-логику.
        retry = Retry(
            total=3,
            backoff_factor=1.0,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=frozenset(
                ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
            ),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)

    def request(self, method: str, path: str, **kwargs):
        """Единая точка отправки запроса с таймаутом и Allure-аттачами.

        :param method: HTTP-метод
        :param path: относительный путь (добавится к base_url)
        :param kwargs: json / params / data и т.п.
        :return: requests.Response
        """
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)

        with allure.step(f"{method.upper()} {url}"):
            if "json" in kwargs:
                allure.attach(
                    str(kwargs["json"]),
                    name="request body",
                    attachment_type=allure.attachment_type.JSON,
                )
            response = self.session.request(method, url, **kwargs)
            allure.attach(
                response.text,
                name=f"response {response.status_code}",
                attachment_type=allure.attachment_type.JSON,
            )
            return response

    def get(self, path: str, **kwargs):
        """GET-запрос. :return: requests.Response"""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        """POST-запрос. :return: requests.Response"""
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        """PUT-запрос. :return: requests.Response"""
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        """DELETE-запрос. :return: requests.Response"""
        return self.request("DELETE", path, **kwargs)
