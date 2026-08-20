# Module 06 — Waiting and assertions

## Goal

Make tests wait for application state instead of guessing with sleeps.

## Lesson

Before a click, Playwright checks uniqueness, visibility, stability, event reception, and enabled state. If the checks are not satisfied before the timeout, the action fails. Assertions retry in the same spirit.

```python
from playwright.sync_api import expect

expect(page.get_by_role("heading", name="Products")).to_be_visible()
expect(page.locator("a[href*='/products/']")).to_have_count(3)
expect(page).to_have_url(re.compile(r"/collections/all$"))
```

### Replace fixed waits

Weak:

```python
page.wait_for_timeout(2000)
```

Better:

```python
expect(page.get_by_role("status")).to_have_text("Saved")
```

A timeout can be correct when you are bounding an external system, but it should be paired with evidence and used narrowly.

### Event synchronization

Register the event before the action:

```python
with page.expect_download() as download_info:
    page.get_by_role("button", name="Export").click()
download = download_info.value
```

For a new tab:

```python
with page.expect_popup() as popup_info:
    page.get_by_role("link", name="Receipt").click()
receipt = popup_info.value
```

For a request:

```python
with page.expect_response(lambda response: "/cart" in response.url) as response_info:
    page.get_by_role("button", name="Add to cart").click()
assert response_info.value.ok
```

### Assertions versus Python `assert`

Use Playwright’s `expect` for page state because it retries and produces locator diagnostics. Use Python `assert` for already-collected values or pure business rules.

```python
expect(page.get_by_role("heading", name="Cart")).to_be_visible()
items = cart.product_names()
assert items == ["Grey jacket"]
```

### Debugging a timeout

Ask in order: what URL am I on, did the intended page render, is the locator unique, is the element hidden, did a verification or consent layer appear, and is the application waiting on a request? Capture a screenshot or trace before changing the test.

## Exercise

Find a test in the existing suite with a fixed wait or an overly broad timeout. Replace it with an assertion or event. Then break the target locator and run with `--trace retain-on-failure`.

## Solution pattern

```python
with page.expect_response(lambda response: "/cart" in response.url):
    add_button.click()
expect(page.get_by_role("link", name=re.compile("Cart"))).to_be_visible()
```

## Common mistakes

Do not use `force=True` to bypass actionability without understanding the overlay or disabled state. Do not increase all timeouts globally. Do not assert the current URL before the page transition has completed.

## Checkpoint

You pass when you can replace one fixed wait with a meaningful condition, synchronize one event, and explain the root cause of a timeout.
