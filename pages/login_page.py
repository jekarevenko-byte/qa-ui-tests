import allure
from playwright.sync_api import Locator

from .base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    @property
    def username(self) -> Locator:
        return self.page.get_by_test_id("username")

    @property
    def password(self) -> Locator:
        return self.page.get_by_test_id("password")

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_test_id("login-button")

    @allure.step("Log in as '{username}'")
    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        return self
