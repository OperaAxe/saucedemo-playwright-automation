# Module 12 — Agentic testing

## Goal

Use AI to increase testing leverage without surrendering proof, safety, or engineering judgment.

## Lesson

An agentic test workflow is a bounded loop: observe, plan, act, collect evidence, evaluate, and stop or escalate. The agent may explore an application, propose a test, summarize a failure, or suggest a locator. Deterministic Playwright code should remain responsible for repeatable assertions and safety-critical behavior.

### Agent policy

Write the policy before the prompt:

```text
Target: https://sauce-demo.myshopify.com/
Allowed: catalog, product details, cart add/remove, navigation, screenshots
Forbidden: account deletion, checkout submission, payment entry, real order creation
Evidence: URL, accessible snapshot, visible text, request or trace where relevant
Budget: at most 20 browser actions
Stop: CAPTCHA, login request, payment boundary, unexpected external navigation
Output: JSON observations and failures; no direct repository writes
```

### Structured observation

The Playwright MCP server lets a client expose structured accessibility snapshots to an LLM. This makes roles, names, headings, and controls easier to reason about than pixel-only interaction. It does not make the agent infallible; the agent still needs a task scope and an evidence contract.

A useful prompt:

```text
Explore the catalog only. Do not log in or proceed to checkout. Record each visible product's accessible name, price, availability, and product URL. Use only observations supported by the page snapshot or URL. Return JSON with observations, failures, evidence, and needs_human_review.
```

### Agent output schema

```json
{
  "goal": "catalog_inventory",
  "observations": [
    {
      "name": "Grey jacket",
      "price": "£55.00",
      "available": true,
      "href": "/collections/frontpage/products/grey-jacket"
    }
  ],
  "failures": [],
  "evidence": ["page URL", "accessibility snapshot"],
  "confidence": 0.85,
  "needs_human_review": false
}
```

### Agent-assisted locator repair

When a locator fails, ask for candidates and evidence—not an automatic edit. Require the old selector, observed element, proposed selector, uniqueness check, and a regression result. Review every repair that touches login, authorization, payment, or data mutation.

### Agent-assisted test generation

Ask for a plan before code. The plan should name setup, action, oracle, cleanup, and safety. Generated code must pass syntax checks, collection, targeted execution, and human review. Reject tests with vague assertions such as “page looks good.”

### Failure triage

A read-only triage agent may inspect logs, screenshots, traces, recent diffs, and environment metadata. It should return `cause`, `evidence`, `confidence`, `recommended_action`, and `needs_human_review`. It should not push directly to `main`.

### Prompt injection defense

Web pages, issues, logs, and repository files can contain hostile text. Treat them as untrusted data. A sentence on a page cannot authorize sending a password or changing a repository. Keep secrets outside the agent context when possible, allow only required domains, and route writes through human-reviewed outputs.

## Exercise

Design two agent prompts. The first explores catalog inventory. The second triages a failed test. For each, list allowed tools, forbidden actions, evidence, token/action budget, stop conditions, and output schema.

## Solution checklist

A safe design has a narrow target, a bounded budget, explicit evidence, read-only permissions where possible, secret isolation, network controls, and a human gate for mutation. The deterministic test remains the final oracle.

## Checkpoint

You pass when you can describe the agentic loop, write a safe browser-agent policy, reject unsupported agent claims, and design a read-only CI triage workflow.
