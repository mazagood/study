# demoqa_tests.py
# Простой проект автоматизированного тестирования на Playwright для сайта DEMOQA
# Этот файл содержит несколько базовых тестов для различных элементов и форм DEMOQA

import pytest
import time
import os
from playwright.sync_api import sync_playwright, expect

# Константы для тестирования
BASE_URL = "https://demoqa.com"
TEXT_BOX_URL = f"{BASE_URL}/text-box"
CHECK_BOX_URL = f"{BASE_URL}/checkbox"
RADIO_BUTTON_URL = f"{BASE_URL}/radio-button"
WEB_TABLES_URL = f"{BASE_URL}/webtables"
BUTTONS_URL = f"{BASE_URL}/buttons"
DYNAMIC_PROPERTIES_URL = f"{BASE_URL}/dynamic-properties"

# Тестовые данные
USER_DATA = {
    "full_name": "John Doe",
    "email": "johndoe@example.com",
    "current_address": "123 Main Street, City",
    "permanent_address": "456 Park Avenue, Town"
}


# Фикстура для инициализации Playwright и создания страницы
@pytest.fixture
def page():
    # Запускаем Playwright
    with sync_playwright() as playwright:
        # Создаём браузер и страницу
        browser = playwright.chromium.launch(
            headless=False)  # headless=False позволяет видеть браузер во время выполнения
        page = browser.new_page()

        # Настраиваем размер окна браузера
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Передаём страницу в тест
        yield page

        # Закрываем браузер после окончания теста
        browser.close()


# Вспомогательная функция для скролла до элемента
def scroll_to_element(page, selector):
    """
    Прокручивает страницу до указанного элемента.
    """
    page.evaluate(f'document.querySelector("{selector}").scrollIntoView()')
    time.sleep(0.5)  # Даем время для завершения скролла


# Тест 1: Заполнение и отправка формы Text Box
def test_text_box_form(page):
    """
    Tест проверяет заполнение и отправку формы Text Box
    с последующей проверкой отображения введенных данных.
    """
    # Шаг 1: Переходим на страницу Text Box
    page.goto(TEXT_BOX_URL)

    # Шаг 2: Заполняем поля формы
    page.fill("#userName", USER_DATA["full_name"])
    page.fill("#userEmail", USER_DATA["email"])
    page.fill("#currentAddress", USER_DATA["current_address"])
    page.fill("#permanentAddress", USER_DATA["permanent_address"])

    # Шаг 3: Скроллим до кнопки отправки и нажимаем её
    scroll_to_element(page, "#submit")
    page.click("#submit")

    # Проверка: Проверяем, что на странице появились введенные данные
    output = page.locator(".border")
    expect(output).to_be_visible()

    # Проверяем каждое поле в выводе с уточненными селекторами
    expect(page.locator("#name")).to_contain_text(USER_DATA["full_name"])
    expect(page.locator("#email")).to_contain_text(USER_DATA["email"])
    expect(page.locator(".border #currentAddress")).to_contain_text(USER_DATA["current_address"])
    expect(page.locator(".border #permanentAddress")).to_contain_text(USER_DATA["permanent_address"])


# Тест 2: Работа с CheckBox
def test_check_box(page):
    """
    Тест проверяет выбор и состояние чекбоксов
    в древовидной структуре.
    """
    # Шаг 1: Переходим на страницу CheckBox
    page.goto(CHECK_BOX_URL)

    # Шаг 2: Раскрываем корневой элемент (Home)
    page.click(".rct-collapse-btn")

    # Шаг 3: Кликаем по чекбоксу "Desktop"
    page.click("//span[text()='Desktop']/..//span[@class='rct-checkbox']")

    # Проверка: Desktop и его дочерние элементы выбраны
    result_text = page.locator(".display-result")
    expect(result_text).to_be_visible()
    expect(result_text).to_contain_text("desktop")
    expect(result_text).to_contain_text("notes")
    expect(result_text).to_contain_text("commands")

    # Шаг 4: Кликаем по чекбоксу "Documents"
    page.click("//span[text()='Documents']/..//span[@class='rct-checkbox']")

    # Проверка: Documents и его дочерние элементы выбраны
    expect(result_text).to_contain_text("documents")
    expect(result_text).to_contain_text("workspace")
    expect(result_text).to_contain_text("office")


