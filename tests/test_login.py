"""Tests for Shopify customer authentication and account entry points."""

import pytest
from playwright.sync_api import expect

from utils.test_data import CustomerCredentials


@pytest.mark.login

def test_customer_login_form_is_available(login_page):
    """Verify that the storefront exposes customer email and password fields."""
    login_page.goto()
    login_page.expect_login_form()


@pytest.mark.login

def test_invalid_customer_login_is_rejected(login_page):
    """Verify that obviously invalid customer credentials do not authenticate."""
    login_page.goto()
    login_page.login("not-a-real-customer@example.com", "definitely-not-valid")
    assert "/account/login" in login_page.page.url
    assert not login_page.is_authenticated()


@pytest.mark.login

def test_registration_page_is_available(login_page):
    """Verify that a visitor can reach the Shopify customer registration form."""
    login_page.goto()
    login_page.open_registration()
    expect(login_page.page.locator("input#first_name")).to_be_visible()
    expect(login_page.page.locator("input#last_name")).to_be_visible()
    expect(login_page.page.locator("input#email")).to_be_visible()
    expect(login_page.page.locator("input#password")).to_be_visible()


@pytest.mark.authenticated
@pytest.mark.login

def test_valid_customer_login(authenticated_page, login_page):
    """Verify that configured Shopify customer credentials produce an authenticated header."""
    authenticated_page.goto(login_page.url_for("/"), wait_until="domcontentloaded")
    login_page.expect_authenticated_header()


@pytest.mark.authenticated
@pytest.mark.login

def test_customer_can_log_out(authenticated_page, login_page):
    """Verify that an authenticated customer can end the session."""
    authenticated_page.goto(login_page.url_for("/"), wait_until="domcontentloaded")
    login_page.logout()
    assert not login_page.is_authenticated()
    login_page.expect_login_form()
