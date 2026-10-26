# Sauce Demo Shopify — Playwright + Python

[![CI](https://github.com/OperaAxe/saucedemo-playwright-automation/actions/workflows/playwright.yml/badge.svg)](https://github.com/OperaAxe/saucedemo-playwright-automation/actions/workflows/playwright.yml)

This repository contains browser tests for the [Sauce Demo Shopify storefront](https://sauce-demo.myshopify.com/) and a separate hands-on Playwright course. The suite is still being developed.

**Site distinction:** the target is `sauce-demo.myshopify.com`, not the classic [SauceDemo application](https://www.saucedemo.com/). The two sites have different pages, accounts, and selectors.

## What the suite covers

- Customer login and registration entry points
- Product catalogue, detail pages, and sold-out states
- Cart contents, quantities, totals, and removal
- Navigation and responsive layout checks
- Safe navigation to the checkout boundary

Tests stop before payment details are entered or an order is submitted. Authenticated tests are skipped unless the required test-account credentials are supplied through environment variables.

## Run locally

Requires Python 3.11 or newer.

```bash
python -m venv .venv
```

Activate the environment in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies and run the tests:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
pytest
```

Useful selections:

```bash
pytest tests/test_inventory.py -v
pytest tests/test_cart.py -v
pytest tests/test_ui_ux.py -v
pytest -m "not authenticated" -v
pytest -m authenticated -v
```

To run the authenticated cases, provide the credentials through environment variables rather than committing them:

```bash
export SHOPIFY_TEST_EMAIL="your-test-email@example.com"
export SHOPIFY_TEST_PASSWORD="your-test-password"
pytest -m authenticated -v
```

On Windows PowerShell, use `$env:SHOPIFY_TEST_EMAIL` and `$env:SHOPIFY_TEST_PASSWORD` to set those variables for the current session.

## Reports and CI

Playwright traces are retained on failure and screenshots are saved under `test-results/`. An HTML report can be generated with:

```bash
mkdir -p reports
pytest --html=reports/report.html --self-contained-html
```

GitHub Actions runs the safe suite on pushes and pull requests. Authenticated tests need `SHOPIFY_TEST_EMAIL` and `SHOPIFY_TEST_PASSWORD` repository secrets to run. If the storefront displays Shopify's connection-verification interstitial, the affected test may be skipped with a reason rather than reported as a selector defect.

## Manual testing notes

[`docs/manual-test-walkthrough.md`](docs/manual-test-walkthrough.md) covers a manual pass through the collection page, product details, cart updates, responsive layout, safe checkout boundary, and the evidence worth saving. These notes support exploratory testing; they are not extra automated coverage.

## Playwright course

The repository also includes a course with lessons, exercises, solutions, checkpoints, and browser labs:

- [Textbook](PLAYWRIGHT_PYTHON_AGENTIC_TESTING_TEXTBOOK.md)
- [Course overview](course/README.md)
- [Modules](course/modules/)
- [Labs](course/labs/)
- [Agentic testing exercises](course/agentic/)
- [Capstone review template](course/projects/capstone-review-template.md)
- [Research notes](course-research-notes.md)

## Scope and status

This is an educational project against a public demo storefront, not a client system. The site may change or block automated traffic, so a failed or skipped run needs to be interpreted in context. Payment submission and real transactions are outside the test scope.
