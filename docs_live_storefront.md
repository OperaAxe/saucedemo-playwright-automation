# Live storefront inspection

## Registration page

URL: https://sauce-demo.myshopify.com/account/register

The current site is a Shopify storefront. The registration page exposes these controls:

- `#first_name` — first name input
- `#last_name` — last name input
- `#email` — email input
- `#password` — password input
- `input[type="submit"]` — Create button

The storefront does not use the classic SauceDemo username/password login form. The home page exposes Home, Catalog, Blog, About Us, Wish list, Refer a friend, Login, Create account, My Cart, and Check Out. The home page currently displays Grey jacket, Noir jacket, and Striped top.

## Implementation implication

The test suite must target Shopify customer registration/login, catalog/product pages, cart, and Shopify checkout. The classic SauceDemo accounts such as `standard_user / secret_sauce` are not applicable to this site.

## Registration interaction update

The registration form accepted first name `Christian` and last name `David`. The page reports `Protected by hCaptcha`, so account creation may require a human CAPTCHA interaction before the form can be submitted. No CAPTCHA-solving attempt will be made programmatically.

The authorized first name, last name, email, and password fields are now filled. The form still indicates hCaptcha protection. The Create action has not been submitted because CAPTCHA completion requires a human interaction and must not be bypassed programmatically.

## Account-state update

After the user completed the CAPTCHA and reported the account created, the storefront home page showed `My Account` and `Log Out`, confirming a logged-in state in that browser context. Direct navigation to `/account` redirected to `/account/login`, so the suite should validate authentication through the visible logged-in navigation state and handle the storefront's legacy account routing carefully.

The login page is available at `/account/login` and contains customer email/password fields plus a forgot-password/reset-password section.

## Catalog page

URL: https://sauce-demo.myshopify.com/collections/all

The catalog currently lists seven products: Black heels (£45.00), Bronze sandals (£39.99), Brown Shades (£20.00, sold out), Grey jacket (£55.00), Noir jacket (£60.00), Striped top (£50.00), and White sandals (£25.00, sold out). Product links use Shopify paths such as `/collections/all/products/grey-jacket`.

The header exposes Search, About Us, Login/Create account or account-state links, My Cart, and Check Out. The catalog page did not expose a classic SauceDemo inventory sort dropdown in the extracted content.

## Product detail page

URL observed: https://sauce-demo.myshopify.com/products/grey-jacket

The rendered product page exposes:

- Product title text `Grey jacket`
- Price text `£55.00`
- Variant selector `#product-select-option-0`
- Add-to-cart submit control `#add`
- Header links for My Account/Log Out, My Cart, and Check Out

The storefront uses a simple Shopify product form rather than SauceDemo inventory controls.

## Local test-run observations

The live cart page renders the empty message as `It appears that your cart is currently empty! Continue Shopping.` rather than containing the exact phrase `Your cart is empty`. The login page screenshot confirms the customer form is rendered with visible Email Address, Password, and SIGN IN controls. Several failures also showed intermittent `ERR_CONNECTION_CLOSED` responses during repeated live navigation, so the suite should use explicit retries for transient storefront network errors where appropriate.

## Connection-verification limitation during repeated headless runs

After several rapid live requests, the storefront returned a full-page interstitial reading `Your connection needs to be verified before you can proceed`. This affected catalog, login, cart, checkout, and UI tests in the repeated suite run. The first targeted run passed all non-authenticated tests except two selector issues, which were fixed; the later full run encountered the storefront interstitial broadly. This is an external anti-automation/network condition, not a selector assertion failure.
