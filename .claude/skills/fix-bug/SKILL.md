---
name: fix-bug
description: Fix a reported bug in three phases - reproduce it with a failing test, make the smallest fix, then prove it with test output.
---

# Fix a bug

## Phase 1: reproduce (no source edits)

1. Restate the bug in one sentence.
2. Read the relevant code and the existing tests.
3. Write the smallest test that fails because of the bug.
4. Run `npm test` and show that test failing.

## Phase 2: smallest fix

1. Name the rule from CLAUDE.md that the code breaks.
2. Change as little code as possible to restore it.
3. Do not change public signatures or existing tests.

## Phase 3: prove it

1. Run `npm test` and show the full output.
2. Report:
   - FACT: what the test output proves
   - INFERENCE: what you believe but did not prove
   - UNKNOWN: what nobody has checked yet
   - files changed
