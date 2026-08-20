"""Reusable data helpers for the Sauce Demo Shopify test suite."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerCredentials:
    """Represent optional Shopify customer credentials supplied by the environment."""

    email: str
    password: str

    @property
    def available(self) -> bool:
        """Return whether both credential fields are populated."""
        return bool(self.email and self.password)


def customer_credentials() -> CustomerCredentials:
    """Read Shopify test credentials from environment variables."""
    return CustomerCredentials(
        email=os.getenv("SHOPIFY_TEST_EMAIL", "").strip(),
        password=os.getenv("SHOPIFY_TEST_PASSWORD", ""),
    )


EXPECTED_PRODUCT_NAMES = {
    "Black heels",
    "Bronze sandals",
    "Brown Shades",
    "Grey jacket",
    "Noir jacket",
    "Striped top",
    "White sandals",
}

PURCHASABLE_PRODUCT_PATH = "/collections/all/products/grey-jacket"
SECOND_PURCHASABLE_PRODUCT_PATH = "/collections/all/products/noir-jacket"
SOLD_OUT_PRODUCT_PATH = "/collections/all/products/brown-shades"
