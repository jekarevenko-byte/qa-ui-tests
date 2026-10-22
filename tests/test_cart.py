import allure
import pytest
from playwright.sync_api import Page, expect

import config
from pages import CartPage, InventoryPage

pytestmark = [pytest.mark.saucedemo, allure.epic("Sauce Demo"), allure.feature("Cart")]

PRODUCTS = {
    "sauce-labs-backpack": "Sauce Labs Backpack",
    "sauce-labs-bike-light": "Sauce Labs Bike Light",
    "sauce-labs-onesie": "Sauce Labs Onesie",
}


@pytest.mark.smoke
@pytest.mark.parametrize("slugs", [["sauce-labs-backpack"], list(PRODUCTS)], ids=["one-item", "three-items"])
def test_cart_shows_added_products(inventory_page: InventoryPage, cart_page: CartPage, slugs):
    for slug in slugs:
        inventory_page.add_to_cart(slug)
    inventory_page.open_cart()
    expect(cart_page.items).to_have_count(len(slugs))
    assert sorted(cart_page.names()) == sorted(PRODUCTS[s] for s in slugs)


@pytest.mark.regression
def test_item_can_be_removed_from_cart(inventory_page: InventoryPage, cart_page: CartPage):
    inventory_page.add_to_cart("sauce-labs-backpack").add_to_cart("sauce-labs-onesie").open_cart()
    cart_page.remove("sauce-labs-backpack")
    expect(cart_page.items).to_have_count(1)
    assert cart_page.names() == ["Sauce Labs Onesie"]


@pytest.mark.regression
def test_cart_content_survives_navigation(page: Page, inventory_page: InventoryPage, cart_page: CartPage):
    inventory_page.add_to_cart("sauce-labs-backpack").open_cart()
    cart_page.continue_shopping()
    expect(page).to_have_url(f"{config.SAUCE_URL}/inventory.html")
    expect(inventory_page.cart_badge).to_have_text("1")


@pytest.mark.regression
def test_empty_cart_has_no_items(inventory_page: InventoryPage, cart_page: CartPage):
    inventory_page.open_cart()
    expect(cart_page.items).to_have_count(0)
