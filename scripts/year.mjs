// Print the tax year for one or more dates: npm run year -- 2026-04-05
import { taxYear } from "../src/taxYear.ts";

for (const d of process.argv.slice(2)) console.log(`taxYear(${d}) = ${taxYear(new Date(d))}`);
