import requests
import json
import pytest
import random
import string

BASE_URL = "https://reqres.in/api"

headers = {
    'x-api-key': 'reqres-free-v1'
}

created_user_id = None
test_user_data = None

def generate_random_string(length=8):

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def log_request_info(method, url, data=None, response=None):

    print(f"\n=== {method} Request to {url} ===")
    if data:
        print(f"Request body: {json.dumps(data, indent=2)}")
    if response:
        print(f"Status code: {response.status_code}")
        try:
            print(f"Response body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response body: {response.text}")
    print("=" * 50)


def test_get_user_list():

    url = f"{BASE_URL}/users"

    response = requests.get(url)

    log_request_info("GET", url, response=response)

    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'data' in response_data, "Ответ не содержит ключ 'data'"
    assert 'page' in response_data, "Ответ не содержит ключ 'page'"

    for user_data in response_data['data']:
        assert 'id' in user_data, "Ответ не содержит ключ 'id'"
        assert 'email' in user_data, "Ответ не содержит ключ 'email'"
        assert 'first_name' in user_data, "Ответ не содержит ключ 'first_name'"
        assert 'last_name' in user_data, "Ответ не содержит ключ 'last_name'"

    assert len(response_data['data']) > 0, "Список пользователей пуст"

def test_get_single_user():

    user_id = 3
    url = f"{BASE_URL}/users/{user_id}"

    response = requests.get(url, headers=headers)

    log_request_info("GET", url, response=response)

    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'data' in response_data, "Ответ не содержит ключ 'data'"

    user_data = response_data['data']
    assert user_data['id'] == user_id, f"ID пользователя в ответе ({user_data['data']}) не соответствует запрошенному ({user_id})"
    assert 'email' in user_data, "Данные пользователя не содержат email"
    assert 'first_name' in user_data, "Данные пользователя не содержат first_name"
    assert 'last_name' in user_data, "Данные пользователя не содержат last_name"
    assert '@' in user_data['email'], "Email не содержит символ @"

def test_create_user():

    global created_user_id, test_user_data

    test_user_data = {
        "name": f"Test User {generate_random_string()}",
        "job": "QA Engineer"
    }

    url = f"{BASE_URL}/users"

    response = requests.post(url, json=test_user_data, headers=headers)

    log_request_info("POST", url, test_user_data, response)

    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"

    response_data = response.json()
    assert 'id' in response_data, "Ответ не содержит ID созданного пользователя"
    assert 'name' in response_data, "Ответ не содержит имя пользователя"
    assert response_data['name'] == test_user_data['name'], "Имя пользователя в ответе не соответствует отправленному"

    created_user_id = response_data['id']

def test_update_user_put():

    global test_user_data

    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")

    updated_user_data = {
        "name": f"Update User {generate_random_string()}",
        "job": "Senior QA Engineer"
    }

    url = f"{BASE_URL}/users/{created_user_id}"

    response = requests.put(url, json=updated_user_data, headers=headers)

    log_request_info("PUT", url, updated_user_data, response)

    assert  response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'name' in response_data, "Ответ не содержит имя пользователя"
    assert response_data['name'] == updated_user_data['name'], "Имя пользователя в ответе не соответствует отправленному"

    test_user_data = updated_user_data

def test_update_user_patch():

    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")

    patch_data = {
        "job": "Lead QA Engineer"
    }

    url = f"{BASE_URL}/users/{created_user_id}"

    response = requests.patch(url, json=patch_data, headers=headers)

    log_request_info("PATCH", url, patch_data, response)

    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data  = response.json()
    assert 'job' in response_data, "Ответ не содержит должность пользователя"
    assert response_data['job'] == patch_data['job'], "Должность пользователя в ответе не соответствует отправленной"

def test_delete_user():

    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")

    url = f"{BASE_URL}/users/{created_user_id}"

    response = requests.delete(url, headers=headers)

    log_request_info("DELETE", url, response=response)

    assert response.status_code == 204, f"Ожидался статус-код 204, получен {response.status_code}"
    assert response.text == '', "Ответ на DELETE запрос должен быть пустым"

def test_get_nonexistent_user():

    user_id = 999
    url = f"{BASE_URL}/users/{user_id}"

    response = requests.get(url, headers=headers)

    log_request_info("GET", url, response=response)

    assert response.status_code == 404, f"Ожидался статус-код 404, получен {response.status_code}"

def test_create_user_invalid_data():

    empty_data = {}

    url = f"{BASE_URL}/users"

    response = requests.post(url, json=empty_data, headers=headers)

    log_request_info("POST", url, empty_data, response)

    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"

def test_register_user_successful():

    register_data = {
        "email": "eve.holt@reqres.in",
        "password": "correct_password"
    }

    url = f"{BASE_URL}/register"

    response = requests.post(url, json=register_data, headers=headers)

    log_request_info("POST", url, register_data, response)

    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'token' in response_data, "Ответ не содержит токен"
    assert 'id' in response_data, "Ответ не содержит ID пользователя"

def test_register_user_unsuccessful():

    incomplete_data = {
        "email": "sydney@fife"
    }

    url = f"{BASE_URL}/register"

    response = requests.post(url, json=incomplete_data, headers=headers)

    log_request_info("POST", url, incomplete_data, response)

    assert response.status_code == 400, f"Ожидался статус-код 400, получен {response.status_code}"

    response_data = response.json()
    assert 'error' in response_data, "Ответ е содержит сообщение об ошибке"

def test_get_users_witch_pagination():

    url = f"{BASE_URL}/users?page=2&per_page=3"

    response = requests.get(url, headers=headers)

    log_request_info("GET", url, response=response)

    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert response_data['page'] == 2
    assert len(response_data['data']) <= 3, "Список пользователей пуст"

def test_login_successful():

    user_data = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    url = f"{BASE_URL}/login"

    response = requests.post(url, json=user_data, headers=headers)

    log_request_info("POST", url, response=response)

    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'token' in response_data, f"Ответ не содержит token"


