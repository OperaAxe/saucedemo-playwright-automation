"""Tests for the Module 01 Python lab."""

from course.labs.module01 import Product, available_under


def test_available_under_filters_price_and_stock():
    products = [Product("A", 10), Product("B", 20, available=False)]
    assert [product.name for product in available_under(products, 10)] == ["A"]


def test_empty_product_list_returns_empty_list():
    assert available_under([], 10) == []
