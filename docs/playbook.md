# Storefront QA Playbook

> **Status: in progress.** These notes describe the checks in the repository today. I'm still adding coverage as I work through the storefront.

## Target

The suite uses the public Shopify demo storefront at https://sauce-demo.myshopify.com/. It is not the classic app at saucedemo.com. This is a demo environment, not a production shop, and the suite deliberately stops at the checkout boundary.

## A manual pass before automation

1. Open the storefront and check whether the collection page is available. Note the browser, viewport, URL, and time.
2. Open a product detail page. Compare the product name and price with the item shown in the collection.
3. Add one product to the cart. Confirm the cart count and item are updated.
4. Add a second product, then change a quantity or remove one. Check that the remaining product is still present and that the cart display updates consistently.
5. Navigate to the checkout boundary, but do not submit payment details or create an order.
6. Repeat the key steps at a smaller viewport and with a fresh browser context.

## Worked example: cart state

**Question:** If two different products are in the cart and one is removed, does the remaining product stay there?

**Setup:** Add product A and product B, then open the cart.

**Expected:** Both products are listed. Remove product A. Product A is absent, product B remains, and the cart count reflects the remaining item.

**Evidence:** Capture the cart before and after the change, along with the trace if the automated check fails. Avoid writing a bug report from an assertion failure alone; inspect whether the storefront changed or an external verification page interrupted the run.

## Test evidence and limits

- The current tests use the live demo storefront, so site availability and markup changes can affect them.
- A verification interstitial is not the same thing as a product bug. The fixture detects the known interstitial and skips with a reason.
- These checks do not submit an order, process payment, or prove the complete store is error-free.
- Next, I'm extending the manual-to-automated examples and improving the notes that accompany failures.
