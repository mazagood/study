import requests
import json
import pytest
import random
import string

BASE_URL = "https://reqres.in/api"

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

    response = requests.get(url)

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