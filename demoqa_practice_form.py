import pytest
import time
import os
from playwright.sync_api import sync_playwright, expect
from pytest_playwright.pytest_playwright import browser

BASE_URL = "https://demoqa.com"
PRACTICE_FORM_URL = f"{BASE_URL}/automation-practice-form"

USER_DATA = {
    "first_name": "Alexander",
    "last_name": "Mazein",
    "email": "alexander.mazein@gmail.com",
    "phone_number": "2131231231"
}

@pytest.fixture
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False)
        page = browser.new_page()

        page.set_viewport_size({"width": 1920, "height": 1080})

        yield page


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

    time.sleep(30)