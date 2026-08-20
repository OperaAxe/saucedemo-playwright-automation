# Course research notes

## Official Playwright Python guidance

[Playwright Python installation](https://playwright.dev/python/docs/intro) recommends the official pytest plugin for end-to-end tests and documents installing `pytest-playwright`, installing browsers, creating `test_*.py` files, running `pytest`, and updating Playwright packages. The current documentation states that Playwright supports Chromium, WebKit, and Firefox and can run locally or in CI.

[Playwright Python library](https://playwright.dev/python/docs/library) documents both synchronous and asynchronous APIs. The sync API uses `sync_playwright()` as a context manager; browsers are launched through `p.chromium`, `p.firefox`, or `p.webkit`. The docs also warn that Playwright auto-waits and that `time.sleep()` is generally the wrong waiting mechanism because it can leave state outdated; Playwright waits should be preferred.

[Playwright locators](https://playwright.dev/python/docs/locators) recommends user-facing locators such as `get_by_role`, `get_by_label`, `get_by_text`, `get_by_placeholder`, and `get_by_test_id`. Locators re-query the current DOM when actions are performed, support filtering and chaining, and should generally be preferred over brittle CSS/XPath chains.

[Playwright actionability](https://playwright.dev/docs/actionability) explains that actions such as click perform checks for uniqueness, visibility, stability, event reception, and enabled state, and wait until those checks pass. Playwright assertions also retry automatically. `force=True` disables non-essential checks and should be treated as an exception, not a default.

[Playwright authentication](https://playwright.dev/python/docs/auth) explains browser-context isolation and recommends saving reusable authenticated state under `playwright/.auth`, adding it to `.gitignore`, and never committing state files because cookies and headers can impersonate the account. The course will teach both login-per-test and storage-state reuse.

[Playwright API testing](https://playwright.dev/docs/api-testing) describes direct REST testing, API-driven setup and teardown, postcondition checks after UI actions, and sharing state between API and browser contexts. The course will teach API/UI hybrid tests without copying the JavaScript-only examples directly.

## Pytest guidance

[Pytest fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) describes fixtures as explicit, modular, and scalable sources of reliable test context. Fixtures are requested through test-function arguments, can depend on one another, can be parametrized, and have scopes such as function, module, and session. Fixture errors prevent a test from being attempted and are distinct from assertion failures. The course will use these distinctions when teaching debugging.

## GitHub Actions guidance

[GitHub’s Python Actions guide](https://docs.github.com/actions/guides/building-and-testing-python) recommends `actions/setup-python` for consistent Python versions, installing dependencies from `requirements.txt`, caching pip dependencies, running the same pytest commands used locally, and uploading test artifacts such as JUnit reports. The CI modules will teach reproducibility, artifacts, matrices, and secret handling.

## Agentic testing references

[Playwright MCP documentation](https://playwright.dev/docs/getting-started-mcp) describes browser automation through the Model Context Protocol using structured accessibility snapshots rather than screenshots. It supports navigation, interaction, screenshots, keyboard and mouse actions, dialogs, tabs, network inspection/mocking, console access, and storage-state handling. The course will treat MCP as an agent interface layered on top of Playwright—not as a replacement for deterministic test code.

[Microsoft Playwright MCP repository](https://github.com/microsoft/playwright-mcp) describes structured accessibility-tree interaction, deterministic tool application, persistent or isolated browser profiles, storage state, network controls, and the distinction between exploratory/self-healing agent loops and token-efficient CLI workflows.

[GitHub Agentic Workflows](https://github.github.com/gh-aw/) distinguishes deterministic workflows for builds, tests, linting, deployment, and reproducible scripts from agentic workflows for reasoning-heavy tasks such as issue triage, CI investigation, documentation updates, code review, and repository reporting. It documents sandboxing, scoped permissions, safe outputs, threat detection, cost controls, and human-reviewed writes.

[GitHub Agentic Workflows Playwright reference](https://github.github.com/gh-aw/reference/playwright/) documents CLI-based Playwright integration as the recommended mode for new agentic workflows, with MCP mode deprecated in that specific ecosystem. It highlights accessibility testing, visual regression, E2E testing, local-dev-server testing, explicit network permissions, and browser/version pinning for visual baselines.

## Course design implications

The course will teach a strict separation between deterministic automation and agentic assistance. Deterministic code owns repeatable assertions, safety-critical actions, data setup, and CI gates. Agents may explore, propose scenarios, summarize failures, suggest locator repairs, generate drafts, and prioritize tests, but every proposal must be evaluated against executable checks. Unsafe actions such as purchases, production mutations, secret exposure, and unreviewed writes remain behind explicit human approval and scoped permissions.

## Python foundations references

[Python Tutorial](https://docs.python.org/3/tutorial/index.html) covers the interpreter, informal language introduction, control flow, data structures, modules, I/O, errors and exceptions, classes, standard-library tours, and virtual environments. It is designed for programmers who are new to Python rather than absolute programming beginners, so the course will add gentler explanations and testing-specific exercises around it.

[Python virtual environments and packages](https://docs.python.org/3/tutorial/venv.html) explains why separate applications need isolated dependencies, how to create and activate `.venv` environments with `python -m venv`, how to install packages with `python -m pip`, and how to record/install dependencies with `requirements.txt`. [The `venv` reference](https://docs.python.org/3/library/venv.html) emphasizes that environments are isolated, disposable, not portable, and should not be committed to version control; they should be recreated from dependency declarations.
