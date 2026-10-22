import allure
import pytest
from playwright.sync_api import Page, expect

import config
from pages import CartPage, CheckoutPage, InventoryPage

pytestmark = [pytest.mark.saucedemo, allure.epic("Sauce Demo"), allure.feature("Checkout")]

PRICES = {  # published prices of the demo shop
    "sauce-labs-backpack": 29.99,
    "sauce-labs-bike-light": 9.99,
    "sauce-labs-onesie": 7.99,
}


def go_to_checkout(inventory_page: InventoryPage, cart_page: CartPage, slugs):
    for slug in slugs:
        inventory_page.add_to_cart(slug)
    inventory_page.open_cart()
    cart_page.checkout()


@pytest.mark.smoke
@allure.severity(allure.severity_level.CRITICAL)
def test_complete_purchase_end_to_end(page: Page, inventory_page, cart_page, checkout_page: CheckoutPage):
    go_to_checkout(inventory_page, cart_page, ["sauce-labs-backpack"])
    checkout_page.fill_info("Ivan", "Petrov", "101000").continue_()
    checkout_page.finish()
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
    expect(page).to_have_url(f"{config.SAUCE_URL}/checkout-complete.html")
    expect(inventory_page.cart_badge).to_have_count(0)  # cart is emptied after the order


@pytest.mark.regression
@pytest.mark.parametrize(
    "slugs",
    [["sauce-labs-backpack"], ["sauce-labs-backpack", "sauce-labs-bike-light"], list(PRICES)],
    ids=["1-item", "2-items", "3-items"],
)
def test_order_totals_are_calculated_correctly(inventory_page, cart_page, checkout_page: CheckoutPage, slugs):
    go_to_checkout(inventory_page, cart_page, slugs)
    checkout_page.fill_info("Ivan", "Petrov", "101000").continue_()
    expected_subtotal = round(sum(PRICES[s] for s in slugs), 2)
    assert checkout_page.subtotal == pytest.approx(expected_subtotal, abs=0.001)
    assert checkout_page.total == pytest.approx(checkout_page.subtotal + checkout_page.tax, abs=0.011)


@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize(
    "first, last, zip_code, message",
    [
        ("", "Petrov", "101000", "First Name is required"),
        ("Ivan", "", "101000", "Last Name is required"),
        ("Ivan", "Petrov", "", "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_form_validation(inventory_page, cart_page, checkout_page: CheckoutPage, first, last, zip_code, message):
    go_to_checkout(inventory_page, cart_page, ["sauce-labs-backpack"])
    checkout_page.fill_info(first, last, zip_code).continue_()
    expect(checkout_page.error).to_contain_text(message)


@pytest.mark.regression
def test_cancel_returns_to_cart(page: Page, inventory_page, cart_page, checkout_page: CheckoutPage):
    go_to_checkout(inventory_page, cart_page, ["sauce-labs-backpack"])
    checkout_page.cancel()
    expect(page).to_have_url(f"{config.SAUCE_URL}/cart.html")
    expect(cart_page.items).to_have_count(1)
