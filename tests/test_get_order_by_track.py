"""Тесты ручки «Получить заказ по его номеру»."""

import allure

from data import messages
from data.urls import ORDERS_TRACK_PATH



@allure.epic("Яндекс Самокат API")
@allure.feature("Получить заказ по номеру")
class TestGetOrderByTrack:
    """Набор тестов поиска заказа по трек-номеру."""

    @allure.title("Успешный запрос возвращает объект с заказом")
    def test_get_order_by_track_when_valid_track_returns_200_and_order(
            self, order_service
    ):
        """Существующий track возвращает 200 и объект order."""
        track = order_service.create_test_order()

        response = order_service.get_order_by_track(track)

        assert response.status_code == 200
        assert "order" in response.json()

    @allure.title("Запрос без номера заказа возвращает ошибку")
    def test_get_order_by_track_when_track_missing_returns_400(self, order_service):
        """Отсутствие параметра t возвращает 400 и сообщение об ошибке."""
        response = order_service.client.get(ORDERS_TRACK_PATH)

        assert response.status_code == 400
        assert response.json()["message"] == messages.OrderMessages.NOT_ENOUGH_SEARCH_DATA

    @allure.title("Несуществующий заказ возвращает 404")
    def test_get_order_by_track_when_track_not_exists_returns_404(self, order_service):
        """Несуществующий track возвращает 404 и сообщение об ошибке."""
        response = order_service.get_order_by_track(0)

        assert response.status_code == 404
        assert response.json()["message"] == messages.OrderMessages.ORDER_NOT_FOUND
