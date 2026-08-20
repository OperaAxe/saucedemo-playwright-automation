# Module 13 — Capstone: build a trustworthy Shopify framework

## Goal

Combine the course into a complete, maintainable project that proves user behavior without unsafe transactions.

## Project brief

Build a Python Playwright suite for `https://sauce-demo.myshopify.com/`. The suite must cover the current storefront behavior rather than the separate classic SauceDemo application.

Required coverage:

- home and catalog navigation;
- product count, names, prices, links, and sold-out representation;
- product detail and add-to-cart behavior;
- empty cart, single item, multiple items, removal, quantity, and total;
- checkout-boundary navigation without entering payment or submitting an order;
- responsive rendering at mobile, tablet, and desktop sizes;
- optional customer login using environment-backed credentials;
- artifacts on failure;
- GitHub Actions on push and pull request;
- a documented agentic-testing policy and read-only exploration prompt.

## Suggested architecture

```text
pages/
  base_page.py
  login_page.py
  inventory_page.py
  product_page.py
  cart_page.py
  checkout_page.py
  order_confirmation_page.py

tests/
  conftest.py
  test_login.py
  test_inventory.py
  test_cart.py
  test_checkout.py
  test_ui_ux.py

utils/
  test_data.py

course/agentic/
  policy.md
  exploration_prompt.md
  triage_schema.json
```

### Milestone 1 — Safe smoke

Create the base URL fixture, open the home page, and prove Catalog and Cart navigation. The tests must run without credentials.

### Milestone 2 — Page objects

Move selectors and reusable actions into page objects. The tests should read like workflows. Do not put passwords in page objects.

### Milestone 3 — State and cart

Use fresh contexts or cleanup to ensure cart tests do not depend on order. Prove that product additions result in cart state. Stop before payment.

### Milestone 4 — Debugging and resilience

Enable screenshots and traces on failure. Add an explicit guard for the storefront’s external connection-verification interstitial so a blocked environment is reported as a skip with a reason rather than a false selector failure.

### Milestone 5 — CI

Run safe tests on push and pull request. Run authenticated tests only when credentials are deliberately configured. Upload reports and browser artifacts with `if: always()`.

### Milestone 6 — Agentic layer

Write a policy that allows read-only catalog exploration and forbids login, checkout, payment, order creation, account deletion, and direct pushes. Define JSON output with observations, evidence, confidence, and human-review status.

## Acceptance rubric

| Area | Pass condition |
|---|---|
| Python | Code is importable, typed where useful, and formatted clearly |
| Playwright | Locators follow a user-facing priority and assertions are meaningful |
| pytest | Fixtures are explicit, scoped deliberately, and parametrization is useful |
| POM | Selectors are not duplicated throughout tests |
| Isolation | Tests do not depend on execution order or leaked cart state |
| Safety | No secrets, payment data, or real orders are committed or submitted |
| CI | Clean runner installs dependencies and executes the safe suite |
| Debugging | Failure produces actionable artifacts |
| Agentic testing | Agent scope, evidence, stop conditions, and human gates are documented |
| Documentation | Another learner can set up and run the project |

## Final review questions

Before calling the capstone complete, answer these questions in `course/projects/capstone-review.md`:

1. Which tests would be cheaper as unit or API tests?
2. Which locator is most likely to break and why?
3. How does a fresh context protect test isolation?
4. What happens if Shopify presents a verification page?
5. Which CI artifacts are uploaded after a failure?
6. Which actions may the agent perform, and which require human approval?
7. How would you validate an agent-proposed locator?
8. What is the first command you would run when CI fails but local tests pass?

## Final checkpoint

You pass the capstone when the safe suite is green or explicitly skips only for documented external blocking, CI completes successfully, no credential scan finds secrets, and a reviewer can understand both the deterministic tests and the agentic safety boundary.
