# Hands-on course: Playwright with Python to Agentic Testing

This directory is the practical companion to [`PLAYWRIGHT_PYTHON_AGENTIC_TESTING_TEXTBOOK.md`](../PLAYWRIGHT_PYTHON_AGENTIC_TESTING_TEXTBOOK.md). The textbook explains the concepts continuously. This course makes you build the skill through small, runnable lessons.

## Starting point

You are starting from zero with Playwright. You do not need to understand the existing automation framework before beginning. The lessons deliberately start with Python, terminal usage, HTML, and test thinking before introducing browser automation.

Use one lesson at a time. Read the lesson, type the example instead of copying it blindly, complete the exercise without opening the solution, run the checkpoint, and write down what failed. A failed test is part of the lesson.

## Curriculum map

| Module | Main question | Deliverable |
|---:|---|---|
| 01 | How do I set up Python for testing? | A working `.venv` and Python exercises |
| 02 | What makes a good test? | Test charters and plain Python checks |
| 03 | How does a web page work? | Locator plan and HTML observations |
| 04 | How do I control a browser? | First Playwright smoke tests |
| 05 | How do I locate elements reliably? | Locator practice suite |
| 06 | How do I wait and assert correctly? | Synchronized interaction tests |
| 07 | How do I build a maintainable suite? | Fixtures and POM refactor |
| 08 | How do I test real browser behavior? | Forms, tabs, downloads, files, dialogs |
| 09 | How do I control state and APIs? | API/UI hybrid and network-mocking tests |
| 10 | How do I deliver tests in CI? | GitHub Actions with artifacts |
| 11 | What makes a test suite trustworthy? | Debugging, reliability, responsive and visual checks |
| 12 | How do I use AI safely? | Agent policy and evidence-based agent loop |
| 13 | How do I build the capstone? | Complete Shopify framework and review |

## Commands used throughout

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
pytest -q
pytest --collect-only -q
python -m compileall -q pages tests utils
```

## Rules for this course

Do not store passwords, API tokens, cookies, or Playwright storage state in Git. Do not use a real payment method or submit an order for a learning exercise. Use the public demo store, a local test page, or a disposable staging system. When an exercise involves an agent, require evidence and keep the agent read-only unless a human has explicitly reviewed the action.

## Completion standard

You have completed the course when you can design a test from a requirement, choose a test layer, implement a resilient locator, control state with fixtures, collect artifacts, diagnose a failure, run the suite in CI, and explain exactly where an agent may assist without replacing deterministic proof.

## Module navigation

- [01 — Python and environment](modules/01-python-and-environment.md)
- [02 — Testing thinking](modules/02-testing-thinking.md)
- [03 — Web fundamentals and inspection](modules/03-web-fundamentals.md)
- [04 — First Playwright tests](modules/04-first-playwright-tests.md)
- [05 — Locators](modules/05-locators.md)
- [06 — Waiting and assertions](modules/06-waiting-and-assertions.md)
- [07 — Fixtures and Page Object Model](modules/07-fixtures-and-pom.md)
- [08 — Browser capabilities](modules/08-browser-capabilities.md)
- [09 — API, network, auth, and state](modules/09-api-network-auth.md)
- [10 — CI/CD](modules/10-ci-cd.md)
- [11 — Reliability and quality](modules/11-reliability-quality.md)
- [12 — Agentic testing](modules/12-agentic-testing.md)
- [13 — Capstone](modules/13-capstone.md)

## Projects

The exercises lead into three projects:

1. **Local browser lab:** a deterministic HTML page used for forms, dialogs, downloads, and uploads.
2. **Shopify storefront suite:** the current Sauce Demo Shopify store at `https://sauce-demo.myshopify.com/`, tested without payment or order submission.
3. **Agentic quality assistant:** a read-only workflow that turns test artifacts into a structured diagnosis or exploration report.

The existing `pages/`, `tests/`, and `.github/workflows/playwright.yml` files are the reference solution for the Shopify project. Do not read them first if you want to practice honestly; use them after attempting the exercises.
