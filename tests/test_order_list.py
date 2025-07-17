import allure
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


@allure.feature("Список заказов")
class TestOrderList:
    @allure.title("Получение списка заказов")
    def test_get_order_list(self):
        response = requests.get(
            f"{BASE_URL}/orders",
            params={"limit": 30}
        )

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
        assert len(response.json()["orders"]) > 0