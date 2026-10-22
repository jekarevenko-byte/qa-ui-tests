import allure
from playwright.sync_api import Locator

from .base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    @property
    def items(self) -> Locator:
        return self.page.get_by_test_id("inventory-item")

    @property
    def cart_badge(self) -> Locator:
        return self.page.get_by_test_id("shopping-cart-badge")

    @property
    def cart_link(self) -> Locator:
        return self.page.get_by_test_id("shopping-cart-link")

    @property
    def sort_select(self) -> Locator:
        return self.page.get_by_test_id("product-sort-container")

    def names(self) -> list[str]:
        return self.page.get_by_test_id("inventory-item-name").all_inner_texts()

    def prices(self) -> list[float]:
        return [float(t.lstrip("$")) for t in self.page.get_by_test_id("inventory-item-price").all_inner_texts()]

    @allure.step("Sort products by '{option}'")
    def sort_by(self, option: str):
        """option: az | za | lohi | hilo"""
        self.sort_select.select_option(option)
        return self

    @allure.step("Add '{slug}' to cart")
    def add_to_cart(self, slug: str):
        self.page.get_by_test_id(f"add-to-cart-{slug}").click()
        return self

    @allure.step("Remove '{slug}' from cart")
    def remove_from_cart(self, slug: str):
        self.page.get_by_test_id(f"remove-{slug}").click()
        return self

    @allure.step("Open cart")
    def open_cart(self):
        self.cart_link.click()
        return self

    @allure.step("Log out via the side menu")
    def logout(self):
        self.page.get_by_role("button", name="Open Menu").click()
        self.page.get_by_test_id("logout-sidebar-link").click()
        return self
