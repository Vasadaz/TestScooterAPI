"""Тесты ручки «Принять заказ»."""

import allure

from data import messages
from data.urls import ORDERS_ACCEPT_PATH

@allure.epic("Яндекс Самокат API")
@allure.feature("Принять заказ")
class TestAcceptOrder:
    """Набор тестов принятия заказа курьером."""

    @allure.title("Успешный приём заказа возвращает 200 и тело {{'ok': True}}")
    def test_accept_order_when_valid_data_returns_200_and_ok_true(
            self, order_service, created_courier, created_order
    ):
        """Приём заказа существующим курьером возвращает 200 и {'ok': True}."""
        response = order_service.accept_order(
            created_order["order_id"], created_courier["id"]
        )

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Без id курьера запрос возвращает 400")
    def test_accept_order_when_courier_id_missing_returns_400(
            self, order_service, created_order
    ):
        """Отсутствие параметра courierId даёт 400 и сообщение об ошибке."""
        response = order_service.accept_order(
            created_order["order_id"], courier_id=None
        )

        assert response.status_code == 400
        assert response.json()["message"] == messages.OrderMessages.NOT_ENOUGH_SEARCH_DATA

    @allure.title("Неверный id курьера возвращает 404")
    def test_accept_order_when_courier_id_wrong_returns_404(
            self, order_service, created_order
    ):
        """Несуществующий courierId даёт 404 и сообщение об отсутствии курьера."""
        response = order_service.accept_order(
            created_order["order_id"], courier_id=999999999
        )

        assert response.status_code == 404
        assert response.json()["message"] == (
            messages.OrderMessages.COURIER_ID_NOT_FOUND
        )

    @allure.title("Без id заказа запрос возвращает ошибку")
    def test_accept_order_when_order_id_missing_returns_error(
            self, order_service, created_courier
    ):
        """Отсутствие id заказа в пути даёт ошибку (роут/параметр)."""
        response = order_service.client.put(
            f"{ORDERS_ACCEPT_PATH.format(order_id='')}",
            params={"courierId": created_courier["id"]},
        )

        assert response.status_code in (400, 404)

    @allure.title("Неверный id курьера возвращает 404")
    def test_accept_order_when_courier_id_wrong_returns_404(
            self, order_service, created_order
    ):
        """Несуществующий courierId даёт 404 и сообщение об отсутствии курьера."""
        response = order_service.accept_order(
            created_order["order_id"], courier_id=999999999
        )

        assert response.status_code == 404
        assert response.json()["message"] == (
            messages.OrderMessages.COURIER_ID_NOT_FOUND
        )
