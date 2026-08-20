"""Shared pytest fixtures for the Shopify Playwright suite."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from utils.test_data import CustomerCredentials, customer_credentials


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the configured storefront URL."""
    return os.getenv("BASE_URL", "https://sauce-demo.myshopify.com/").rstrip("/") + "/"


@pytest.fixture(scope="session")
def customer() -> CustomerCredentials:
    """Return optional Shopify customer credentials from the environment."""
    return customer_credentials()


@pytest.fixture
def page(context: BrowserContext):
    """Create a page and skip cleanly when Shopify blocks the test connection."""
    page = context.new_page()
    original_goto = page.goto

    def guarded_goto(*args, **kwargs):
        result = original_goto(*args, **kwargs)
        try:
            body = page.locator("body").inner_text(timeout=2000).lower()
        except Exception:
            return result
        if "your connection needs to be verified before you can proceed" in body:
            pytest.skip("Shopify connection-verification interstitial blocked this browser run")
        return result

    page.goto = guarded_goto
    yield page
    page.close()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Configure a consistent desktop context while allowing CI overrides."""
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 1000},
        "ignore_https_errors": True,
        "locale": "en-GB",
    }


@pytest.fixture(autouse=True)
def capture_failure_artifacts(request: pytest.FixtureRequest, page: Page):
    """Capture a screenshot and URL when a browser test fails."""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        output_dir = Path(os.getenv("ARTIFACT_DIR", "test-results"))
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = request.node.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")
        page.screenshot(path=str(output_dir / f"{safe_name}.png"), full_page=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Expose the test report to the automatic failure-artifact fixture."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """Return a login page object bound to the current browser page."""
    return LoginPage(page, base_url)


@pytest.fixture
def inventory_page(page: Page, base_url: str) -> InventoryPage:
    """Return a catalog page object bound to the current browser page."""
    return InventoryPage(page, base_url)


@pytest.fixture
def product_page(page: Page, base_url: str) -> ProductPage:
    """Return a product page object bound to the current browser page."""
    return ProductPage(page, base_url)


@pytest.fixture
def cart_page(page: Page, base_url: str) -> CartPage:
    """Return a cart page object bound to the current browser page."""
    return CartPage(page, base_url)


@pytest.fixture
def checkout_page(page: Page, base_url: str) -> CheckoutPage:
    """Return a checkout page object bound to the current browser page."""
    return CheckoutPage(page, base_url)


@pytest.fixture
def authenticated_page(page: Page, login_page: LoginPage, customer: CustomerCredentials) -> Page:
    """Log in with configured credentials and return the authenticated page."""
    if not customer.available:
        pytest.skip("Set SHOPIFY_TEST_EMAIL and SHOPIFY_TEST_PASSWORD to run authenticated tests")
    login_page.goto()
    login_page.login(customer.email, customer.password)
    page.goto(login_page.url_for("/"), wait_until="domcontentloaded")
    login_page.expect_authenticated_header()
    return page
