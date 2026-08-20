# Module 05 — Locators that survive change

## Goal

Learn to choose locators from the user-facing contract instead of copying brittle DOM paths.

## Lesson

Playwright’s locator guidance prioritizes role, label, text, placeholder, alt text, title, and test ID locators. Each action re-resolves the locator against the current DOM, which helps when reactive applications re-render.

```python
page.get_by_role("button", name="Add to cart").click()
page.get_by_label("Email").fill("tester@example.com")
page.get_by_test_id("cart-count").to_have_text("1")
```

### Role and name

```python
page.get_by_role("heading", name="Products", exact=True)
page.get_by_role("link", name="Catalog", exact=True)
page.get_by_role("button", name="Submit", exact=False)
```

Use an accessible name when possible. It makes the test communicate what a user sees.

### Forms

```python
page.get_by_label("First name").fill("Christian")
page.get_by_placeholder("name@example.com").fill("tester@example.com")
```

A missing label may be a product quality issue. If you must use a CSS selector, document why the user-facing contract is unavailable.

### Scope and filtering

```python
product = page.get_by_role("listitem").filter(
    has=page.get_by_role("heading", name="Grey jacket")
)
product.get_by_role("button", name="Add to cart").click()
```

Filtering is more meaningful than a long descendant selector. If a locator matches two elements, inspect the page rather than hiding the ambiguity with `.first`.

### Test IDs

A test ID is an explicit agreement between developers and testers. It is not user-facing, but it is often very stable. Use it for dynamic widgets, repeated structures, and elements whose visible text changes by localization.

### CSS and XPath

CSS is reasonable for a stable attribute or a region boundary:

```python
page.locator("#cart input[name='updates[]']")
```

Avoid generated paths such as `div:nth-child(3) > div:nth-child(2) > button`. XPath is even more sensitive to structure and should be a last resort.

## Exercise

For each selector below, classify it as resilient, questionable, or brittle and rewrite the last two:

```python
page.locator("button").nth(2)
page.get_by_role("button", name="Add to cart")
page.locator("#product > div:nth-child(4) > form > input")
page.get_by_label("Email")
```

## Solution

The role and label locators are resilient when their accessible contracts are correct. The bare button locator is ambiguous. The generated CSS chain is brittle. Prefer a role/name or a stable form contract.

## Common mistakes

Do not use `get_by_text` for a button when `get_by_role` is available. Do not use a locator that matches the hidden mobile version when you mean the visible desktop version. Do not treat a test ID as permission to ignore the business meaning of the assertion.

## Checkpoint

You pass when you can defend each locator choice, diagnose strictness, and create a product-card locator by filtering a repeated collection.
