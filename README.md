# taxyear-lab

The warm-up from the **AI Engineering Masterclass: From Prompting to Production**.
One tiny TypeScript function, one bug, and every idea from the session at small scale.
Synthetic data only.

> When you've done this, try the full version: **[ledgerlab](https://github.com/developermustaq/ledgerlab)**
> (a release blocked by a CI contract check, an incident system over MCP, three agents, checkpoints).

## The bug

The UK tax year runs from 6 April to 5 April. `taxYear()` puts **5 April 2026** in **2026/27**.
It belongs in **2025/26**. All 5 tests still pass.

```bash
npm ci
npm test                          # 5 passed
npm run -s year -- 2026-04-05     # taxYear(2026-04-05) = 2026/27  ← wrong
```

## The session, step by step

Each step has a real screenshot in [`slides/out/`](slides/out/), captured 2026-11-04 in VS Code with Claude Code.

| Step | Idea | Try it | Screenshot |
|---|---|---|---|
| 1 | Green tests ≠ correct code | `npm test`, then `npm run -s year -- 2026-04-05` | `01-the-case` |
| 2 | Context costs tokens: search, don't paste | `bench/measure.sh haystack` (real tokens), or `npm run -s compare:haystack` for the recorded numbers | `02-haystack` |
| 3 | `CLAUDE.md` survives `/clear` | In `claude`: `/clear`, then ask for the project's tax-year rules | `03-claude-md` |
| 4 | A skill packages a procedure | `/fix-bug 5 April 2026 is reported as 2026/27 but should be 2025/26` | `04-fix-t20` |
| 5 | Prove it: red → green → diff | `git switch step-2-fixed`, then `git stash` the fix to watch the new test fail | `04a-red`, `04c-green`, `04d-diff` |
| 6 | FACT / INFERENCE / UNKNOWN | Read the end of the `/fix-bug` report | `04-fix-t40` |
| 7 | Parallel agents: faster, not cheaper | `bench/measure.sh agents`, or `npm run -s compare:agents` | `05-agents` |
| 8 | MCP: named tools, typed arguments | `/mcp`, then ask Claude to use `tax-calendar` | `06a-mcp-list`, `06b-mcp-call` |
| 9 | Permissions are enforced | Ask Claude to run `git push origin main` | `07b-deny-rule` |

## What's where

| Path | What it is |
|---|---|
| `src/taxYear.ts` | The function with the bug (line 5) |
| `CLAUDE.md` | Project rules Claude loads every session |
| `.claude/skills/fix-bug/SKILL.md` | The three-phase skill: reproduce, smallest fix, prove it |
| `.claude/agents/reviewer.md` | A read-only reviewer subagent (Read, Grep, Glob) |
| `.claude/settings.json` | Allow `npm test`, `git diff`; deny `.env`, `git push`, `curl` |
| `.mcp.json`, `mcp/tax-calendar.mjs` | A one-tool MCP server: `get_tax_year_dates(startYear)` |
| `logs/report-run.log` | 2,000 noisy lines, one real error (line 1424) |
| `bench/` | `measure.sh` re-runs the measured scenarios; `recorded/` holds the session's numbers |

Branches: `main` has the bug. `step-2-fixed` has the fix Claude made with `/fix-bug`.

The numbers are **one run each**, not a benchmark. Your runs will differ.

## Safety

- Synthetic data only. Never put real client data, keys or credentials in a sandbox.
- `.env` is git-ignored and holds a placeholder. The deny rule stops Claude reading it.
- Prefer allow-lists and permission modes over `--dangerously-skip-permissions`.
