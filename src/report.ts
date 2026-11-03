import { taxYear } from "./taxYear.js";

export interface Payment {
  client: string;
  paidOn: string; // ISO date, YYYY-MM-DD
  pence: number;
}

// Groups payments by tax year and totals them in pence.
export function totalsByTaxYear(payments: Payment[]): Record<string, number> {
  const totals: Record<string, number> = {};
  for (const p of payments) {
    const year = taxYear(new Date(p.paidOn));
    totals[year] = (totals[year] ?? 0) + p.pence;
  }
  return totals;
}
