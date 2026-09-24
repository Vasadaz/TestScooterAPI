"""Тесты ручки «Удалить курьера»."""

import allure

from data import messages
from data.urls import COURIER_CREATE_PATH


@allure.epic("Яндекс Самокат API")
@allure.feature("Удаление курьера")
class TestDeleteCourier:
    """Набор тестов удаления курьера."""

    @allure.title("Успешное удаление курьера возвращает 200 и {{'ok': True}}")
    def test_delete_courier_when_valid_id_returns_200_and_ok_true(
            self, courier_service
    ):
        """Удаление существующего курьера по id возвращает 200 и {'ok': True}."""
        courier = courier_service.register_and_login_courier()

        response = courier_service.delete_courier(courier["id"])

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Запрос без id возвращает ошибку")
    def test_delete_courier_when_id_missing_returns_error(self, courier_service):
        """Запрос DELETE на путь без id не создаёт корректный вызов — вернётся ошибка."""
        response = courier_service.client.delete(COURIER_CREATE_PATH)

        assert response.status_code in (400, 404)
        assert messages.CourierMessages.DELETE_MISSING_ID in response.text

    @allure.title("Удаление курьера с несуществующим id возвращает 404")
    def test_delete_courier_when_id_not_exists_returns_404(self, courier_service):
        """Несуществующий id курьера возвращает 404 и сообщение об ошибке."""
        response = courier_service.delete_courier(999999999)

        assert response.status_code == 404
        assert response.json()["message"] == messages.CourierMessages.DELETE_NOT_FOUND

    @allure.title("Повторное удаление того же курьера возвращает 404")
    def test_delete_courier_when_already_deleted_returns_404(self, courier_service):
        """Повторное удаление уже удалённого курьера возвращает 404 (неуспешный запрос)."""
        courier = courier_service.register_and_login_courier()
        courier_service.delete_courier(courier["id"])

        response = courier_service.delete_courier(courier["id"])

        assert response.status_code == 404
