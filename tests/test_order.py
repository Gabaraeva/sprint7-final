import pytest
import allure
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


@allure.feature("Создание заказа")
class TestOrderCreation:
    ORDER_PAYLOAD = {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "Москва",
        "metroStation": 4,
        "phone": "+79991112233",
        "rentTime": 5,
        "deliveryDate": "2024-12-31",
        "comment": "Тестовый заказ"
    }

    @allure.title("Создание заказа с цветом: {color}")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        payload = self.ORDER_PAYLOAD.copy()
        if color:
            payload["color"] = color

        response = requests.post(
            f"{BASE_URL}/orders",
            json=payload
        )

        assert response.status_code == 201
        assert "track" in response.json()