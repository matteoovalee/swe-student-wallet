# Simulated transactions

`transactions.csv` holds 200 simulated transactions for a Taylor's international student, from 1 Aug to 24 Oct 2026. The data is made up. It is only used to demo and test the prototype, no real person or bank account is behind it.

Columns: `date` (YYYY-MM-DD), `merchant`, `amount`, `currency`.
- All amounts are in MYR.
- Expenses are negative, transfers from home are positive (`TRANSFER FROM HOME`).
- There is no category column on purpose: the app assigns categories by keyword rules on `merchant` (smart feature 1).

Author: Sai (UI/UX design). Closes issue #9.
