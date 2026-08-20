"""Tests for the Shopify product catalog."""

from utils.test_data import EXPECTED_PRODUCT_NAMES, PURCHASABLE_PRODUCT_PATH, SOLD_OUT_PRODUCT_PATH


def test_catalog_displays_products(inventory_page):
    """Verify that the all-products collection renders the expected catalog size."""
    inventory_page.goto()
    inventory_page.expect_loaded()
    assert inventory_page.product_count() >= 7


def test_catalog_contains_expected_product_names_and_prices(inventory_page):
    """Verify that the live collection exposes recognizable product names and prices."""
    inventory_page.goto()
    summaries = inventory_page.product_summaries()
    names = {summary.name for summary in summaries}
    assert EXPECTED_PRODUCT_NAMES.issubset(names)
    assert all(summary.price.startswith("£") for summary in summaries)


def test_catalog_product_links_are_unique(inventory_page):
    """Verify that each displayed product points to a distinct Shopify product path."""
    inventory_page.goto()
    summaries = inventory_page.product_summaries()
    hrefs = [summary.href for summary in summaries]
    assert len(hrefs) == len(set(hrefs))
    assert all("/products/" in href for href in hrefs)


def test_product_detail_navigation(inventory_page, product_page):
    """Verify that a catalog product opens a product detail page."""
    inventory_page.goto()
    inventory_page.open_product_by_href(PURCHASABLE_PRODUCT_PATH)
    product_page.expect_loaded()
    assert product_page.product_title().lower() == "grey jacket"
    assert "£55.00" in product_page.product_price()


def test_sold_out_product_is_marked_in_catalog(inventory_page):
    """Verify that a sold-out product is represented in the collection."""
    inventory_page.goto()
    sold_out = [item for item in inventory_page.product_summaries() if item.href.endswith(SOLD_OUT_PRODUCT_PATH.split("/products/")[-1])]
    assert sold_out and sold_out[0].sold_out
