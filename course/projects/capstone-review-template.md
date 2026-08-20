# Capstone review

## 1. Test-layer decisions

Which behaviors did you place in unit, API, integration, browser, or agentic exploration checks? Why is each layer appropriate?

## 2. Locator decisions

Identify the three most important locators in your suite. For each, state the user-facing contract, fallback, and known risk.

## 3. State isolation

Explain how browser contexts, cart cleanup, test data, and optional authentication prevent order-dependent tests.

## 4. Failure evidence

Describe which screenshots, traces, reports, console logs, or network records CI uploads and how you would investigate a red run.

## 5. CI safety

Explain how the workflow avoids committing secrets and how authenticated tests behave when secrets are missing.

## 6. Agent policy

List the actions an agent may perform, the actions it must never perform, the evidence it must provide, and the conditions that require human review.

## 7. Final commands

```bash
python -m compileall -q pages tests utils course
pytest --collect-only -q
pytest -m "not authenticated" -q
```

## 8. Human review decision

- [ ] Safe suite passes or skips only for documented external blocking.
- [ ] Authenticated state and secrets are ignored and not committed.
- [ ] CI artifacts are available after failure.
- [ ] Agent output is treated as a proposal, not proof.
- [ ] No payment or real order was submitted.
- [ ] Another learner can reproduce the setup from the README.
