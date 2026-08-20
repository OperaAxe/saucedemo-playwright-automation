"""Page object for the Shopify customer login and registration screens."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Interact with the storefront's customer login form."""

    email_input = "#customer_email"
    password_input = "#customer_password"
    submit_button = "#customer_login input[type='submit']"
    login_link = "#customer_login_link"
    register_link = "#customer_register_link"
    logout_link = "#customer_logout_link"

    def goto(self, path: str = "/account/login") -> None:
        """Open the customer login page."""
        super().goto(path)

    def is_login_form_visible(self) -> bool:
        """Return whether the customer login form is rendered."""
        return self.page.locator(self.email_input).is_visible() and self.page.locator(self.password_input).is_visible()

    def login(self, email: str, password: str) -> None:
        """Submit the customer login form with the supplied credentials."""
        self.page.locator(self.email_input).fill(email)
        self.page.locator(self.password_input).fill(password)
        self.page.locator(self.submit_button).last.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.ensure_storefront_available()

    def open_registration(self) -> None:
        """Open the customer registration page."""
        self.page.locator(self.register_link).first.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.ensure_storefront_available()

    def logout(self) -> None:
        """Log out through the shared header when the customer is authenticated."""
        self.page.locator(self.logout_link).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.ensure_storefront_available()

    def expect_login_form(self) -> None:
        """Assert that the login page exposes its required controls."""
        expect(self.page.locator(self.email_input)).to_be_visible()
        expect(self.page.locator(self.password_input)).to_be_visible()
        expect(self.page.locator(self.submit_button).last).to_be_visible()

    def error_text(self) -> str:
        """Return visible login error text, or an empty string when none exists."""
        error = self.page.locator(".errors, .form-error, [role='alert']").first
        return error.inner_text().strip() if error.is_visible() else ""
