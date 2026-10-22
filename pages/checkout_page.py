import re

import allure
from playwright.sync_api import Locator

from .base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    @allure.step("Fill customer info: {first} / {last} / {zip_code}")
    def fill_info(self, first: str, last: str, zip_code: str):
        self.page.get_by_test_id("firstName").fill(first)
        self.page.get_by_test_id("lastName").fill(last)
        self.page.get_by_test_id("postalCode").fill(zip_code)
        return self

    @allure.step("Continue to the overview")
    def continue_(self):
        self.page.get_by_test_id("continue").click()
        return self

    @allure.step("Cancel checkout")
    def cancel(self):
        self.page.get_by_test_id("cancel").click()
        return self

    @allure.step("Finish the order")
    def finish(self):
        self.page.get_by_test_id("finish").click()
        return self

    @property
    def complete_header(self) -> Locator:
        return self.page.get_by_test_id("complete-header")

    def _money(self, test_id: str) -> float:
        text = self.page.get_by_test_id(test_id).inner_text()
        return float(re.search(r"\$([\d.]+)", text).group(1))

    @property
    def subtotal(self) -> float:
        return self._money("subtotal-label")

    @property
    def tax(self) -> float:
        return self._money("tax-label")

    @property
    def total(self) -> float:
        return self._money("total-label")
