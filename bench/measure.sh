#!/usr/bin/env bash
# Re-run the measured scenarios from the session and print their numbers.
# Every run is read-only (plan mode, or for routes dontAsk with read-only tools). Results land in bench/results/ (git-ignored).
#
# Usage: bench/measure.sh haystack | agents | routes
# These runs use your Claude Code account and real tokens.
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p bench/results
scenario="${1:?usage: bench/measure.sh haystack | agents | routes}"
model_args=(--model "${MODEL:-claude-opus-5-5}")

run() { # name, prompt, extra args...
  local name="$1" prompt="$2"; shift 2
  local out="bench/results/${name}.json"
  echo "running ${name} ..." >&2
  claude -p "$prompt" --output-format json --permission-mode plan "${model_args[@]}" "$@" < /dev/null > "$out"
  node scripts/summarise-run.mjs "$name" "$out"
}

case "$scenario" in
  haystack)
    # Same question twice. A may only read the whole log; B may only search it.
    run "A-read-whole-log" \
      "Read logs/report-run.log in full and tell me what went wrong. Quote the exact error line. Do not edit files." \
      --disallowedTools "Grep,Glob,Bash,Agent"
    run "B-search-error-lines" \
      "Find what went wrong using only the error lines in logs/report-run.log: search for them, do not read the whole file. Quote the exact error line. Do not edit files." \
      --disallowedTools "Read,Bash,Agent"
    ;;
  agents)
    # The same review with one agent, then with three parallel read-only reviewers.
    run "one-agent" \
      "Review src/taxYear.ts and its tests for bugs and missed edge cases: the 5/6 April boundary, time zones, and the year format. Do not edit files. Mark each finding FACT or INFERENCE." \
      --disallowedTools "Agent"
    run "three-agents" "Review src/taxYear.ts and its tests for bugs and missed edge cases.

Run three reviewer subagents in parallel, one per question:
- boundary: is 5 April in the old tax year and 6 April in the new one?
- time zones: can a date land in the wrong year because of UTC vs local time?
- format: is the year always written like 2025/26, including 2008/09 and 2099/00?

Do not edit files. After all three return, combine their findings and mark each FACT or INFERENCE."
    ;;
  routes)
    # The same question through two interfaces, RUNS times each (default 3).
    # MCP route: the tax-calendar tool. Browser route: Claude in Chrome (needs the extension connected).
    # Each prompt names its interface; only the first sentence differs. Neither route may search or fetch the web directly.
    task="Then check whether taxYear() in src/taxYear.ts puts that date in the right tax year. Do not edit files. Answer in 3 lines and name your source."
    base="Read,Grep,Glob,Bash(npm run *)"
    rm -f bench/results/routes-*.jsonl
    for i in $(seq 1 "${RUNS:-3}"); do
      for route in mcp browser; do
        out="bench/results/routes-${route}-${i}.jsonl"
        echo "running ${route} ${i} ..." >&2
        if [ "$route" = mcp ]; then
          prompt="Use the tax-calendar MCP tool to find the last day of UK tax year 2025/26. ${task}"
          extra=(--allowedTools "${base},mcp__tax-calendar__get_tax_year_dates" --disallowedTools "WebSearch,WebFetch,Agent")
        else
          prompt="Use the browser to find the last day of UK tax year 2025/26 on GOV.UK. ${task}"
          extra=(--chrome --allowedTools "${base},mcp__claude-in-chrome" --disallowedTools "WebSearch,WebFetch,Agent,mcp__tax-calendar__get_tax_year_dates")
        fi
        claude -p "$prompt" --output-format stream-json --verbose --permission-mode dontAsk "${model_args[@]}" "${extra[@]}" < /dev/null > "$out"
      done
    done
    node scripts/routes.mjs bench/results/routes-*.jsonl
    ;;
  *)
    echo "unknown scenario: $scenario (use haystack, agents or routes)" >&2
    exit 1
    ;;
esac
