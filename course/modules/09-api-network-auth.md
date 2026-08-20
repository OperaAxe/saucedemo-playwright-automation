# Module 09 — API, network, authentication, and state

## Goal

Combine browser behavior with HTTP-level setup and verification without making tests unnecessarily slow or unsafe.

## Lesson

Playwright can issue API requests, inspect browser traffic, mock responses, and reuse authentication state. API calls are useful for setting up data, validating server-side postconditions, or testing a service directly.

### Observe traffic

```python
requests = []
page.on("request", lambda request: requests.append(request.url))
page.goto(base_url)
assert any("collections" in url for url in requests)
```

### Mock one boundary

```python
page.route(
    "**/api/products",
    lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='[{"name":"Synthetic product","price":10}]',
    ),
)
```

Mock only the boundary you intend to isolate. A fully mocked UI test may no longer prove that frontend and backend integrate.

### API request context

Use an API context to prepare a disposable record or verify a server response. Keep the token in an environment variable and do not print it.

```python
from playwright.sync_api import APIRequestContext


def get_health(request: APIRequestContext):
    response = request.get("/health")
    assert response.ok
    return response.json()
```

The exact request fixture depends on whether you use `pytest-playwright`’s available fixtures or create a context manually. Always close manually created contexts.

### Authentication

The safe choices are login-per-test and storage-state reuse. Storage state may contain cookies and headers that impersonate a user, so put it under `playwright/.auth` and ignore that directory.

```python
context = browser.new_context()
login_page = context.new_page()
login_page.goto(f"{base_url.rstrip('/')}/account/login")
login_page.get_by_label("Email").fill(email)
login_page.get_by_label("Password").fill(password)
login_page.get_by_role("button", name="Sign in").click()
context.storage_state(path="playwright/.auth/customer.json")
```

For a public demo storefront, do not use a real financial account and do not submit an order. Authenticated coverage should stop at safe account or cart assertions unless a sandbox explicitly supports test transactions.

### State isolation

Fresh browser contexts reset cookies and local storage. A new context does not necessarily reset server-side data. Use unique records or cleanup APIs where the system allows them.

## Exercise

Add three tests: one that records a request URL, one that mocks a product response on a local practice page, and one that skips cleanly when `SHOPIFY_TEST_EMAIL` or `SHOPIFY_TEST_PASSWORD` is absent.

## Solution pattern

```python
import pytest


@pytest.fixture
def credentials():
    email = os.getenv("SHOPIFY_TEST_EMAIL")
    password = os.getenv("SHOPIFY_TEST_PASSWORD")
    if not email or not password:
        pytest.skip("Authenticated credentials are not configured")
    return email, password
```

## Common mistakes

Do not commit storage state. Do not use API setup that creates data without cleanup. Do not mistake a successful API status code for a valid business response; assert useful fields too. Do not let authentication credentials appear in traces or logs.

## Checkpoint

You pass when you can inspect a request, mock a targeted response, explain API/browser context separation, and run optional authenticated tests without hard-coded credentials.
