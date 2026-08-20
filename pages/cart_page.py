"""Page object for the Shopify cart page."""

from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CartPage(BasePage):
    """Inspect and mutate cart contents without submitting an order."""

    cart_root = "#cart, #your-shopping-cart"
    product_links = "#cart a[href*='/products/'], a[href*='/cart'] + a[href*='/products/']"
    quantity_inputs = "#cart input[name='updates[]'], #cart input[id^='updates_'], input[name^='updates']"
    remove_links = "#cart a[href*='/cart/change'], #cart a[href*='remove']"
    checkout_link = "#cart a.checkout, a[href='/checkout'], a.checkout"
    total_selectors = ".total, .subtotal, #cart-subtotal, [class*='subtotal']"

    def goto(self, path: str = "/cart") -> None:
        """Open the Shopify cart page."""
        super().goto(path)

    def is_empty(self) -> bool:
        """Return whether the cart page displays an empty-cart message."""
        body = self.page.locator("body").inner_text().lower()
        return any(
            phrase in body
            for phrase in (
                "cart is empty",
                "your cart is empty",
                "cart is currently empty",
            )
        )

    def item_names(self) -> list[str]:
        """Return distinct product names linked from the cart."""
        names: list[str] = []
        for link in self.page.locator("#cart a[href*='/products/']").all():
            name = " ".join(link.inner_text().split())
            if " - " in name:
                name = name.split(" - ", 1)[0].strip()
            if name and name not in names:
                names.append(name)
        return names

    def item_count(self) -> int:
        """Return the number of cart line items using product links as the stable signal."""
        return len(self.item_names())

    def quantities(self) -> list[int]:
        """Return line-item quantities from Shopify's cart update inputs."""
        values: list[int] = []
        for field in self.page.locator(self.quantity_inputs).all():
            value = field.input_value().strip()
            if value.isdigit():
                values.append(int(value))
        return values

    def total_text(self) -> str:
        """Return visible cart total text, falling back to the page body when needed."""
        for selector in self.total_selectors.split(", "):
            locator = self.page.locator(selector).first
            if locator.is_visible():
                return " ".join(locator.inner_text().split())
        body = self.page.locator("body").inner_text()
        match = re.search(r"(?:total|subtotal)[^\n]*", body, flags=re.IGNORECASE)
        return match.group(0).strip() if match else ""

    def update_quantity(self, index: int, quantity: int) -> None:
        """Update a line-item quantity and submit the cart form."""
        fields = self.page.locator(self.quantity_inputs)
        fields.nth(index).fill(str(quantity))
        update = self.page.locator("#cart input[name='update'], #cart button[name='update'], input[value='Update']").first
        if update.is_visible():
            update.click()
        else:
            fields.nth(index).press("Enter")
        self.page.wait_for_load_state("domcontentloaded")

    def remove_item(self, index: int = 0) -> None:
        """Remove a line item through the theme's cart-change link."""
        link = self.page.locator(self.remove_links).nth(index)
        if link.is_visible():
            link.click()
        else:
            fields = self.page.locator(self.quantity_inputs)
            if not fields.nth(index).is_visible():
                raise AssertionError("The cart did not expose a removable line item")
            fields.nth(index).fill("0")
            update = self.page.locator("#cart input[name='update'], #cart button[name='update'], input[value='Update']").first
            if update.is_visible():
                update.click()
            else:
                fields.nth(index).press("Enter")
        self.page.wait_for_load_state("domcontentloaded")

    def proceed_to_checkout(self) -> None:
        """Open Shopify checkout without submitting payment or an order."""
        expect(self.page.locator(self.checkout_link).first).to_be_visible()
        self.page.locator(self.checkout_link).first.click()
        self.page.wait_for_load_state("domcontentloaded")
