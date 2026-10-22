"""Shared fixtures and hooks. Browser/page fixtures come from pytest-playwright."""

import allure
import pytest
from playwright.sync_api import Page

import config
from pages import CartPage, CheckoutPage, InventoryPage, LoginPage


@pytest.fixture(scope="session", autouse=True)
def _use_data_test_attribute(playwright):
    """saucedemo marks elements with data-test, so get_by_test_id() must look at that attribute."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 800}, "locale": "en-US"}


# ── page objects ──────────────────────────────────────────────────────────────

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(page: Page, login_page: LoginPage) -> InventoryPage:
    """A logged-in standard user, already on the inventory page."""
    login_page.login("standard_user", config.PASSWORD)
    page.wait_for_url("**/inventory.html")  # explicit wait for navigation
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


# ── Allure: attach a screenshot and URL when a UI test fails ─────────────────

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    page = item.funcargs.get("page")
    if page is None or page.is_closed():
        return
    try:
        allure.attach(page.screenshot(full_page=True), name="Screenshot on failure",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(page.url, name="Page URL", attachment_type=allure.attachment_type.TEXT)
    except Exception:  # never hide the real failure because of a reporting problem
        pass
