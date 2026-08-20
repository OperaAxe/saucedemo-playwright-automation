"""Shared page-object functionality for the Sauce Demo Shopify theme."""

from __future__ import annotations

import time
from urllib.parse import urljoin

import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, expect


class BasePage:
    """Provide common navigation and header interactions for all page objects."""

    def __init__(self, page: Page, base_url: str) -> None:
        """Store the Playwright page and the configured storefront base URL."""
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"

    def url_for(self, path: str = "/") -> str:
        """Return an absolute storefront URL for a relative path."""
        return urljoin(self.base_url, path.lstrip("/"))

    def goto(self, path: str = "/") -> None:
        """Navigate to a storefront path with a small retry for transient network errors."""
        last_error: PlaywrightError | None = None
        for attempt in range(2):
            try:
                self.page.goto(self.url_for(path), wait_until="domcontentloaded", timeout=60000)
                self.ensure_storefront_available()
                return
            except PlaywrightError as error:
                last_error = error
                if attempt == 0:
                    time.sleep(1)
        if last_error is not None:
            raise last_error

    def ensure_storefront_available(self) -> None:
        """Skip the test when Shopify serves its connection-verification interstitial."""
        body = self.page.locator("body").inner_text(timeout=5000).lower()
        if "your connection needs to be verified before you can proceed" in body:
            pytest.skip("Shopify connection-verification interstitial blocked this browser run")

    def open_home(self) -> None:
        """Open the storefront home page from the shared header."""
        self.page.locator("a[href='/'], a[href='./']").first.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.ensure_storefront_available()

    def open_catalog(self) -> None:
        """Open the all-products collection."""
        self.page.locator("a[href='/collections/all']").first.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.ensure_storefront_available()

    def open_cart(self) -> None:
        """Open the Shopify cart page."""
        self.page.locator("a[href='/cart']").first.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.ensure_storefront_available()

    def is_authenticated(self) -> bool:
        """Return whether the header exposes the customer logout link."""
        return self.page.locator("#customer_logout_link").is_visible()

    def expect_authenticated_header(self) -> None:
        """Assert that the storefront exposes the authenticated customer state."""
        expect(self.page.locator("#customer_logout_link")).to_be_visible()
        expect(self.page.get_by_text("My Account", exact=True)).to_be_visible()

    def cart_count(self) -> int:
        """Return the numeric cart count when the theme exposes one."""
        count = self.page.locator(".cart-target .count, .cart-count, [data-cart-count]").first
        if not count.is_visible():
            return 0
        text = count.inner_text().strip()
        digits = "".join(character for character in text if character.isdigit())
        return int(digits or 0)

    def viewport_has_no_horizontal_overflow(self) -> bool:
        """Return whether the document fits within the current viewport width."""
        return self.page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2")
