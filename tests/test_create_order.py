"""Тесты ручки «Создать заказ»."""

import allure
import pytest

from data.generators import COLOR_BLACK, COLOR_BOTH, COLOR_GREY, generate_order_payload


@allure.epic("Яндекс Самокат API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    """Набор тестов создания заказа с проверкой вариантов цвета."""

    @allure.title("Заказ создаётся с любым вариантом цвета, ответ 201 и track")
    @pytest.mark.parametrize(
        "color",
        [None, [COLOR_BLACK], [COLOR_GREY], COLOR_BOTH],
        ids=["no_color", "black", "grey", "both_colors"],
    )
    def test_create_order_when_color_variant_passed_returns_201_and_track(
            self, order_service, color
    ):
        """При любом варианте color заказ создаётся и возвращает track."""

        payload = generate_order_payload(color=color)

        response = order_service.create_order(payload)

        assert response.status_code == 201
        assert "track" in response.json()
