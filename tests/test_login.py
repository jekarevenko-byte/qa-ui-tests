import allure
import pytest
from playwright.sync_api import Page, expect

import config
from pages import InventoryPage, LoginPage

pytestmark = [pytest.mark.saucedemo, allure.epic("Sauce Demo"), allure.feature("Login")]


@pytest.mark.smoke
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.parametrize("username", ["standard_user", "problem_user", "performance_glitch_user"])
def test_valid_user_can_log_in(page: Page, login_page: LoginPage, username):
    login_page.login(username, config.PASSWORD)
    # performance_glitch_user is deliberately slow, so the wait is longer than the 5 s default
    expect(page).to_have_url(f"{config.SAUCE_URL}/inventory.html", timeout=20_000)
    expect(InventoryPage(page).title).to_have_text("Products")


@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, message",
    [
        ("standard_user", "wrong_password", "Username and password do not match any user in this service"),
        ("no_such_user", config.PASSWORD, "Username and password do not match any user in this service"),
        ("", config.PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
        ("", "", "Username is required"),
    ],
    ids=["wrong-password", "unknown-user", "empty-username", "empty-password", "both-empty"],
)
def test_invalid_credentials_show_error(page: Page, login_page: LoginPage, username, password, message):
    login_page.login(username, password)
    expect(login_page.error).to_contain_text(message)
    expect(page).to_have_url(f"{config.SAUCE_URL}/")


@pytest.mark.negative
@pytest.mark.regression
def test_locked_out_user_is_rejected(login_page: LoginPage):
    login_page.login("locked_out_user", config.PASSWORD)
    expect(login_page.error).to_have_text("Epic sadface: Sorry, this user has been locked out.")


@pytest.mark.negative
@pytest.mark.regression
def test_inventory_is_not_accessible_without_login(page: Page):
    page.goto(f"{config.SAUCE_URL}/inventory.html")
    expect(LoginPage(page).error).to_contain_text("You can only access '/inventory.html' when you are logged in")


@pytest.mark.regression
def test_logout_returns_to_login_page(page: Page, inventory_page: InventoryPage):
    inventory_page.logout()
    expect(page).to_have_url(f"{config.SAUCE_URL}/")
    expect(LoginPage(page).login_button).to_be_visible()
