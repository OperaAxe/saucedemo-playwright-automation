# Manual Test Walkthrough: Shopify Demo Storefront

Target: [sauce-demo.myshopify.com](https://sauce-demo.myshopify.com/)

This walkthrough covers a manual pass through the same storefront used by the Playwright suite. It is a demo store, not the classic SauceDemo app at saucedemo.com and not a production shop.

## Before testing

Record the browser, viewport size, URL, and date. Check that the collection page loads. If Shopify shows a connection-verification page, record what appeared and stop there; an external verification page is not evidence of an application defect.

## Collection and product details

1. Open the collection page and confirm that product cards are visible.
2. Note a product name and price.
3. Open its details page and compare the name and price with the collection card.
4. Check whether sold-out products are identified clearly and whether their available actions make sense.

## Cart behaviour

1. Add one product and open the cart.
2. Check the product name, quantity, and total.
3. Add a second product.
4. Change the quantity or remove one item.
5. Confirm the remaining product is still present and the displayed total reflects the new cart state.

The key question is not just whether the cart updates. It is whether the state of the other items remains correct after the change.

## Responsive layout

Repeat the main navigation, product, and cart checks at a smaller viewport. Look for clipped text, horizontal overflow, hidden controls, or navigation that cannot be reached.

## Evidence to keep

For a reproducible issue, record the starting URL, browser and viewport, preconditions, steps, expected result, actual result, and a screenshot. For a failed automated run, inspect the trace before concluding that a selector or product behaviour is broken. A connection-verification interstitial needs to be distinguished from the page under test.

## Checkout boundary

Follow the journey only as far as the checkout boundary. Do not enter payment details or submit an order. These checks are intended to inspect storefront behaviour without creating transactions.

## Limits

The site is public and can change independently of this repository. A single run does not establish that the whole store is defect-free; it records what happened in the tested conditions.
