"""UI and UX smoke tests for the Shopify storefront."""

import pytest
from playwright.sync_api import expect


@pytest.mark.ui

def test_home_page_navigation_links(page, base_url):
    """Verify that primary header navigation links are visible and point to expected routes."""
    page.goto(base_url, wait_until="domcontentloaded")
    expect(page.get_by_role("link", name="Catalog", exact=True)).to_have_attribute("href", "/collections/all")
    expect(page.get_by_role("link", name="About Us", exact=True).first).to_be_visible()
    expect(page.locator("a[href='/cart']").first).to_be_visible()


@pytest.mark.ui

def test_catalog_navigation_from_home(page, base_url):
    """Verify that the catalog link opens the all-products collection."""
    page.goto(base_url, wait_until="domcontentloaded")
    page.get_by_role("link", name="Catalog", exact=True).first.click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(f"{base_url.rstrip('/')}/collections/all")
    expect(page.get_by_role("heading", name="Products", exact=True)).to_be_visible()


@pytest.mark.ui
@pytest.mark.parametrize("viewport", [(390, 844), (768, 1024)])

def test_responsive_layout_has_no_horizontal_overflow(page, base_url, viewport):
    """Verify that common mobile and tablet widths do not overflow horizontally."""
    page.set_viewport_size({"width": viewport[0], "height": viewport[1]})
    page.goto(base_url, wait_until="domcontentloaded")
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2")


@pytest.mark.ui

def test_about_us_navigation(page, base_url):
    """Verify that the About Us link opens a real storefront page."""
    page.goto(base_url, wait_until="domcontentloaded")
    page.get_by_role("link", name="About Us", exact=True).first.click()
    page.wait_for_load_state("domcontentloaded")
    assert "/pages/about-us" in page.url
    expect(page.locator("body")).to_contain_text("About Us")
