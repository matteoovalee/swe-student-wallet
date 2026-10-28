# User Stories: Student Wallet

Priority uses MoSCoW (Must, Should, Could, Won't).

| ID | As a | I want | So that | Priority | Acceptance criteria |
|----|------|--------|---------|----------|---------------------|
| US-01 | student | to import my transactions from a CSV file | I don't have to type every expense | Must | I upload a valid CSV and all rows show up in my transaction list |
| US-02 | student | my expenses to be sorted into categories automatically | I don't have to label each one myself | Must | After an import, every transaction has a category, and I can see which ones were assigned automatically |
| US-03 | student | to correct the category of a transaction | my reports stay accurate when the app guesses wrong | Should | I change a category, and the transaction and all totals update straight away |
| US-04 | student | to see my spending by category for a chosen month | I know where my money goes | Must | I pick a month and see a chart and a table of totals per category in MYR, and the totals add up to the month's spending |
| US-05 | student | to set a monthly budget in MYR | I can control how much I spend | Must | I save a budget amount, and the app shows how much of it I have used and how much is left |
| US-06 | student | to see a forecast of my balance at the end of the month | I know whether my money will last until the next transfer | Must | The app shows a projected end-of-month balance based on my spending so far, and it updates when I add new transactions |
| US-07 | student | to be alerted when the EUR to MYR exchange rate is good | I can transfer money from home at a better moment | Should | I set a target rate, and when the current rate reaches or passes it, I receive an alert showing the rate and the time |
| US-08 | student | to export my transactions | I can keep my own records offline | Could | I click export and download a CSV with all transactions for the selected period |
| US-09 | sponsor/parent | to view the student's budget and how much of it is used | I can see that the money I send is being managed | Must | After I log in, I see the student's monthly budget and spending progress, and I have no button to add, edit or delete anything |
| US-10 | sponsor/parent | access to be given only when the student agrees | the student's privacy is respected | Should | The student sends an invitation, I can see data only after I accept, and the student can remove my access at any time |
| US-11 | admin | to add, rename and remove spending categories | the category list stays useful for all students | Must | After I edit a category, it is available to all users, and removing one asks me to move its existing transactions to another category |
| US-12 | exchange-rate service | to deliver the latest EUR to MYR rate to the app on a regular basis | forecasts and rate alerts use current data | Must | The app gets and stores a new rate at least once a day, and keeps the last valid rate if a request fails |

## Notes

- Roles covered: student (US-01 to US-08), sponsor/parent (US-09, US-10), admin (US-11), exchange-rate service (US-12).
- MoSCoW count: Must 8, Should 3, Could 1 (12 stories in total).
