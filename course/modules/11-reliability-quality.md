# Module 11 — Reliability and quality signals

## Goal

Learn how to distinguish product defects from test defects and environmental failures.

## Lesson

A failing test is evidence, not a verdict. First capture the page URL, screenshot, accessible snapshot, console output, network activity, and trace where useful. Then classify the failure.

| Failure | Example | First response |
|---|---|---|
| Product | Valid form is rejected | Reproduce and report |
| Locator | Hidden duplicate selected | Improve locator |
| Timing | Assertion precedes response | Synchronize with state |
| Data | Account is locked | Fix fixture or environment |
| Environment | Verification interstitial | Skip/quarantine with evidence |
| Agent | Unsupported repair proposal | Reject and require proof |

### Traces

Run `pytest --trace retain-on-failure`. A trace shows the action timeline and DOM snapshots around the failure. It is more useful than a screenshot alone because it lets you inspect what the page looked like before and after the action.

### Flakiness

A flaky test is not “almost passing.” Record the test, environment, attempt number, failure class, and artifact. A retry may collect information, but it should not be the permanent fix. If an external verification page blocks a public demo site, the test should skip with an explicit reason rather than failing as if the selector were wrong.

### Responsive tests

```python
import pytest


@pytest.mark.parametrize("width,height", [(390, 844), (768, 1024), (1440, 900)])
def test_no_horizontal_overflow(page, base_url, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(base_url)
    body = page.locator("body").bounding_box()
    assert body is not None
    assert body["width"] <= width
```

### Visual checks

A screenshot comparison is sensitive to browser version, fonts, data, time, and animations. Use stable fixtures, mask dynamic areas, and pin the environment. A visual diff is a prompt for review, not automatic proof of a defect.

### Quality gates

A useful quality gate may include syntax compilation, unit checks, smoke tests, browser tests, artifact upload, and linting. Not every check needs to run on every pull request. Make the gate fast enough to use and strong enough to matter.

## Exercise

Break a locator in a cart test. Run with `--trace retain-on-failure`. Write a short incident note with the failure class, evidence, root cause, fix, and regression command.

## Solution template

```text
Failure class: Locator defect
Evidence: Trace shows two matching cart links; first match is hidden
Root cause: Test selected a responsive duplicate without a visible or region constraint
Fix: Use header region plus visible cart link
Regression: pytest tests/test_ui_ux.py -q
```

## Common mistakes

Do not call every failure flaky. Do not change selectors from a screenshot without inspecting the DOM. Do not add retries before understanding the failure. Do not compare full-page screenshots containing dynamic timestamps.

## Checkpoint

You pass when you can collect a trace, classify a failure, write a useful incident note, and explain the limits of responsive and visual checks.
