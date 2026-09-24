"""Тесты ручки «Логин курьера»"""

import allure
import pytest

from data import messages
from data.generators import generate_courier_credentials
from data.urls import COURIER_LOGIN_PATH


@allure.epic("Яндекс Самокат API")
@allure.feature("Логин курьера")
class TestLoginCourier:
    """Набор тестов авторизации курьера."""

    @allure.title("Курьер может авторизоваться, ответ 200 и наличие id")
    def test_login_courier_when_valid_credentials_returns_200_and_id(
            self, courier_service, created_courier
    ):
        """Успешная авторизация возвращает 200 и поле id."""
        response = courier_service.login_courier(
            created_courier["login"], created_courier["password"]
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Без обязательного поля запрос возвращает 400")
    @pytest.mark.parametrize(
        "missing_field",
        ["login", "password"],
        ids=["no_login", "no_password"],
    )
    def test_login_courier_when_required_field_missing_returns_400(
            self, courier_service, created_courier, missing_field
    ):
        """Отсутствие login или password даёт 400 и сообщение об ошибке."""
        payload = {
            "login": created_courier["login"],
            "password": created_courier["password"],
        }
        payload.pop(missing_field)

        response = courier_service.client.post(COURIER_LOGIN_PATH, json=payload)

        assert response.status_code == 400
        assert response.json()["message"] == (
            messages.CourierMessages.LOGIN_MISSING_FIELDS
        )

    @allure.title("Неверный логин даёт 404")
    def test_login_courier_when_wrong_login_returns_404(
            self, courier_service, created_courier
    ):
        """Неверный логин возвращает 404 и сообщение об отсутствии учётки."""
        wrong = generate_courier_credentials()
        response = courier_service.login_courier(
            wrong["login"], created_courier["password"]
        )

        assert response.status_code == 404
        assert response.json()["message"] == messages.CourierMessages.ACCOUNT_NOT_FOUND

    @allure.title("Неверный пароль даёт 404")
    def test_login_courier_when_wrong_password_returns_404(
            self, courier_service, created_courier
    ):
        """Неверный пароль возвращает 404 и сообщение об отсутствии учётки."""
        response = courier_service.login_courier(
            created_courier["login"], "wrong_password_12345"
        )

        assert response.status_code == 404
        assert response.json()["message"] == messages.CourierMessages.ACCOUNT_NOT_FOUND

    @allure.title("Авторизация под несуществующим пользователем даёт 404")
    def test_login_courier_when_user_not_exists_returns_404(self, courier_service):
        """Логин и пароль несуществующего курьера дают 404."""
        response = courier_service.login_courier(
            "no_such_user_999", "no_such_password_999"
        )

        assert response.status_code == 404
        assert response.json()["message"] == messages.CourierMessages.ACCOUNT_NOT_FOUND
