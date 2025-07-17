import pytest
import allure
import requests
from helpers.courier import create_new_courier, login_courier, delete_courier

# Добавляем BASE_URL который используется в запросах
BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


@allure.feature("Создание курьера")
class TestCourierCreation:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        courier = create_new_courier()
        assert courier is not None
        courier_id = login_courier(courier["login"], courier["password"])
        assert courier_id is not None
        delete_courier(courier_id)

    @allure.title("Создание дубликата курьера")
    def test_create_duplicate_courier(self):
        courier = create_new_courier()
        response = requests.post(
            f"{BASE_URL}/courier",
            json={
                "login": courier["login"],
                "password": courier["password"],
                "firstName": courier["first_name"]
            }
        )
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]
        courier_id = login_courier(courier["login"], courier["password"])
        delete_courier(courier_id)

    @allure.title("Создание курьера без обязательных полей")
    @pytest.mark.parametrize("field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, field):
        payload = {
            "login": "test_login",
            "password": "test_pass",
            "firstName": "Имя"
        }
        payload.pop(field)

        response = requests.post(
            f"{BASE_URL}/courier",
            json=payload
        )
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]


# Класс должен быть НА УРОВНЕ других классов, а не внутри метода!
@allure.feature("Логин курьера")
class TestCourierLogin:
    @allure.title("Успешный логин курьера")
    def test_login_success(self):
        courier = create_new_courier()
        courier_id = login_courier(courier["login"], courier["password"])
        assert isinstance(courier_id, int)
        delete_courier(courier_id)

    @allure.title("Логин без обязательных полей")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_login_missing_field(self, field):
        courier = create_new_courier()
        payload = {"login": courier["login"], "password": courier["password"]}
        payload.pop(field)

        response = requests.post(
            f"{BASE_URL}/courier/login",
            json=payload
        )
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]
        courier_id = login_courier(courier["login"], courier["password"])
        delete_courier(courier_id)

    @allure.title("Логин с неверными данными")
    def test_login_invalid_credentials(self):
        response = requests.post(
            f"{BASE_URL}/courier/login",
            json={"login": "invalid_login", "password": "invalid_password"}
        )
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]