# Тест 3: Работа с Radio Button
def test_radio_button(page):
    """
    Тест проверяет выбор радиокнопок и
    отображение соответствующего сообщения.
    """
    # Шаг 1: Переходим на страницу Radio Button
    page.goto(RADIO_BUTTON_URL)

    # Шаг 2: Выбираем радиокнопку "Yes"
    page.click("//label[@for='yesRadio']")

    # Проверка: Появляется сообщение "You have selected Yes"
    success_text = page.locator(".text-success")
    expect(success_text).to_be_visible()
    expect(success_text).to_have_text("Yes")

    # Шаг 3: Выбираем радиокнопку "Impressive"
    page.click("//label[@for='impressiveRadio']")

    # Проверка: Появляется сообщение "You have selected Impressive"
    expect(success_text).to_be_visible()
    expect(success_text).to_have_text("Impressive")

    # Проверка: Радиокнопка "No" отключена
    no_radio = page.locator("#noRadio")
    expect(no_radio).to_be_disabled()


# Тест 4: Работа с Web Tables
def test_web_tables(page):
    """
    Тест проверяет добавление, редактирование и удаление
    записей в веб-таблице.
    """
    # Данные для нового пользователя
    new_user = {
        "firstName": "Michael",
        "lastName": "Smith",
        "email": "michaelsmith@example.com",
        "age": "35",
        "salary": "6000",
        "department": "QA"
    }

    # Данные для редактирования
    edited_data = {
        "firstName": "Michael",
        "lastName": "Johnson",
        "email": "michaeljohnson@example.com",
        "age": "36",
        "salary": "7000",
        "department": "Development"
    }

    # Шаг 1: Переходим на страницу Web Tables
    page.goto(WEB_TABLES_URL)

    # Шаг 2: Нажимаем кнопку добавления
    page.click("#addNewRecordButton")

    # Шаг 3: Заполняем форму регистрации
    page.fill("#firstName", new_user["firstName"])
    page.fill("#lastName", new_user["lastName"])
    page.fill("#userEmail", new_user["email"])
    page.fill("#age", new_user["age"])
    page.fill("#salary", new_user["salary"])
    page.fill("#department", new_user["department"])

    # Шаг 4: Нажимаем кнопку Submit
    page.click("#submit")

    # Проверка: Новый пользователь добавлен в таблицу
    page.wait_for_selector(f"//div[contains(@class, 'rt-tbody')]//div[contains(text(), '{new_user['email']}')]")

    # Шаг 5: Редактируем добавленную запись
    # Нажимаем кнопку редактирования для только что добавленной записи
    edit_button = page.locator(f"//div[contains(text(), '{new_user['email']}')]/following::div//span[@title='Edit']")
    edit_button.click()

    # Шаг 6: Обновляем данные в форме
    page.fill("#firstName", edited_data["firstName"])
    page.fill("#lastName", edited_data["lastName"])
    page.fill("#userEmail", edited_data["email"])
    page.fill("#age", edited_data["age"])
    page.fill("#salary", edited_data["salary"])
    page.fill("#department", edited_data["department"])

    # Шаг 7: Сохраняем изменения
    page.click("#submit")

    # Проверка: Данные пользователя обновлены
    page.wait_for_selector(f"//div[contains(@class, 'rt-tbody')]//div[contains(text(), '{edited_data['email']}')]")

    # Шаг 8: Удаляем запись
    delete_button = page.locator(
        f"//div[contains(text(), '{edited_data['email']}')]/following::div//span[@title='Delete']")
    delete_button.click()

    # Проверка: Запись удалена
    expect(page.locator(f"//div[contains(text(), '{edited_data['email']}')]")).to_have_count(0)


# Тест 5: Тестирование кнопок
def test_buttons(page):
    """
    Тест проверяет разные варианты клика по кнопкам:
    обычный клик, двойной клик и клик правой кнопкой мыши.
    """
    # Шаг 1: Переходим на страницу Buttons
    page.goto(BUTTONS_URL)

    # Шаг 2: Выполняем двойной клик
    double_click_button = page.locator("#doubleClickBtn")
    double_click_button.dblclick()

    # Проверка: Появляется сообщение о двойном клике
    expect(page.locator("#doubleClickMessage")).to_be_visible()
    expect(page.locator("#doubleClickMessage")).to_have_text("You have done a double click")

    # Шаг 3: Выполняем клик правой кнопкой мыши
    right_click_button = page.locator("#rightClickBtn")
    right_click_button.click(button="right")

    # Проверка: Появляется сообщение о клике правой кнопкой мыши
    expect(page.locator("#rightClickMessage")).to_be_visible()
    expect(page.locator("#rightClickMessage")).to_have_text("You have done a right click")

    # Шаг 4: Выполняем обычный клик
    # Используем селектор XPath, чтобы выбрать кнопку "Click Me"
    page.click("//button[text()='Click Me']")

    # Проверка: Появляется сообщение о динамическом клике
    expect(page.locator("#dynamicClickMessage")).to_be_visible()
    expect(page.locator("#dynamicClickMessage")).to_have_text("You have done a dynamic click")


