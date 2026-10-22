"""Base class of the Page Object pattern: wraps a Playwright Page, no assertions inside."""

import allure
from playwright.sync_api import Locator, Page

import config


class BasePage:
    path = ""  # relative URL of the page, set in subclasses

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Open the page")
    def open(self):
        self.page.goto(f"{config.SAUCE_URL}{self.path}")
        return self

    @property
    def title(self) -> Locator:
        return self.page.get_by_test_id("title")

    @property
    def error(self) -> Locator:
        return self.page.get_by_test_id("error")
