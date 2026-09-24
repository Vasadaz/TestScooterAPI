"""Тесты ручки «Список заказов»"""

import allure

@allure.epic("Яндекс Самокат API")
@allure.feature("Список заказов")
class TestGetOrdersList:
    """Набор тестов получения списка заказов."""

    @allure.title("Ответ содержит список заказов, ответ 200")
    def test_get_orders_when_called_returns_200_and_orders_list(
            self, order_service
    ):
        """Успешный запрос возвращает 200 и непустой список orders."""
        response = order_service.get_orders()

        assert response.status_code == 200
        body = response.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)
        assert "pageInfo" in body
