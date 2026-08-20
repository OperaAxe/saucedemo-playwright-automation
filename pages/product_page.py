"""Page object for Shopify product detail pages."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class ProductPage(BasePage):
    """Interact with a Shopify product detail page."""

    title = "h1[itemprop='name'], .product_name, .product-title"
    price = "#product-price, .product-price"
    variant_select = "#product-select-option-0, #product-select"
    add_to_cart_button = "#add"
    product_form = "#product-form"

    def product_title(self) -> str:
        """Return the visible product title."""
        return self.page.locator(self.title).first.inner_text().strip()

    def product_price(self) -> str:
        """Return the visible product price."""
        return self.page.locator(self.price).first.inner_text().strip()

    def select_variant(self, label: str) -> None:
        """Select a product variant when the page exposes a select control."""
        selector = self.page.locator(self.variant_select).first
        if selector.is_visible() and selector.get_attribute("id") == "product-select-option-0":
            selector.select_option(label=label)

    def add_to_cart(self) -> None:
        """Add the current product to the cart and wait for Shopify's cart response."""
        with self.page.expect_response(lambda response: "/cart/add" in response.url, timeout=30000):
            self.page.locator(self.add_to_cart_button).click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_load_state("domcontentloaded")

    def is_sold_out(self) -> bool:
        """Return whether the product page exposes sold-out text instead of a purchasable form."""
        body = self.page.locator("body").inner_text().lower()
        return "sold out" in body and not self.page.locator(self.add_to_cart_button).is_visible()

    def expect_loaded(self) -> None:
        """Assert that the product detail page exposes a title and price."""
        expect(self.page.locator(self.title).first).to_be_visible()
        expect(self.page.locator(self.price).first).to_be_visible()
