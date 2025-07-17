import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def create_new_courier():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}/courier", json=payload)

    if response.status_code == 201:
        return {
            "login": login,
            "password": password,
            "first_name": first_name
        }
    return None


def delete_courier(courier_id):
    return requests.delete(f"{BASE_URL}/courier/{courier_id}")


def login_courier(login, password):
    payload = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}/courier/login", json=payload)
    return response.json().get("id") if response.status_code == 200 else None