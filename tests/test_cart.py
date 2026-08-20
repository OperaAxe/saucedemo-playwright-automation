"""Tests for Shopify cart behavior."""

from pages.product_page import ProductPage
from utils.test_data import PURCHASABLE_PRODUCT_PATH, SECOND_PURCHASABLE_PRODUCT_PATH


def add_product(page, base_url: str, path: str) -> None:
    """Add a product to the cart through its detail page."""
    product = ProductPage(page, base_url)
    product.goto(path)
    product.add_to_cart()


def test_cart_is_empty_at_start(cart_page):
    """Verify that a fresh browser context starts with an empty cart."""
    cart_page.goto()
    assert cart_page.is_empty()


def test_add_one_product_to_cart(page, base_url, cart_page):
    """Verify that a purchasable product appears in the cart after adding it."""
    add_product(page, base_url, PURCHASABLE_PRODUCT_PATH)
    cart_page.goto()
    assert "Grey jacket" in cart_page.item_names()
    assert cart_page.total_text()


def test_add_multiple_products_to_cart(page, base_url, cart_page):
    """Verify that two distinct products can coexist in the cart."""
    add_product(page, base_url, PURCHASABLE_PRODUCT_PATH)
    add_product(page, base_url, SECOND_PURCHASABLE_PRODUCT_PATH)
    cart_page.goto()
    names = cart_page.item_names()
    assert "Grey jacket" in names
    assert "Noir jacket" in names
    assert cart_page.item_count() >= 2


def test_cart_exposes_quantity_controls(page, base_url, cart_page):
    """Verify that Shopify exposes a quantity value for a cart line item."""
    add_product(page, base_url, PURCHASABLE_PRODUCT_PATH)
    cart_page.goto()
    quantities = cart_page.quantities()
    assert quantities and quantities[0] >= 1


def test_remove_product_from_cart(page, base_url, cart_page):
    """Verify that the first cart line item can be removed."""
    add_product(page, base_url, PURCHASABLE_PRODUCT_PATH)
    cart_page.goto()
    cart_page.remove_item()
    assert cart_page.is_empty()
