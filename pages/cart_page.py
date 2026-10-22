import allure
from playwright.sync_api import Locator

from .base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    @property
    def items(self) -> Locator:
        return self.page.get_by_test_id("inventory-item")

    def names(self) -> list[str]:
        return self.page.get_by_test_id("inventory-item-name").all_inner_texts()

    @allure.step("Remove '{slug}' from the cart page")
    def remove(self, slug: str):
        self.page.get_by_test_id(f"remove-{slug}").click()
        return self

    @allure.step("Click Checkout")
    def checkout(self):
        self.page.get_by_test_id("checkout").click()
        return self

    @allure.step("Continue shopping")
    def continue_shopping(self):
        self.page.get_by_test_id("continue-shopping").click()
        return self
