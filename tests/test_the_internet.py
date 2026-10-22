"""
Explicit-wait and browser-feature scenarios on https://the-internet.herokuapp.com
(a practice site made for exactly these cases).
"""

import allure
import pytest
from playwright.sync_api import Page, expect

import config

pytestmark = [pytest.mark.the_internet, allure.epic("The Internet"), pytest.mark.regression]


@allure.feature("Dynamic loading")
@pytest.mark.parametrize("example", [1, 2], ids=["element-hidden-on-page", "element-added-later"])
def test_waits_for_dynamically_loaded_element(page: Page, example):
    page.goto(f"{config.INTERNET_URL}/dynamic_loading/{example}")
    page.locator("#start button").click()
    # Explicit wait: the text appears after a loading bar; no sleep() anywhere.
    expect(page.locator("#finish")).to_have_text("Hello World!", timeout=15_000)
    expect(page.locator("#loading")).to_be_hidden()


@allure.feature("Checkboxes")
def test_checkboxes_can_be_toggled(page: Page):
    page.goto(f"{config.INTERNET_URL}/checkboxes")
    first, second = page.locator("#checkboxes input").nth(0), page.locator("#checkboxes input").nth(1)
    expect(first).not_to_be_checked()
    expect(second).to_be_checked()
    first.check()
    second.uncheck()
    expect(first).to_be_checked()
    expect(second).not_to_be_checked()


@allure.feature("Dropdown")
@pytest.mark.parametrize("option", ["1", "2"])
def test_dropdown_selection(page: Page, option):
    page.goto(f"{config.INTERNET_URL}/dropdown")
    page.locator("#dropdown").select_option(option)
    expect(page.locator("#dropdown")).to_have_value(option)


@allure.feature("JavaScript dialogs")
def test_js_alert_is_accepted(page: Page):
    page.goto(f"{config.INTERNET_URL}/javascript_alerts")
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Alert").click()
    expect(page.locator("#result")).to_have_text("You successfully clicked an alert")


@allure.feature("JavaScript dialogs")
def test_js_confirm_is_dismissed(page: Page):
    page.goto(f"{config.INTERNET_URL}/javascript_alerts")
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="Click for JS Confirm").click()
    expect(page.locator("#result")).to_have_text("You clicked: Cancel")


@allure.feature("JavaScript dialogs")
def test_js_prompt_receives_text(page: Page):
    page.goto(f"{config.INTERNET_URL}/javascript_alerts")
    page.once("dialog", lambda dialog: dialog.accept("QA"))
    page.get_by_role("button", name="Click for JS Prompt").click()
    expect(page.locator("#result")).to_have_text("You entered: QA")


@allure.feature("Form authentication")
@pytest.mark.parametrize(
    "username, password, message",
    [
        ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"),
        ("tomsmith", "wrong", "Your password is invalid!"),
        ("nobody", "SuperSecretPassword!", "Your username is invalid!"),
    ],
    ids=["valid", "wrong-password", "wrong-username"],
)
def test_form_authentication(page: Page, username, password, message):
    page.goto(f"{config.INTERNET_URL}/login")
    page.locator("#username").fill(username)
    page.locator("#password").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash")).to_contain_text(message)
