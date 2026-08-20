# Module 01 — Python and environment setup

## Goal

Build the minimum Python foundation needed to read and write Playwright tests without feeling that the language is hiding the important ideas.

## You will learn

You will create a virtual environment, install packages, run a Python file, use variables and collections, define functions, handle simple errors, and write a small reusable test-data helper.

## Lesson

A repository is a project folder plus a repeatable environment. The environment matters because your computer may have several Python versions and projects may require different package versions. Create an isolated environment with `python -m venv .venv`, activate it, and install packages with `python -m pip`. Never commit `.venv`.

Create `course/labs/module01.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    price: float
    available: bool = True


def available_under(products: list[Product], maximum: float) -> list[Product]:
    """Return available products whose price is at most maximum."""
    return [
        product
        for product in products
        if product.available and product.price <= maximum
    ]


def main() -> None:
    products = [
        Product("Grey jacket", 55.00),
        Product("Noir jacket", 60.00, available=False),
        Product("Striped top", 50.00),
    ]
    affordable = available_under(products, 55.00)
    for product in affordable:
        print(f"{product.name}: £{product.price:.2f}")


if __name__ == "__main__":
    main()
```

Run it with `python course/labs/module01.py`. A function is a named piece of behavior. A dataclass gives a small object a clear shape. Type hints communicate intent; they do not replace runtime checks.

Use `pytest` for tests, but learn the language first with plain `assert`:

```python
from course.labs.module01 import Product, available_under


def test_available_under_filters_by_price_and_stock():
    products = [Product("A", 10), Product("B", 20, available=False)]
    assert [product.name for product in available_under(products, 10)] == ["A"]
```

## Exercise

Create a `Credentials` dataclass with `email` and `password` fields. Write `is_complete()` so it returns `True` only when both values are non-empty. Add tests for complete, empty-email, and empty-password cases.

## Solution

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    email: str
    password: str

    def is_complete(self) -> bool:
        return bool(self.email.strip() and self.password)
```

## Common mistakes

Do not install packages globally when a project environment is available. Do not name a file `pytest.py`, `playwright.py`, or `typing.py`; those names can shadow real packages. Do not catch every exception and return `False`, because that hides programming errors.

## Checkpoint

You pass this module when you can create `.venv`, activate it, run a Python file, explain a list and dictionary, write a typed function, and add three passing pytest checks.
