# Module 10 — CI/CD with GitHub Actions

## Goal

Run the same trustworthy tests locally and in GitHub Actions, then preserve evidence when the run fails.

## Lesson

A CI workflow checks out code, selects a Python version, installs dependencies, installs browsers, runs tests, and uploads artifacts. GitHub recommends `actions/setup-python` for consistent interpreters and supports dependency caching and artifact upload.

```yaml
name: Playwright course tests

on:
  push:
  pull_request:

jobs:
  safe-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install -r requirements.txt
      - run: python -m playwright install --with-deps chromium
      - run: pytest -m "not authenticated" --junitxml=reports/junit.xml
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-artifacts
          path: |
            reports/
            test-results/
```

### Safe defaults

The safe job must not require a password or payment. Optional authenticated tests can run in a separate job and skip if credentials are unavailable. Do not reference secrets in unsupported conditional expressions. Keep secrets in repository or environment secrets and pass them through `env` only where required.

### Matrices

Run a small browser matrix when compatibility matters:

```yaml
strategy:
  matrix:
    browser: [chromium, firefox]
```

Do not add browsers merely to look comprehensive. Each additional browser increases runtime and creates another failure surface.

### Artifacts

Artifacts should include JUnit XML, screenshots, traces, videos, and HTML reports when available. Always upload them on failure. A red build without evidence wastes a second debugging session.

### CI debugging exercise

Break a selector, push a branch, open the Actions run, inspect the failed step, download the artifact, and classify the failure. Then fix the test and verify a green run. Record the commit that changed the result.

### Solution checklist

- The workflow has `push` and `pull_request` triggers.
- Python and browser versions are explicit.
- Dependencies are installed from the repository.
- Safe tests do not need secrets.
- Auth tests are optional and isolated.
- Artifacts upload with `if: always()`.
- No password appears in YAML, logs, or source.

## Common mistakes

Do not trust a local green run when the workflow has not executed. Do not hide failure with `continue-on-error` on the actual test step. Do not put credentials in command-line arguments that may appear in logs. Do not silently skip every test; report skip reasons.

## Checkpoint

You pass when your workflow can run on a clean Ubuntu runner, install Chromium, execute safe tests, and upload evidence after failure.
