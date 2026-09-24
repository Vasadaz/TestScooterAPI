"""Общие фикстуры проекта автотестов Яндекс Самокат."""

from collections.abc import Generator
from typing import Any

import allure
import pytest

from data.generators import generate_courier_credentials
from data.urls import BASE_URL
from services.courier_service import CourierService
from services.order_service import OrderService
from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    """Сессионный HTTP-клиент с общим base_url."""
    return ApiClient(base_url=BASE_URL)


@pytest.fixture
def courier_service(api_client: ApiClient) -> CourierService:
    """Сервис курьеров, привязанный к api_client."""
    return CourierService(api_client)


@pytest.fixture
def order_service(api_client: ApiClient) -> OrderService:
    """Сервис заказов, привязанный к api_client."""
    return OrderService(api_client)


@pytest.fixture
def registered_courier(courier_service: CourierService) -> Generator[dict, Any, None]:
    """Только регистрирует курьера (без логина) и удаляет после теста."""
    payload = generate_courier_credentials()
    courier_service.create_courier(payload)

    yield payload

    with allure.step("Cleanup: удалить созданного курьера"):
        login_response = courier_service.login_courier(
            payload["login"], payload["password"]
        )
        if login_response.status_code == 200:
            courier_service.delete_courier(login_response.json()["id"])


@pytest.fixture
def created_courier(courier_service: CourierService) -> Generator[dict, Any, None]:
    """Создаёт и авторизует курьера до теста, удаляет после (cleanup)."""
    courier_data = courier_service.register_and_login_courier()

    yield courier_data

    with allure.step("Cleanup: удалить созданного курьера"):
        courier_service.delete_courier(courier_data["id"])


@pytest.fixture
def created_order(order_service: OrderService) -> Generator[dict, Any, None]:
    """Создаёт заказ до теста и корректно закрывает его после (cleanup).

    Если заказ уже принят курьером (есть courierId) — завершаем через
    finish, иначе отменяем через cancel. Пустой ответ order трактуется
    как ошибка подготовки с понятным сообщением.

    :return: dict с order_id и track созданного заказа
    """
    track = order_service.create_test_order()

    track_response = order_service.get_order_by_track(track)
    assert track_response.status_code == 200, (
        f"Не удалось получить созданный заказ по track={track}: "
        f"{track_response.status_code} {track_response.text}"
    )
    order_body = track_response.json()
    assert "order" in order_body, (
        f"В ответе /orders/track нет ключа 'order': {order_body}"
    )
    order_id = order_body["order"]["id"]

    yield {"order_id": order_id, "track": track}

    with allure.step("Cleanup: закрыть тестовый заказ"):
        current = order_service.get_order_by_track(track).json().get("order", {})
        if current.get("courierId"):
            order_service.finish_order(order_id)
        else:
            order_service.cancel_order(track)


@pytest.fixture
def accepted_order(
        order_service: OrderService,
        courier_service: CourierService,
) -> Generator[dict, Any, None]:
    """Создаёт заказ, принимает его курьером и завершает после теста.

    :return: dict с order_id, track, courier_id
    """
    courier = courier_service.register_and_login_courier()
    track = order_service.create_test_order()
    order_id = order_service.get_order_by_track(track).json()["order"]["id"]
    order_service.accept_order(order_id, courier["id"])

    yield {"order_id": order_id, "track": track, "courier_id": courier["id"]}

    with allure.step("Cleanup: завершить заказ и удалить курьера"):
        order_service.finish_order(order_id)
        courier_service.delete_courier(courier["id"])


@pytest.fixture
def cleanup_couriers(courier_service: CourierService) -> Generator[list, Any, None]:
    """Гарантированно удаляет всех курьеров, логины которых тест добавит в список.

    Пример:
        cleanup_couriers.append(payload)
    """
    created: list[dict] = []

    yield created

    with allure.step("Cleanup: удалить курьеров, созданных в тесте"):
        for payload in created:
            login_response = courier_service.login_courier(
                payload["login"], payload["password"]
            )
            if login_response.status_code == 200:
                courier_service.delete_courier(login_response.json()["id"])
