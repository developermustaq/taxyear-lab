// Returns the UK tax year a date falls in, for example "2025/26".
// The UK tax year runs from 6 April to 5 April. Dates are treated as UTC.
export function taxYear(date: Date): string {
  const year = date.getUTCFullYear();
  const month = date.getUTCMonth();
  const startsThisYear = month > 3 || (month === 3 && date.getUTCDate() >= 6); // 6 April onwards
  const start = startsThisYear ? year : year - 1;
  const end = String((start + 1) % 100).padStart(2, "0");
  return `${start}/${end}`;
}
