"""Safe tests for the Shopify checkout boundary."""

from pages.product_page import ProductPage
from utils.test_data import PURCHASABLE_PRODUCT_PATH


def test_checkout_link_is_not_available_for_empty_cart(cart_page):
    """Verify that an empty cart does not expose a usable checkout action."""
    cart_page.goto()
    assert cart_page.is_empty()
    assert not cart_page.page.locator(cart_page.checkout_link).first.is_visible()


def test_cart_can_reach_checkout_boundary(page, base_url, cart_page, checkout_page):
    """Verify checkout entry without filling shipping or payment fields."""
    product = ProductPage(page, base_url)
    product.goto(PURCHASABLE_PRODUCT_PATH)
    product.add_to_cart()
    cart_page.goto()
    cart_page.proceed_to_checkout()
    checkout_page.expect_checkout_boundary()
    assert not checkout_page.is_payment_form_visible()
