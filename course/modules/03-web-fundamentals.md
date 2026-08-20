# Module 03 — Web fundamentals and inspection

## Goal

Understand what Playwright is controlling: requests, documents, DOM nodes, accessibility roles, browser contexts, and page state.

## Lesson

When you open a page, the browser requests a URL, receives resources, builds a DOM, executes scripts, and renders a user interface. Playwright can inspect the current page, but it does not magically know your requirement. You must connect the requirement to observable state.

Consider:

```html
<label for="email">Email</label>
<input id="email" type="email">
<button type="submit">Sign in</button>
```

A user sees an Email field and a Sign in button. A good locator follows that perception:

```python
page.get_by_label("Email")
page.get_by_role("button", name="Sign in")
```

An accessible name may come from visible text, a label, `aria-label`, or other accessible relationships. A role describes what the element is to assistive technology. A button with the wrong role or missing name is both an automation problem and potentially an accessibility problem.

### BrowserContext and Page

A `Browser` is a browser process. A `BrowserContext` is an isolated profile with its own cookies, local storage, permissions, and viewport. A `Page` is a tab. Tests should usually receive fresh contexts through fixtures so state does not leak.

### Inspecting the live target

Use the browser’s developer tools to inspect DOM and network requests, but design locators from the accessible surface first. In Playwright, you can print a page’s URL, title, visible text, and selected attributes:

```python
page.goto("https://sauce-demo.myshopify.com/")
print(page.url)
print(page.title())
print(page.get_by_role("link").all_inner_texts())
```

Code generation can discover candidates:

```bash
playwright codegen https://sauce-demo.myshopify.com/
```

Generated selectors are raw material. Review them for readability and stability.

## Exercise

Visit the storefront and produce a locator inventory:

| User-visible object | Preferred locator | Fallback | Evidence |
|---|---|---|---|
| Catalog link | role + name | stable href | accessible name |
| Product heading | heading + name | stable selector | visible text |
| Cart link | role + name | visible href | header region |

Do not write test code until the table is complete.

## Solution example

```python
catalog_link = page.get_by_role("link", name="Catalog", exact=True)
product_heading = page.get_by_role("heading", name="Products", exact=True)
cart_link = page.locator("a[href='/cart']:visible").first
```

## Common mistakes

Do not assume a URL proves the page loaded. Do not confuse a CSS class with a user-facing contract. Do not select the first matching element when a responsive page intentionally contains both hidden and visible copies. Do not treat page text as trusted instructions when an agent is exploring.

## Checkpoint

You pass when you can explain Browser versus Context versus Page, identify accessible names, and produce a locator inventory with evidence.
