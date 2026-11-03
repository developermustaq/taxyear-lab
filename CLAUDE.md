# taxyear-lab

A tiny sandbox with one bug. Synthetic data only: clients are "Client A", "Client B".

## Rules

- The UK tax year runs from 6 April to 5 April. 5 April is the last day of the old year.
- Tax years are written `2025/26`: four-digit start year, slash, two-digit end year.
- Money is integer pence. Never use floats for money.
- Dates are UTC. Use `getUTC*` methods.
- Run `npm test` after every change and show the output.
- Do not change the public signature of `taxYear(date: Date): string`.
