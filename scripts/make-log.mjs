// Generates logs/report-run.log: a noisy 2,000-line log with one real error.
// Deterministic, so every run of the workshop sees the same file.
import { writeFileSync } from "node:fs";

let seed = 7;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const clients = ["Client A", "Client B", "Client C", "Client D"];
const noise = [
  (i) => `INFO  cache hit key=rates:${i % 97}`,
  (i) => `DEBUG http GET /health 200 ${(rand() * 9 + 1).toFixed(1)}ms`,
  (i) => `INFO  loaded payment batch=${1000 + (i % 40)} rows=${Math.floor(rand() * 50) + 1}`,
  (i) => `WARN  slow query report_totals ${Math.floor(rand() * 400) + 600}ms (retrying not needed)`,
  (i) => `INFO  ${clients[i % 4]} totals recomputed`,
  (i) => `DEBUG gc pause ${(rand() * 3).toFixed(2)}ms`,
];

const lines = [];
const t0 = Date.UTC(2026, 3, 6, 2, 0, 0);
for (let i = 0; i < 2000; i++) {
  const ts = new Date(t0 + i * 1500).toISOString();
  const body =
    i === 1423
      ? "ERROR year-end check failed: Client B payment paidOn=2026-04-05 filed under 2026/27, expected 2025/26 (taxYear boundary)"
      : noise[Math.floor(rand() * noise.length)](i);
  lines.push(`${ts} ${body}`);
}
writeFileSync(new URL("../logs/report-run.log", import.meta.url), lines.join("\n") + "\n");
console.log(`wrote logs/report-run.log (${lines.length} lines, error at line 1424)`);
