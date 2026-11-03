// Print the numbers from one `claude -p --output-format json` result.
// Usage: node scripts/summarise-run.mjs <label> <result.json>

import { readFileSync } from "node:fs";

const [label, file] = process.argv.slice(2);
const r = JSON.parse(readFileSync(file, "utf8"));
const u = r.usage ?? {};
const mainInput = (u.input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0);
const models = r.modelUsage ?? {};
// modelUsage covers every model call in the run, subagents included.
const allTokens = Object.values(models).reduce(
  (sum, m) => sum + (m.inputTokens ?? 0) + (m.cacheReadInputTokens ?? 0) + (m.cacheCreationInputTokens ?? 0) + (m.outputTokens ?? 0),
  0,
);

console.log(`\n== ${label}`);
console.log(`  model(s)                    ${Object.keys(models).join(", ") || "unknown"}`);
console.log(`  input tokens (main session) ${mainInput.toLocaleString("en-GB")}`);
console.log(`  output tokens (main)        ${(u.output_tokens ?? 0).toLocaleString("en-GB")}`);
console.log(`  all tokens incl. subagents  ${allTokens.toLocaleString("en-GB")}`);
console.log(`  subagents spawned           ${r.subagent_stats?.spawned ?? 0}`);
console.log(`  model turns                 ${r.num_turns}`);
console.log(`  seconds                     ${Math.round((r.duration_ms ?? 0) / 1000)}`);
console.log(`  error                       ${r.is_error ? "YES" : "no"}`);
console.log(`\n${(r.result ?? "").split("\n").slice(0, 12).join("\n")}\n  …`);
