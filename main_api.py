import requests
import json
import pytest
import random
import string

# URL тестового API сервиса - reqres.in является отличным бесплатным ресурсом для практики тестирования API
BASE_URL = "https://reqres.in/api"

# Глобальные переменные для хранения временных данных между тестами
created_user_id = None
test_user_data = None


# Вспомогательная функция для генерации случайных строк (для тестовых данных)
def generate_random_string(length=8):
    """
    Генерирует случайную строку указанной длины.
    Полезно для создания уникальных тестовых данных.
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


# Вспомогательная функция для логирования запросов и ответов
def log_request_info(method, url, data=None, response=None):
    """
    Выводит информацию о запросе и ответе для отладки.
    Помогает понять, что происходит во время выполнения тестов.
    """
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


# Тест на получение списка пользователей
def test_get_users_list():
    """
    Тест GET запроса для получения списка пользователей.
    Проверяет статус-код ответа и структуру данных.
    """
    # Формируем URL для запроса списка пользователей
    url = f"{BASE_URL}/users"

    # Отправляем GET запрос
    response = requests.get(url)

    # Логируем информацию о запросе и ответе
    log_request_info("GET", url, response=response)

    # Проверяем, что статус-код ответа равен 200 (OK)
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    # Проверяем, что ответ содержит ключи 'data' и 'page'
    response_data = response.json()
    assert 'data' in response_data, "Ответ не содержит ключ 'data'"
    assert 'page' in response_data, "Ответ не содержит ключ 'page'"

    # Проверяем, что список пользователей не пустой
    assert len(response_data['data']) > 0, "Список пользователей пуст"


# Тест на получение информации о конкретном пользователе
def test_get_single_user():
    """
    Тест GET запроса для получения информации о конкретном пользователе.
    Проверяет статус-код ответа и данные пользователя.
    """
    # Используем ID существующего пользователя (например, 2)
    user_id = 2
    url = f"{BASE_URL}/users/{user_id}"

    # Отправляем GET запрос
    response = requests.get(url)

    # Логируем информацию
    log_request_info("GET", url, response=response)

    # Проверки
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'data' in response_data, "Ответ не содержит ключ 'data'"

    user_data = response_data['data']
    assert user_data['id'] == user_id, f"ID пользователя в ответе ({user_data['id']}) не соответствует запрошенному ({user_id})"
    assert 'email' in user_data, "Данные пользователя не содержат email"
    assert 'first_name' in user_data, "Данные пользователя не содержат first_name"
    assert 'last_name' in user_data, "Данные пользователя не содержат last_name"


# Тест на создание нового пользователя
def test_create_user():
    """
    Тест POST запроса для создания нового пользователя.
    Проверяет статус-код ответа и возвращаемые данные.
    Сохраняет ID созданного пользователя для последующих тестов.
    """
    global created_user_id, test_user_data

    # Формируем тестовые данные для создания пользователя
    test_user_data = {
        "name": f"Test User {generate_random_string()}",
        "job": "QA Engineer"
    }

    url = f"{BASE_URL}/users"

    # Отправляем POST запрос с данными пользователя
    response = requests.post(url, json=test_user_data)

    # Логируем информацию
    log_request_info("POST", url, test_user_data, response)

    # Проверки
    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"

    response_data = response.json()
    assert 'id' in response_data, "Ответ не содержит ID созданного пользователя"
    assert 'name' in response_data, "Ответ не содержит имя пользователя"
    assert response_data['name'] == test_user_data['name'], "Имя пользователя в ответе не соответствует отправленному"

    # Сохраняем ID созданного пользователя для использования в других тестах
    created_user_id = response_data['id']


# Тест на обновление данных пользователя (PUT)
def test_update_user_put():
    """
    Тест PUT запроса для полного обновления данных пользователя.
    Проверяет статус-код ответа и обновленные данные.
    Использует ID пользователя, созданного в предыдущем тесте.
    """
    global test_user_data

    # Проверяем, что у нас есть ID пользователя из предыдущего теста
    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")

    # Обновляем данные пользователя
    updated_user_data = {
        "name": f"Updated User {generate_random_string()}",
        "job": "Senior QA Engineer"
    }

    url = f"{BASE_URL}/users/{created_user_id}"

    # Отправляем PUT запрос с обновленными данными
    response = requests.put(url, json=updated_user_data)

    # Логируем информацию
    log_request_info("PUT", url, updated_user_data, response)

    # Проверки
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'name' in response_data, "Ответ не содержит имя пользователя"
    assert response_data['name'] == updated_user_data[
        'name'], "Имя пользователя в ответе не соответствует отправленному"

    # Обновляем данные пользователя для использования в других тестах
    test_user_data = updated_user_data


# Тест на частичное обновление данных пользователя (PATCH)
def test_update_user_patch():
    """
    Тест PATCH запроса для частичного обновления данных пользователя.
    Проверяет статус-код ответа и обновленные данные.
    """
    # Проверяем, что у нас есть ID пользователя из предыдущего теста
    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")

    # Частично обновляем данные пользователя (только job)
    patch_data = {
        "job": "Lead QA Engineer"
    }

    url = f"{BASE_URL}/users/{created_user_id}"

    # Отправляем PATCH запрос с обновленными данными
    response = requests.patch(url, json=patch_data)

    # Логируем информацию
    log_request_info("PATCH", url, patch_data, response)

    # Проверки
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'job' in response_data, "Ответ не содержит должность пользователя"
    assert response_data['job'] == patch_data['job'], "Должность пользователя в ответе не соответствует отправленной"


# Тест на удаление пользователя
def test_delete_user():
    """
    Тест DELETE запроса для удаления пользователя.
    Проверяет статус-код ответа.
    """
    # Проверяем, что у нас есть ID пользователя из предыдущих тестов
    if not created_user_id:
        pytest.skip("Пропуск теста, так как ID пользователя не был получен")

    url = f"{BASE_URL}/users/{created_user_id}"

    # Отправляем DELETE запрос
    response = requests.delete(url)

    # Логируем информацию
    log_request_info("DELETE", url, response=response)

    # Для DELETE запроса ожидаем статус-код 204 (No Content)
    assert response.status_code == 204, f"Ожидался статус-код 204, получен {response.status_code}"

    # Проверяем, что тело ответа пустое
    assert response.text == "", "Ответ на DELETE запрос должен быть пустым"


# Тест на попытку получения несуществующего пользователя
def test_get_nonexistent_user():
    """
    Негативный тест GET запроса для получения несуществующего пользователя.
    Проверяет, что API возвращает правильный статус-код ошибки.
    """
    # Используем заведомо несуществующий ID пользователя
    user_id = 999
    url = f"{BASE_URL}/users/{user_id}"

    # Отправляем GET запрос
    response = requests.get(url)

    # Логируем информацию
    log_request_info("GET", url, response=response)

    # Ожидаем статус-код 404 (Not Found)
    assert response.status_code == 404, f"Ожидался статус-код 404, получен {response.status_code}"


# Тест с невалидными данными при создании пользователя
def test_create_user_invalid_data():
    """
    Негативный тест POST запроса с невалидными данными.
    Проверяет обработку ошибочных данных сервером.
    """
    # Пустые данные для создания пользователя
    empty_data = {}

    url = f"{BASE_URL}/users"

    # Отправляем POST запрос с пустыми данными
    response = requests.post(url, json=empty_data)

    # Логируем информацию
    log_request_info("POST", url, empty_data, response)

    # Проверяем, что API возвращает успешный статус (в данном случае 201),
    # так как reqres.in принимает пустые данные, но это редкость в реальных API
    # В реальном проекте здесь обычно был бы код 400 Bad Request
    assert response.status_code == 201, f"Ожидался статус-код 201, получен {response.status_code}"


# Тест на регистрацию пользователя
def test_register_user_successful():
    """
    Тест POST запроса для регистрации пользователя.
    Проверяет успешную регистрацию и получение токена.
    """
    # Данные для регистрации (используем существующего пользователя из reqres.in)
    register_data = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    url = f"{BASE_URL}/register"

    # Отправляем POST запрос для регистрации
    response = requests.post(url, json=register_data)

    # Логируем информацию
    log_request_info("POST", url, register_data, response)

    # Проверки
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    response_data = response.json()
    assert 'token' in response_data, "Ответ не содержит токен"
    assert 'id' in response_data, "Ответ не содержит ID пользователя"


# Тест на неудачную регистрацию (без пароля)
def test_register_user_unsuccessful():
    """
    Негативный тест POST запроса для регистрации пользователя без указания пароля.
    Проверяет обработку ошибки сервером.
    """
    # Неполные данные для регистрации (отсутствует пароль)
    incomplete_data = {
        "email": "sydney@fife"
    }

    url = f"{BASE_URL}/register"

    # Отправляем POST запрос с неполными данными
    response = requests.post(url, json=incomplete_data)

    # Логируем информацию
    log_request_info("POST", url, incomplete_data, response)

    # Ожидаем статус-код ошибки 400 (Bad Request)
    assert response.status_code == 400, f"Ожидался статус-код 400, получен {response.status_code}"

    response_data = response.json()
    assert 'error' in response_data, "Ответ не содержит сообщение об ошибке"


# Для запуска тестов в терминале выполните:
# pytest api_test.py -v
# Флаг -v включает подробный вывод результатов тестирования

if __name__ == "__main__":
    # Этот блок выполняется, если скрипт запущен напрямую через Python, а не через pytest
    print("Запуск тестов API...")

    # Можно вручную запустить отдельные тесты для демонстрации
    test_get_users_list()
    test_get_single_user()
    test_create_user()
    test_update_user_put()
    test_update_user_patch()
    test_delete_user()
    test_get_nonexistent_user()
    test_create_user_invalid_data()
    test_register_user_successful()
    test_register_user_unsuccessful()

    print("\nВсе тесты выполнены!")