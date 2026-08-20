# Sauce Demo Shopify Playwright Automation

A maintainable end-to-end test suite for the current [Sauce Demo Shopify storefront](https://sauce-demo.myshopify.com/), built with Python, Playwright, pytest, and the Page Object Model.

> This repository targets the Shopify storefront at `sauce-demo.myshopify.com`. It does not target the separate classic SauceDemo application at `saucedemo.com`, so the classic `standard_user / secret_sauce` accounts and inventory selectors are intentionally not used here.

## What the suite covers

The suite validates the behavior that exists on the current storefront. It checks customer login and registration entry points, catalog rendering, product detail pages, sold-out product representation, add-to-cart behavior, cart quantities and removal, checkout-boundary navigation, shared navigation, and responsive layouts.

Checkout tests deliberately stop at the Shopify checkout boundary. They do not fill payment fields, submit an order, or create a financial transaction.

| Area | Coverage |
|---|---|
| Customer account | Login form, invalid login rejection, registration form, optional authenticated login, logout |
| Catalog | Product count, product names and prices, unique product links, product detail navigation, sold-out state |
| Cart | Empty state, one product, multiple products, quantities, removal, totals |
| Checkout | Empty-cart checkout behavior and safe cart-to-checkout boundary |
| UI/UX | Header navigation, catalog routing, mobile/tablet overflow, About Us navigation |

## Project structure

```text
saucedemo-playwright-automation/
├── .github/workflows/playwright.yml
├── docs/superpowers/specs/2026-08-20-saucedemo-shopify-automation-design.md
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── order_confirmation_page.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_ui_ux.py
├── utils/
│   ├── __init__.py
│   └── test_data.py
├── requirements.txt
├── pytest.ini
└── .gitignore
```

## Local setup

Use Python 3.11 or newer. Create and activate a virtual environment, install the dependencies, and install the Chromium browser used by the tests:

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate      # Windows PowerShell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run the tests

The default command runs the complete safe suite. Authenticated tests are skipped unless both credential environment variables are present.

```bash
pytest
```

Useful focused commands are:

```bash
pytest tests/test_inventory.py -v
pytest tests/test_cart.py -v
pytest tests/test_ui_ux.py -v
pytest -m "not authenticated" -v
pytest -m authenticated -v
```

To run with the created Shopify customer account locally, provide the credentials through environment variables rather than committing them to the repository:

```bash
export SHOPIFY_TEST_EMAIL="your-test-email@example.com"
export SHOPIFY_TEST_PASSWORD="your-test-password"
pytest -m authenticated -v
```

The base URL can also be overridden for a compatible staging environment:

```bash
export BASE_URL="https://sauce-demo.myshopify.com/"
pytest -v
```

## Reports and debugging

Pytest is configured to retain Playwright traces on failure and capture screenshots into `test-results/`. HTML reports can be generated with:

```bash
pytest --html=reports/report.html --self-contained-html
```

The artifact directories are ignored by Git so test output is not accidentally committed. If Shopify presents the full-page `Your connection needs to be verified before you can proceed` interstitial, the page fixture skips that test with an explicit reason rather than reporting a misleading selector failure. This protects CI results from transient external anti-automation conditions.

## Continuous integration

GitHub Actions runs the safe suite on every push to `main` and every pull request targeting `main`. The workflow installs Python dependencies and Chromium, runs the tests, and uploads reports and failure artifacts. Authenticated tests run only when the repository has `SHOPIFY_TEST_EMAIL` and `SHOPIFY_TEST_PASSWORD` Actions secrets configured.

## Design notes

The live storefront is a Shopify theme with customer-account pages, collection pages, product forms, and Shopify cart/checkout routes. It is not the classic SauceDemo application. The design record in `docs/superpowers/specs/` documents this decision and the selector strategy.

## License

This project is provided for educational and portfolio use. The Sauce Demo storefront and its assets remain the property of their respective owners.


## Complete Playwright course

This repository now includes a from-scratch course that takes you from Python foundations to agentic testing:

- [`PLAYWRIGHT_PYTHON_AGENTIC_TESTING_TEXTBOOK.md`](PLAYWRIGHT_PYTHON_AGENTIC_TESTING_TEXTBOOK.md) — the standalone textbook.
- [`course/README.md`](course/README.md) — the hands-on curriculum and navigation map.
- [`course/modules/`](course/modules/) — 13 sequential modules with lessons, exercises, solutions, and checkpoints.
- [`course/labs/`](course/labs/) — runnable Python and browser-lab exercises.
- [`course/agentic/`](course/agentic/) — safe agent policy, exploration prompt, and structured output schema.
- [`course/projects/capstone-review-template.md`](course/projects/capstone-review-template.md) — final review checklist.
- [`course-research-notes.md`](course-research-notes.md) — verified official references used to design the course.

The course distinguishes deterministic Playwright proof from AI-assisted exploration. Agents may propose scenarios, inspect artifacts, and help triage failures, but they must not autonomously enter payment details, submit orders, expose secrets, modify production data, or push unreviewed code.