# Тест 6: Проверка динамических свойств
def test_dynamic_properties(page):
    """
    Тест проверяет элементы с динамическими свойствами:
    кнопка, которая становится активной через 5 секунд,
    кнопка, которая меняет цвет, и кнопка, которая появляется через 5 секунд.
    """
    # Шаг 1: Переходим на страницу Dynamic Properties
    page.goto(DYNAMIC_PROPERTIES_URL)

    # Шаг 2: Проверяем исходное состояние первой кнопки (disabled)
    will_enable_button = page.locator("#enableAfter")
    expect(will_enable_button).to_be_disabled()

    # Шаг 3: Ждем, пока кнопка станет активной
    page.wait_for_selector("#enableAfter:not([disabled])")

    # Проверка: Кнопка стала активной
    expect(will_enable_button).to_be_enabled()

    # Шаг 4: Проверяем кнопку, которая меняет цвет
    color_change_button = page.locator("#colorChange")

    # Ждем, пока цвет изменится
    page.wait_for_function("""
        () => {
            const button = document.querySelector('#colorChange');
            const style = window.getComputedStyle(button);
            return style.color === 'rgb(220, 53, 69)';
        }
    """)

    # Шаг 5: Проверяем видимость кнопки "Visible After 5 Seconds"
    visible_after_button = page.locator("#visibleAfter")

    # Проверяем, что кнопка существует и видима
    # Если кнопка еще не видима, ждем ее появления
    if not visible_after_button.is_visible():
        page.wait_for_selector("#visibleAfter", state="visible")

    # Проверка: Кнопка видима
    expect(visible_after_button).to_be_visible()


# Тест 7: Загрузка файла
def test_upload_and_download(page):
    """
    Тест проверяет функциональность загрузки и скачивания файлов.
    """
    # Константа для страницы загрузки
    UPLOAD_DOWNLOAD_URL = f"{BASE_URL}/upload-download"

    # Шаг 1: Переходим на страницу Upload and Download
    page.goto(UPLOAD_DOWNLOAD_URL)

    # Создаем временный файл для теста
    test_file_path = "test_upload.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test file content for upload testing.")

    # Шаг 2: Загружаем файл
    file_input = page.locator("#uploadFile")
    file_input.set_input_files(test_file_path)

    # Проверка: Отображается имя загруженного файла
    upload_result = page.locator("#uploadedFilePath")
    expect(upload_result).to_be_visible()
    expect(upload_result).to_contain_text("test_upload.txt")

    # Удаляем временный файл после использования
    os.remove(test_file_path)

    # Шаг 3: Проверяем кнопку скачивания
    download_button = page.locator("#downloadButton")
    expect(download_button).to_be_visible()

    # Примечание: Фактическое скачивание не тестируем, так как это требует
    # дополнительной настройки для работы с файловой системой


# Тест 8: Модальные диалоги
def test_modal_dialogs(page):
    """
    Тест проверяет работу с модальными диалогами:
    маленький и большой диалоги.
    """
    # Константа для страницы модальных диалогов
    MODAL_DIALOGS_URL = f"{BASE_URL}/modal-dialogs"

    # Шаг 1: Переходим на страницу Modal Dialogs
    page.goto(MODAL_DIALOGS_URL)

    # Шаг 2: Открываем маленький модальный диалог
    page.click("#showSmallModal")

    # Проверка: Диалог отображается
    small_modal = page.locator(".modal-content")
    expect(small_modal).to_be_visible()

    # Проверяем заголовок и содержимое
    expect(page.locator(".modal-title")).to_have_text("Small Modal")
    expect(page.locator(".modal-body")).to_contain_text("This is a small modal")

    # Шаг 3: Закрываем маленький диалог
    page.click("#closeSmallModal")

    # Дожидаемся закрытия диалога
    expect(small_modal).to_have_count(0)

    # Шаг 4: Открываем большой модальный диалог
    page.click("#showLargeModal")

    # Проверка: Диалог отображается
    large_modal = page.locator(".modal-content")
    expect(large_modal).to_be_visible()

    # Проверяем заголовок
    expect(page.locator(".modal-title")).to_have_text("Large Modal")

    # Шаг 5: Закрываем большой диалог
    page.click("#closeLargeModal")

    # Дожидаемся закрытия диалога
    expect(large_modal).to_have_count(0)

# Запуск тестов:
# pytest -v demoqa_tests.py