# UI-автотесты: Playwright + Pytest + Page Object

[![UI Tests](https://github.com/jekarevenko-byte/qa-ui-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/jekarevenko-byte/qa-ui-tests/actions/workflows/tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-report-8A2BE2)](https://jekarevenko-byte.github.io/qa-ui-tests/)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Playwright](https://img.shields.io/badge/Playwright-Python-2EAD33?logo=playwright&logoColor=white)

Проект UI-автоматизации на Python. Объекты тестирования — учебные сайты:
[saucedemo.com](https://www.saucedemo.com) (интернет-магазин: логин, каталог, корзина, оформление заказа) и
[the-internet.herokuapp.com](https://the-internet.herokuapp.com) (динамическая загрузка, чекбоксы, JS-диалоги, форма входа).

## Что показано

| Приём | Где смотреть |
|---|---|
| **Page Object**: локаторы и действия на странице отдельно от проверок | `pages/` |
| **Ожидания без `sleep`**: авто-ожидание Playwright, `expect(...)` с таймаутом, `wait_for_url` | `tests/test_the_internet.py`, `tests/conftest.py` |
| **Параметризация**: пользователи, неверные данные, сортировки, наборы товаров | `tests/test_login.py`, `test_inventory.py`, `test_checkout.py` |
| **Скриншот при падении** + трейс Playwright | `tests/conftest.py`, `pytest.ini` |
| **Allure**: шаги из Page Object, severity, epic/feature, вложения | `pages/`, `tests/` |
| **Маркеры**: `smoke`, `regression`, `negative`, по сайтам | `pytest.ini` |
| **CI**: smoke-гейт, полный прогон, отчёт на GitHub Pages | `.github/workflows/tests.yml` |

## Структура

```
qa-ui-tests/
├── config.py                  ← адреса сайтов (можно переопределить переменными окружения)
├── pages/
│   ├── base_page.py           ← общий класс страницы
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py            ← фикстуры, test-id атрибут, скриншот при падении
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_the_internet.py
├── pytest.ini
└── .github/workflows/tests.yml
```

## Запуск

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                                # все тесты, результаты Allure в allure-results/
pytest -m smoke                       # быстрый набор
pytest -m "saucedemo and negative"    # негативные сценарии магазина
pytest -n 2                           # параллельно, 2 процесса
pytest --headed --slowmo 300          # смотреть браузер
allure serve allure-results           # отчёт (нужны Allure CLI и Java)
```

При падении теста скриншот попадает в Allure-отчёт, а трейс лежит в `test-results/`. Открыть трейс:
`playwright show-trace test-results/<папка-теста>/trace.zip`.

## Как устроен Page Object

Страница хранит локаторы и действия, но **не содержит проверок** — `assert`/`expect` остаются в тестах:

```python
login_page.login("standard_user", config.PASSWORD)          # действие из Page Object
expect(page).to_have_url(f"{config.SAUCE_URL}/inventory.html")  # проверка в тесте
```

Элементы saucedemo размечены атрибутом `data-test`, поэтому в `conftest.py` он назначен тестовым идентификатором и локаторы пишутся как `page.get_by_test_id("login-button")`.

## CI

Workflow запускается на push и PR в `main`, по будням и вручную: ставит Chromium, прогоняет smoke, затем полный набор, собирает Allure-отчёт с историей прогонов и публикует его в ветку `gh-pages`. Однократно включите **Settings → Pages → Deploy from a branch → `gh-pages` / root**, отчёт откроется на https://jekarevenko-byte.github.io/qa-ui-tests/. При падении скриншоты и трейсы доступны как artifact `test-results-failures`.

## Замечания

- Сайты общедоступные и могут быть временно недоступны или медленны; тест `performance_glitch_user` намеренно ждёт дольше.
- Тесты не используют реальные данные: логины и пароль saucedemo публично указаны на странице входа.
