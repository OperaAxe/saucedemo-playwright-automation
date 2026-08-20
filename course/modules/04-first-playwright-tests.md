# Module 04 — Your first Playwright tests

## Goal

Install Playwright with Python and write browser tests that open a page and prove meaningful state.

## Setup

```bash
python -m pip install pytest pytest-playwright
python -m playwright install chromium
```

Create `tests/test_first_smoke.py`:

```python
import re

from playwright.sync_api import Page, expect


def test_playwright_documentation_has_a_get_started_link(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))
    expect(page.get_by_role("link", name="Get started")).to_be_visible()
```

Run:

```bash
pytest -q
pytest --collect-only -q
pytest --headed --slowmo 250
```

The official Playwright Python documentation recommends the pytest plugin for end-to-end tests because it provides fixtures and isolated browser contexts. The sync API is intentionally used in this course first. The async API uses the same concepts but adds `async` and `await`.

### Manual API versus plugin

A manual script is useful for a quick experiment:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    assert "Example" in page.title()
    browser.close()
```

A test suite benefits from the plugin because setup, teardown, browser options, and artifact behavior are centralized. Do not launch a browser manually inside every pytest function.

### The first assertion

A good smoke test has at least one assertion tied to the purpose of the test. A page title check may prove routing, but a heading or user-visible control usually proves more. Use both when they answer different questions.

## Exercise

Write three tests against `https://sauce-demo.myshopify.com/`:

1. the home page opens;
2. the Catalog link is visible;
3. the Cart link is visible.

Add a `base_url` fixture instead of repeating the URL.

## Solution pattern

```python
import pytest
from playwright.sync_api import expect


@pytest.fixture
def base_url() -> str:
    return "https://sauce-demo.myshopify.com/"


def test_catalog_link(page, base_url):
    page.goto(base_url)
    expect(page.get_by_role("link", name="Catalog", exact=True)).to_be_visible()
```

## Common mistakes

Do not use `time.sleep()` to make a first test pass. Do not put secrets in the file. Do not call a test “passed” because the browser opened; prove a visible behavior.

## Checkpoint

You pass when `pytest --collect-only -q` finds your tests, the suite runs headless, and you can run one test headed to inspect the browser.
