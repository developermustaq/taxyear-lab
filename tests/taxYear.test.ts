import { describe, expect, it } from "vitest";
import { taxYear } from "../src/taxYear.js";
import { totalsByTaxYear } from "../src/report.js";

describe("taxYear", () => {
  it("puts a June date in the tax year that started that April", () => {
    expect(taxYear(new Date("2026-06-01"))).toBe("2026/27");
  });

  it("puts a January date in the tax year that started the previous April", () => {
    expect(taxYear(new Date("2026-01-15"))).toBe("2025/26");
  });

  it("starts a new tax year on 6 April", () => {
    expect(taxYear(new Date("2026-04-06"))).toBe("2026/27");
  });

  it("pads the end year", () => {
    expect(taxYear(new Date("2008-05-01"))).toBe("2008/09");
  });
});

describe("totalsByTaxYear", () => {
  it("totals payments per tax year in pence", () => {
    const totals = totalsByTaxYear([
      { client: "Client A", paidOn: "2026-02-10", pence: 12000 },
      { client: "Client B", paidOn: "2026-03-20", pence: 3000 },
      { client: "Client A", paidOn: "2026-07-01", pence: 5000 },
    ]);
    expect(totals).toEqual({ "2025/26": 15000, "2026/27": 5000 });
  });
});
