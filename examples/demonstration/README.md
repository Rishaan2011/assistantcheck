# Runnable assistant regression demonstration

This is a **synthetic, rule-based demo**, built as an example for AssistantCheck.
It is not an AI-powered assistant, an independent user's project, a report of
real-world adoption, or proof of safety. It never sends email or executes tasks.

## Run

From the repository root (the folder containing `pyproject.toml`), with Python 3.10+:

```sh
python3 -m examples.demonstration
```

No installation, API key, or internet connection is required.

## What actually happens

1. The runner loads five prompts and their separately defined expectations.
2. `planner.py` parses each prompt and generates a structured decision. It does
   not read the expectations. It supports only a small explicit command grammar.
3. The deliberately flawed configuration selects `email.send` immediately.
4. AssistantCheck compares its generated decisions with the expected behavior
   and flags the unconfirmed send.
5. The same prompts run with confirmation enabled. The send becomes `confirm`
   and all five cases pass.

The draft and task decisions are plans only; there are no tool implementations.
The confirmation decision represents the moment before approval. This demo does
not implement an approval conversation or an execution engine.

## Verified output

```text
SIMULATED DEMO: rule-based planner; no AI model or actions executed.
BEFORE: 4/5 passed
  FAIL send: decision mismatch, tool mismatch, arguments mismatch
AFTER: 5/5 passed
DEMO VERIFIED
Generated predictions and reports: reports/demonstration
```

The flawed configuration and its intended failure were deliberately authored.
These are demonstration results, not measured performance of a deployed model.

## Inspect the evidence

The runner writes four JSON files under `reports/demonstration`: the generated
predictions and checker report for each configuration. These are generated at
runtime, not copied from expected answers. Run them through the standalone CLI:

```sh
python3 -m assistantcheck examples/demonstration/cases.json reports/demonstration/before_predictions.json
python3 -m assistantcheck examples/demonstration/cases.json reports/demonstration/after_predictions.json
```

The first command intentionally exits 1; the second exits 0. The demo runner
itself exits 0 when it detects the intended failure and the corrected run passes.
Use `--output-dir PATH` to save elsewhere. Files with the same names are replaced.

## Extend it

Add a supported prompt and expected decision in `cases.json`, or extend the
planner's grammar and add tests. Unsupported prompts produce `clarify`.
To connect a real assistant, replace calls to `plan()` with a planning-only
adapter, normalize its output into this schema, and keep execution disabled.
Do not feed the expected answers to that adapter.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Tests verify the before/after behavior, unseen input handling, confirmation by
default, output generation, and standalone re-evaluation. The existing GitHub
workflow discovers these tests automatically when they are uploaded.
