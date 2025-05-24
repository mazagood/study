from tkinter.constants import RADIOBUTTON

import pytest
import time
import os
from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://demoqa.com"
TEXT_BOX_URL = f"{BASE_URL}/text-box"
CHECK_BOX_URL = f"{BASE_URL}/checkbox"
RADIO_BUTTON_URL = f"{BASE_URL}/radio-button"
WEB_TABLES_URL =f"{BASE_URL}/webtables"
BUTTONS_URL = f"{BASE_URL}/buttons"
DYNAMIC_PROPERTIES_URL = f"{BASE_URL}/dynamic-properties"

USER_DATA = {
    "full_name": "Alexander Mazein",
    "email": "random.mail@gmail.com",
    "address": "Раушская наб., 6, Москва, 115035"
}

@pytest.fixture
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.set_viewport_size({"width": 1920, "height": 1080})

        yield page

        browser.close()

def scroll_to_elements(page, selector):
    page.evaluate(f'document.querySelector("{selector}").scrollIntoView()')
    time.sleep(0.5)

def test_text_box_form(page):

    page.goto(TEXT_BOX_URL)

    page.fill("#userName", USER_DATA["full_name"])
    page.fill("#userEmail", USER_DATA["email"])
    page.fill("#currentAddress", USER_DATA["address"])
    page.fill("#permanentAddress", USER_DATA["address"])

    scroll_to_elements(page, "#submit")
    page.click("#submit")

    output = page.locator(".border")
    expect(output).to_be_visible()

    expect(page.locator("#name")).to_contain_text(USER_DATA["full_name"])
    expect(page.locator("#email")).to_contain_text(USER_DATA["email"])
    expect(page.locator(".border #currentAddress")).to_contain_text(USER_DATA["address"])
    expect(page.locator(".border #permanentAddress")).to_contain_text(USER_DATA["address"])