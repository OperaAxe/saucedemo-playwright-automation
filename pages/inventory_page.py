"""Page object for the Shopify all-products collection."""

from __future__ import annotations

from dataclasses import dataclass
import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


@dataclass(frozen=True)
class ProductSummary:
    """Represent the product information exposed by a collection card."""

    name: str
    price: str
    href: str
    sold_out: bool


class InventoryPage(BasePage):
    """Interact with the storefront catalog, called inventory for test-suite compatibility."""

    product_links = "a[href*='/products/']"
    product_cards = "li.product, .product, .collection-product, a[href*='/products/']"

    def goto(self, path: str = "/collections/all") -> None:
        """Open the all-products collection."""
        super().goto(path)

    def product_count(self) -> int:
        """Return the number of product links rendered in the collection."""
        return self.page.locator(self.product_links).count()

    def product_names(self) -> list[str]:
        """Return normalized product names from the collection links."""
        names: list[str] = []
        for link in self.page.locator(self.product_links).all():
            text = " ".join(link.inner_text().split())
            if text and text not in names:
                names.append(text)
        return names

    def product_summaries(self) -> list[ProductSummary]:
        """Return product name, price, link, and sold-out state from each product link."""
        summaries: list[ProductSummary] = []
        seen: set[str] = set()
        for link in self.page.locator(self.product_links).all():
            href = link.get_attribute("href") or ""
            if href in seen:
                continue
            seen.add(href)
            text = " ".join(link.inner_text().split())
            price = next((part for part in text.split() if "£" in part), "")
            raw_name = re.sub(r"sold out", "", text, flags=re.IGNORECASE).replace(price, "").strip()
            words = raw_name.split()
            midpoint = len(words) // 2
            name = " ".join(words[:midpoint]) if midpoint and words[:midpoint] == words[midpoint:] else raw_name
            summaries.append(
                ProductSummary(
                    name=name,
                    price=price,
                    href=href,
                    sold_out="sold out" in text.lower(),
                )
            )
        return summaries

    def open_product(self, name: str) -> None:
        """Open a product by accessible link text."""
        self.page.get_by_role("link", name=name, exact=False).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def open_product_by_href(self, href: str) -> None:
        """Open a product by its Shopify path."""
        self.page.locator(f"a[href='{href}']").first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def expect_loaded(self) -> None:
        """Assert that the collection heading and at least one product are visible."""
        expect(self.page.get_by_role("heading", name="Products", exact=True)).to_be_visible()
        expect(self.page.locator(self.product_links).first).to_be_visible()
