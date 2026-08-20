"""Runnable Python lab for course Module 01."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """Represent a small product record used by the exercises."""

    name: str
    price: float
    available: bool = True


def available_under(products: list[Product], maximum: float) -> list[Product]:
    """Return available products priced at or below maximum."""
    return [
        product
        for product in products
        if product.available and product.price <= maximum
    ]


def main() -> None:
    """Print the available products in the exercise data set."""
    products = [
        Product("Grey jacket", 55.00),
        Product("Noir jacket", 60.00, available=False),
        Product("Striped top", 50.00),
    ]
    for product in available_under(products, 55.00):
        print(f"{product.name}: £{product.price:.2f}")


if __name__ == "__main__":
    main()
