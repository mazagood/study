from tkinter.constants import RADIOBUTTON

import pytest
import time
import os
from playwright.sync_api import sync_playwright, expect
from requests import delete

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

def test_check_box(page):

    page.goto(CHECK_BOX_URL)

    page.click(".rct-collapse-btn")

    page.click("//span[text()='Desktop']/..//span[@class='rct-checkbox']")

    result_text = page.locator(".display-result")
    expect(result_text).to_be_visible()
    expect(result_text).to_contain_text("desktop")
    expect(result_text).to_contain_text("note")
    expect(result_text).to_contain_text("commands")

    page.click("//span[text()='Documents']/../span[@class='rct-checkbox']")

    expect(result_text).to_contain_text("documents")
    expect(result_text).to_contain_text("workspace")
    expect(result_text).to_contain_text("office")

def test_radio_button(page):

    page.goto(RADIO_BUTTON_URL)

    page.click("//label[@for='yesRadio']")

    success_text = page.locator(".text-success")
    expect(success_text).to_be_visible()
    expect(success_text).to_have_text("Yes")

    page.click("//label[@for='impressiveRadio']")

    expect(success_text).to_be_visible()
    expect(success_text).to_have_text("Impressive")

    no_radio = page.locator("#noRadio")
    expect(no_radio).to_be_disabled()

def test_web_tables(page):
    new_user = {
        "fistName": "Michael",
        "lastName": "Smith",
        "email": "michaelsmith@example.com",
        "age": "22",
        "salary": "6000",
        "department": "QA"
    }

    edited_data = {
        "firstName": "Michael",
        "lastName": "Johnson",
        "email": "michaeljohnson@example.com",
        "age": "24",
        "salary": "7000",
        "department": "Development"
    }

    page.goto(WEB_TABLES_URL)

    page.click("#addNewRecordButton")

    page.fill("#firstName", new_user["fistName"])
    page.fill("#lastName", new_user["lastName"])
    page.fill("#userEmail", new_user["email"])
    page.fill("#age", new_user["age"])
    page.fill("#salary", new_user["salary"])
    page.fill("#department", new_user["department"])

    page.click("#submit")

    page.wait_for_selector(f"//div[contains(@class, 'rt-tbody')]//div[contains(text(), '{new_user['email']}')]")

    edit_button = page.locator(f"//div[contains(text(), '{new_user['email']}')]/following::div//span[@title='Edit']")
    edit_button.click()

    page.fill("#firstName", edited_data["firstName"])
    page.fill("#lastName", edited_data["lastName"])
    page.fill("#userEmail", edited_data["email"])
    page.fill("#age", edited_data["age"])
    page.fill("#salary", edited_data["salary"])
    page.fill("#department", edited_data["department"])

    page.click("#submit")

    page.wait_for_selector(f"//div[contains(@class, 'rt-tbody')]//div[contains(text(), '{edited_data['email']}')]")

    delete_button = page.locator(f"//div[contains(text(), '{edited_data['email']}')]/following::div//span[@title='Delete']")
    delete_button.click()

    expect(page.locator(f"//div[contains(text(), '{edited_data['email']}')]")).to_have_count(0)

def test_buttons(page):
     page.goto(BUTTONS_URL)

     double_click_button = page.locator("#doubleClickBtn")
     double_click_button.dblclick()

     expect(page.locator("#doubleClickMessage")).to_be_visible()
     expect(page.locator("#doubleClickMessage")).to_have_text("You have done a double click")

     right_click_button = page.locator("#rightClickBtn")
     right_click_button.click(button="right")

     expect(page.locator("#rightClickMessage")).to_be_visible()
     expect(page.locator("#rightClickMessage")).to_have_text("You have done a right click")

     page.click("//button[text()='Click Me']")

     expect(page.locator("#dynamicClickMessage")).to_be_visible()
     expect(page.locator("#dynamicClickMessage")).to_have_text("You have done a dynamic click")