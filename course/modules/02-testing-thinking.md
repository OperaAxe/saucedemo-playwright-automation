# Module 02 — Testing thinking before Playwright

## Goal

Learn to design a useful test before touching a locator.

## You will learn

You will turn a requirement into a test charter, choose the cheapest suitable test layer, separate happy paths from risks, and write behavior-oriented test names.

## Lesson

Start with a behavior, not a button. For “a customer can add a product to the cart,” identify the precondition, action, and oracle:

- Starting state: catalog is available and cart is empty.
- Action: customer chooses an in-stock product and adds it.
- Oracle: cart contains the product with quantity one and a visible total.

A test charter describes what you intend to learn or prove. It is useful before the test becomes code because it exposes missing decisions.

```text
Charter: Add an in-stock product to an empty cart
Risk: Product selection may add the wrong variant or fail silently
Setup: Fresh browser context, catalog loaded, empty cart
Action: Open Grey jacket and activate Add to cart
Evidence: Cart URL, product name, quantity, total
Safety: Stop before checkout submission
```

Use the test pyramid as a decision aid. Pure calculations belong in unit tests. HTTP behavior belongs in API tests. A critical user journey belongs in a browser test. An exploratory question may be handled by an agent first, but the final regression should become deterministic code when the behavior is stable.

Good names describe behavior:

```python
def test_customer_sees_the_selected_product_in_the_cart(page):
    ...
```

Weak names describe implementation:

```python
def test_click_button_2(page):
    ...
```

### Positive, negative, and boundary cases

For a login form, consider valid credentials, invalid password, empty email, malformed email, locked account, and network failure. Do not create every possible combination immediately. Prioritize risks, then expand with evidence.

### Invariants

An invariant remains true across actions. Examples include: cart quantity never becomes negative; a disabled button cannot be submitted; a product link points to a product route; payment fields are not submitted by a safe test.

## Exercise

Write charters for three flows: browsing the catalog, removing a product from the cart, and opening the About Us page. Each charter must include risk, setup, action, oracle, evidence, and safety boundary.

## Solution pattern

```text
Charter: Remove the only cart line
Risk: Remove control may update quantity but leave stale UI state
Setup: Add one known product in a fresh context
Action: Activate the remove/quantity-zero control
Oracle: Empty-cart state is visible and the product row is absent
Evidence: Cart URL, empty message, row count
Safety: Do not proceed to checkout
```

## Common mistakes

Do not confuse “the click succeeded” with “the feature worked.” Do not write a browser test for every validation rule if a unit or API test can prove it more directly. Do not use a random assertion such as “body is not empty”; assert the state that matters to a user.

## Checkpoint

You pass when you can write a charter before code, choose a test layer with a reason, and define an observable oracle for each action.
