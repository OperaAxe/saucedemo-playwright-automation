"""Page object for the Shopify checkout boundary."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Validate that the cart can reach checkout without performing a purchase."""

    checkout_url_fragment = "/checkouts/"
    email_fields = "input[type='email'], input[name='email'], #email"
    shipping_fields = "input[name*='address'], input[name*='firstName'], input[name*='lastName']"

    def is_checkout_url(self) -> bool:
        """Return whether the current URL is a Shopify checkout URL."""
        return self.checkout_url_fragment in self.page.url

    def has_checkout_content(self) -> bool:
        """Return whether the page contains checkout-related content."""
        text = self.page.locator("body").inner_text().lower()
        return any(term in text for term in ("checkout", "contact information", "delivery", "shipping address"))

    def expect_checkout_boundary(self) -> None:
        """Assert that checkout navigation reached a Shopify checkout surface."""
        assert "/checkout" in self.page.url, f"Expected checkout URL, got {self.page.url}"
        assert self.has_checkout_content(), "Checkout page did not expose checkout-related content"

    def is_payment_form_visible(self) -> bool:
        """Return whether Shopify currently exposes a payment form."""
        return self.page.locator("input[name*='card'], iframe[title*='Card'], input[autocomplete='cc-number']").first.is_visible()
