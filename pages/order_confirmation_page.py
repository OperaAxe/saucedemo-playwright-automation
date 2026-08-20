"""Read-only helpers for a Shopify order confirmation page."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class OrderConfirmationPage(BasePage):
    """Inspect an order-confirmation page when a test environment provides one."""

    confirmation_markers = (
        "thank you",
        "order confirmed",
        "order #",
        "thank you for your purchase",
    )

    def is_confirmed(self) -> bool:
        """Return whether the page contains a common confirmation marker."""
        body = self.page.locator("body").inner_text().lower()
        return any(marker in body for marker in self.confirmation_markers)

    def confirmation_text(self) -> str:
        """Return the visible confirmation text for diagnostic use."""
        return " ".join(self.page.locator("body").inner_text().split())

    def expect_confirmed(self) -> None:
        """Assert that the page contains a confirmation marker."""
        expect(self.page.locator("body")).to_contain_text("thank you", ignore_case=True)
