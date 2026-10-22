"""Test configuration. Override with environment variables if needed."""

import os

SAUCE_URL = os.getenv("SAUCE_URL", "https://www.saucedemo.com").rstrip("/")
INTERNET_URL = os.getenv("INTERNET_URL", "https://the-internet.herokuapp.com").rstrip("/")

PASSWORD = "secret_sauce"  # public demo password published on the saucedemo login page
