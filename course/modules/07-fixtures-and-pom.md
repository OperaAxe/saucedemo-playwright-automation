# Module 07 — Fixtures and Page Object Model

## Goal

Move from isolated scripts to a test framework that stays readable as coverage grows.

## Lesson

A fixture creates reliable context and makes dependencies visible through function arguments. A page object groups selectors and actions around a page or reusable component.

```python
# tests/conftest.py
import os
import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://sauce-demo.myshopify.com/")
```

```python
# pages/catalog_page.py
from playwright.sync_api import Page, expect


class CatalogPage:
    """Model the all-products collection."""

    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Products", exact=True)
        self.products = page.locator("a[href*='/products/']")

    def open(self, base_url: str) -> None:
        self.page.goto(f"{base_url.rstrip('/')}/collections/all")

    def expect_loaded(self) -> None:
        expect(self.heading).to_be_visible()
        expect(self.products.first).to_be_visible()
```

```python
# tests/test_catalog.py
from pages.catalog_page import CatalogPage


def test_catalog_has_products(page, base_url):
    catalog = CatalogPage(page)
    catalog.open(base_url)
    catalog.expect_loaded()
```

### Scope decisions

Use function-scoped browser state when tests mutate cart or account state. Use session scope for immutable configuration. A wide-scope mutable context creates order-dependent tests.

### Parametrization

```python
import pytest


@pytest.mark.parametrize("width,height", [(390, 844), (1280, 720)])
def test_catalog_renders_at_viewport(page, base_url, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(base_url)
    assert page.locator("body").bounding_box()["width"] <= width
```

### Components

A shared `Header` object can expose `open_catalog`, `open_cart`, and `open_account`. A `ProductCard` object can expose `name`, `price`, and `open`. Create a component object when repeated behavior or a meaningful boundary justifies it.

### POM boundaries

A page object should not know every business decision in the test. It should expose focused operations and state. Tests decide whether the resulting cart is correct.

## Exercise

Take one raw test from `tests/test_inventory.py`. Create or use a page object for navigation and product discovery. Refactor the test so the selectors are not visible in the test body. Add a fixture that returns the page object.

## Solution pattern

```python
@pytest.fixture
def catalog_page(page, base_url):
    catalog = CatalogPage(page)
    catalog.open(base_url)
    catalog.expect_loaded()
    return catalog


def test_product_names_are_unique(catalog_page):
    names = catalog_page.product_names()
    assert len(names) == len(set(names))
```

## Common mistakes

Do not create a “god page object” that performs login, shopping, checkout, and reporting. Do not hide assertions inside every method. Do not use module- or session-scoped cart state unless you deliberately reset it.

## Checkpoint

You pass when you can write a fixture, choose its scope, parametrize a test, create a page object, and keep the test body focused on behavior.
