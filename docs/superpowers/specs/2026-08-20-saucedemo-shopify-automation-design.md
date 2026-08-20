# SauceDemo Shopify Playwright Automation Design

## Objective

Build a maintainable Python test suite that validates the current Sauce Demo Shopify storefront at [https://sauce-demo.myshopify.com/](https://sauce-demo.myshopify.com/). The suite will use Playwright's synchronous API and the Page Object Model. It will focus on storefront behavior that exists on the live Shopify site rather than the classic SauceDemo application contract.

## Scope decision

The supplied `standard_user / secret_sauce` accounts belong to the classic SauceDemo application and are not valid for this Shopify storefront. The implementation therefore replaces those incompatible tests with Shopify customer authentication, catalog, product detail, cart, navigation, responsive-layout, and checkout-boundary coverage. The suite will not submit an order or enter payment details.

## Architecture

The suite will separate browser-facing behavior into focused page objects:

| Component | Responsibility |
|---|---|
| `BasePage` | Shared navigation, URL checks, and common header selectors. |
| `LoginPage` | Customer login, logout-state assertions, and login validation. |
| `CatalogPage` | Collection navigation, product discovery, product names, prices, and availability. |
| `ProductPage` | Product title, price, variant selection, and add-to-cart action. |
| `CartPage` | Cart contents, quantities, line-item removal, subtotal, and checkout navigation. |
| `CheckoutPage` | Checkout-page boundary assertions only; no payment submission. |

Fixtures in `tests/conftest.py` will provide the base URL, browser context, page, customer credentials from environment variables, and reusable page-object instances. Credentials will never be hard-coded in the test source or CI logs.

## Test coverage

The test modules will cover the following behaviors:

| Test module | Coverage |
|---|---|
| `test_login.py` | Customer login page, successful authenticated header state when credentials are available, invalid credentials, logout visibility, and registration-page availability. |
| `test_inventory.py` | Catalog page availability, product count, product names/prices, product detail navigation, and sold-out product representation. |
| `test_cart.py` | Add one item, add multiple items, verify quantities and totals, remove an item, and empty-cart behavior. |
| `test_checkout.py` | Checkout entry from cart and checkout boundary visibility. No order completion or payment data will be submitted. |
| `test_ui_ux.py` | Header navigation, home/catalog links, mobile viewport rendering, and absence of horizontal overflow where measurable. |

## Robustness strategy

Selectors will prefer stable IDs and semantic roles, with CSS classes used only where the theme exposes no better contract. Product assertions will derive from the live catalog where possible rather than assuming a fixed product order. Tests that depend on an account will be skipped with a clear reason when the required environment variables are absent, allowing public CI to run safely without exposing credentials.

The suite will use conservative timeouts, isolated browser contexts, cleanup through cart removal where possible, and screenshots or traces on failure. Checkout tests will stop at the Shopify checkout boundary to avoid financial or irreversible actions.

## CI/CD

GitHub Actions will run on pushes to `main` and on pull requests. The workflow will install the pinned-compatible Python dependencies, install Chromium, execute the safe test suite, and upload HTML reports, screenshots, and traces when available. Authenticated tests will run only when repository secrets are configured.

## Acceptance criteria

The implementation is complete when the requested repository structure exists, the tests can be collected and executed locally, safe live-storefront tests pass or are explicitly skipped for environmental reasons, the CI workflow is syntactically valid, the README describes setup and execution, and all changes are committed and pushed to the public repository's `main` branch.

## References

[1]: https://sauce-demo.myshopify.com/ "Sauce Demo Shopify storefront"
[2]: https://playwright.dev/python/docs/intro "Playwright Python documentation"
[3]: https://docs.pytest.org/en/stable/ "pytest documentation"
