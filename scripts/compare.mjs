// Compare measured runs side by side: node scripts/compare.mjs bench/results/A.json bench/results/B.json
import { readFileSync } from "node:fs";
import { basename } from "node:path";

const rows = process.argv.slice(2).map((file) => {
  const r = JSON.parse(readFileSync(file, "utf8"));
  const u = r.usage ?? {};
  const main = (u.input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0);
  // modelUsage covers every model call in the run, subagents included.
  const all = Object.values(r.modelUsage ?? {}).reduce(
    (s, m) => s + (m.inputTokens ?? 0) + (m.cacheReadInputTokens ?? 0) + (m.cacheCreationInputTokens ?? 0) + (m.outputTokens ?? 0),
    0,
  );
  return [basename(file, ".json"), Object.keys(r.modelUsage ?? {}).join(","), main, all, r.subagent_stats?.spawned ?? 0, r.num_turns, Math.round((r.duration_ms ?? 0) / 1000)];
});

const head = ["run", "model", "input (main)", "all tokens", "subagents", "turns", "seconds"];
const fmt = (v) => (typeof v === "number" ? v.toLocaleString("en-GB") : v);
const widths = head.map((h, i) => Math.max(h.length, ...rows.map((r) => String(fmt(r[i])).length)));
const line = (cells) => cells.map((c, i) => String(fmt(c))[i < 2 ? "padEnd" : "padStart"](widths[i])).join("  ");
console.log("");
console.log(line(head));
console.log(widths.map((w) => "-".repeat(w)).join("  "));
for (const r of rows) console.log(line(r));
