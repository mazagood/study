import pytest
import time
from playwright.sync_api import sync_playwright, expect


BASE_URL = "https://demoqa.com"
PRACTICE_FORM_URL = f"{BASE_URL}/automation-practice-form"

USER_DATA = {
    "first_name": "Alexander",
    "last_name": "Mazein",
    "email": "random.mail@gmail.com",
    "phone_number": "2131231231",
    "address": "Раушская наб., 6, Москва, 115035"
}

@pytest.fixture
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False)
        page = browser.new_page()

        page.set_viewport_size({"width": 1920, "height": 1080})

        yield page

        browser.close()

def scroll_to_element(page, selector):
    page.evaluate(f'document.querySelector("{selector}").scrollIntroView()')
    time.sleep(0.5)

def test_practice_form(page):
    page.goto(PRACTICE_FORM_URL)

    page.fill("#firstName", USER_DATA["first_name"])
    page.fill("#lastName", USER_DATA["last_name"])
    page.fill("#userEmail", USER_DATA["email"])

    page.click("//label[@for='gender-radio-1']")

    page.fill("#userNumber", USER_DATA["phone_number"])

    page.click("#dateOfBirthInput")
    page.click('.react-datepicker__month-select')
    page.select_option('.react-datepicker__month-select', value='9')
    page.click('.react-datepicker__year-select')
    page.select_option('.react-datepicker__year-select', value='2017')
    page.click('.react-datepicker__day--025')

    page.fill("#subjectsInput", "Ph")
    page.click("#react-select-2-option-0")
    page.fill("#subjectsInput", "C")
    page.click("#react-select-2-option-6")
    page.fill("#subjectsInput", "E")
    page.click("#react-select-2-option-4")

    page.click("//label[@for='hobbies-checkbox-1']")
    page.click("//label[@for='hobbies-checkbox-2']")
    page.click("//label[@for='hobbies-checkbox-3']")
    page.click("//label[@for='hobbies-checkbox-2']")

    test_file_path = "test_upload.png"

    file_input = page.locator("#uploadPicture")
    file_input.set_input_files(test_file_path)

    page.fill("#currentAddress", USER_DATA["address"])

    page.click("#state")
    page.click("#react-select-3-option-3")
    page.click("#city")
    page.click("#react-select-4-option-0")

    page.click("#submit")
    time.sleep(2)
    page.click("#closeLargeModal")

    time.sleep(2)