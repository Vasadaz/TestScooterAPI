"""Тесты ручки «Создать курьера»."""

import allure
import pytest

from data import messages
from data.generators import generate_courier_credentials


@allure.epic("Яндекс Самокат API")
@allure.feature("Создание курьера")
class TestCreateCourier:
    """Набор тестов ручки создания курьера."""

    @allure.title("Курьера можно создать, ответ 201 и тело ok=true")
    def test_create_courier_when_valid_data_returns_201_and_ok_true(
            self, courier_service, cleanup_couriers
    ):
        """Успешное создание курьера возвращает 201 и тело {'ok': True}."""
        payload = generate_courier_credentials()
        cleanup_couriers.append(payload)

        response = courier_service.create_courier(payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров, ответ 409")
    def test_create_courier_when_login_already_used_returns_409(
            self, courier_service, cleanup_couriers
    ):
        """Повторная регистрация с тем же логином возвращает 409 и сообщение."""
        payload = generate_courier_credentials()
        cleanup_couriers.append(payload)
        courier_service.create_courier(payload)

        response = courier_service.create_courier(payload)

        assert response.status_code == 409
        assert response.json()["message"] == messages.CourierMessages.LOGIN_ALREADY_USED

    @allure.title("Без обязательного поля запрос возвращает 400")
    @pytest.mark.parametrize(
        "missing_field",
        ["login", "password", "firstName"],
        ids=["no_login", "no_password", "no_firstname"],
    )
    def test_create_courier_when_required_field_missing_returns_400(
            self, courier_service, missing_field
    ):
        """Отсутствие обязательного поля даёт 400 и сообщение об ошибке."""
        payload = generate_courier_credentials()
        payload.pop(missing_field)

        response = courier_service.create_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == (
            messages.CourierMessages.CREATE_MISSING_FIELDS
        )
