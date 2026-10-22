import allure
import pytest
from playwright.sync_api import expect

from pages import InventoryPage

pytestmark = [pytest.mark.saucedemo, allure.epic("Sauce Demo"), allure.feature("Inventory")]

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"


@pytest.mark.smoke
def test_six_products_are_displayed(inventory_page: InventoryPage):
    expect(inventory_page.items).to_have_count(6)


@pytest.mark.regression
@pytest.mark.parametrize(
    "option, key, reverse",
    [("az", "name", False), ("za", "name", True), ("lohi", "price", False), ("hilo", "price", True)],
    ids=["name-asc", "name-desc", "price-low-high", "price-high-low"],
)
def test_sorting(inventory_page: InventoryPage, option, key, reverse):
    inventory_page.sort_by(option)
    values = inventory_page.names() if key == "name" else inventory_page.prices()
    assert values == sorted(values, reverse=reverse), f"Not sorted by {key}: {values}"


@pytest.mark.smoke
def test_adding_product_updates_cart_badge(inventory_page: InventoryPage):
    expect(inventory_page.cart_badge).to_have_count(0)
    inventory_page.add_to_cart(BACKPACK)
    expect(inventory_page.cart_badge).to_have_text("1")
    inventory_page.add_to_cart(BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_have_text("2")


@pytest.mark.regression
def test_removing_product_updates_cart_badge(inventory_page: InventoryPage):
    inventory_page.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)
    inventory_page.remove_from_cart(BACKPACK)
    expect(inventory_page.cart_badge).to_have_text("1")
    inventory_page.remove_from_cart(BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_have_count(0)


@pytest.mark.regression
def test_all_prices_are_positive(inventory_page: InventoryPage):
    prices = inventory_page.prices()
    assert len(prices) == 6 and all(p > 0 for p in prices)
