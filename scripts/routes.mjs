// Compare the browser and MCP routes from `claude -p --output-format stream-json --verbose` runs.
// Usage: node scripts/routes.mjs bench/results/routes-*.jsonl
// Prints one row per run, then the median of each route.
import { readFileSync } from "node:fs";
import { basename } from "node:path";

const rows = process.argv.slice(2).map((file) => {
  const events = readFileSync(file, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
  const r = events.find((e) => e.type === "result") ?? {};
  const u = r.usage ?? {};
  const tokens = (u.input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0) + (u.output_tokens ?? 0);
  const blocks = events.flatMap((e) => (Array.isArray(e.message?.content) ? e.message.content : []));
  const toolCalls = blocks.filter((b) => b.type === "tool_use").length;
  // A wrong action is a tool call that failed or was denied.
  const failed = blocks.filter((b) => b.type === "tool_result" && b.is_error).length;
  const text = r.result ?? "";
  const route = basename(file).includes("browser") ? "browser" : "mcp";
  // The run only counts if it actually used its route's tools, not memory.
  const prefix = route === "browser" ? "mcp__claude-in-chrome__" : "mcp__tax-calendar__";
  const routeCalls = blocks.filter((b) => b.type === "tool_use" && b.name.startsWith(prefix)).length;
  // Correct: used its route, names 5 April 2026 as the last day, and says taxYear() gives 2026/27 for it.
  const correct = routeCalls > 0 && /(5 April 2026|2026-04-05|April 5, 2026)/.test(text) && /2026\/27/.test(text);
  return {
    run: basename(file, ".jsonl"),
    route,
    routeCalls,
    turns: r.num_turns ?? 0,
    tokens,
    seconds: Math.round((r.duration_ms ?? 0) / 1000),
    toolCalls,
    failed,
    correct,
  };
});

const fmt = (v) => (typeof v === "number" ? v.toLocaleString("en-GB") : String(v));
const cols = ["run", "turns", "tokens", "seconds", "toolCalls", "routeCalls", "failed", "correct"];
const print = (list) => {
  const widths = cols.map((c) => Math.max(c.length, ...list.map((r) => fmt(r[c]).length)));
  for (const r of [Object.fromEntries(cols.map((c) => [c, c])), ...list]) {
    console.log(cols.map((c, i) => fmt(r[c])[i === 0 ? "padEnd" : "padStart"](widths[i])).join("  "));
  }
};
print(rows);

const median = (xs) => {
  const s = [...xs].sort((a, b) => a - b);
  return s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2;
};
console.log("\nmedians");
print(
  ["browser", "mcp"]
    .map((route) => rows.filter((r) => r.route === route))
    .filter((list) => list.length)
    .map((list) => ({
      run: `${list[0].route} (n=${list.length})`,
      turns: median(list.map((r) => r.turns)),
      tokens: median(list.map((r) => r.tokens)),
      seconds: median(list.map((r) => r.seconds)),
      toolCalls: median(list.map((r) => r.toolCalls)),
      routeCalls: median(list.map((r) => r.routeCalls)),
      failed: median(list.map((r) => r.failed)),
      correct: `${list.filter((r) => r.correct).length}/${list.length}`,
    })),
);
