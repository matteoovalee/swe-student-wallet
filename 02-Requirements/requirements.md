# Requirements: Student Wallet
 
FR = what the app does. NFR = how well it does it (always with a number or a check).
Every FR is linked to a user story in `user-stories.md`.
Home currencies supported: EUR, USD, CNY, INR and SAR (the same ones as in the survey and in the prototype).
 
## Functional requirements
 
| ID | Requirement | User story |
|----|-------------|------------|
| FR-01 | The app imports transactions from a CSV file with the columns date, merchant, amount, currency. | US-01 |
| FR-02 | The app assigns a category to every imported transaction automatically and marks it as "auto". | US-02 |
| FR-03 | The student can change the category of a transaction, and all totals are recalculated. | US-03 |
| FR-04 | The app shows spending per category for a chosen month, in MYR, as a chart and a table. | US-04 |
| FR-05 | The student can set a monthly budget in MYR, and the app shows the amount used and the amount left. | US-05 |
| FR-06 | The app calculates a forecast of the balance at the end of the month, in MYR and in the student's home currency, from the spending so far, and updates it when transactions change. | US-06 |
| FR-07 | The student can set a target exchange rate between MYR and their home currency, and the app sends an alert when the current rate (MYR received for 1 unit of home currency) reaches or passes it. If no target is set, the target is the average rate of the last 30 days. | US-07 |
| FR-08 | The student can export the transactions of a chosen period as a CSV file. | US-08 |
| FR-09 | The sponsor/parent can view the student's budget and spending progress in read-only mode, with no option to add, edit or delete data. | US-09 |
| FR-10 | The student can invite a sponsor/parent, and the sponsor sees data only after accepting. The student can remove access at any time. | US-10 |
| FR-11 | The admin can add, rename and remove categories, and removing a category requires moving its transactions to another category. | US-11 |
| FR-12 | The app gets the latest exchange rates between MYR and the home currencies (EUR, USD, CNY, INR, SAR) from the exchange-rate service at least once a day and keeps the last valid rates if a request fails. | US-12 |
| FR-13 | Users register and log in with an email and a password, and the app shows only the pages of their role (student, sponsor/parent or admin). | US-13 |
 
## Non-functional requirements
 
Type follows the lesson on NFRs: product, organizational or external.
 
| ID | Type | Category | Requirement |
|----|------|----------|-------------|
| NFR-01 | Product | Performance | The dashboard loads in under 3 seconds with 200 transactions. |
| NFR-02 | Product | Performance | Importing a CSV file with 500 rows takes under 10 seconds, including automatic categorisation. |
| NFR-03 | Product | Usability | A new student can import a CSV and see the spending by category within 5 minutes without help (tested with at least 5 users). |
| NFR-04 | Product | Security | Passwords are stored as salted hashes, and a sponsor/parent account can never change data (0 successful write requests in testing). |
| NFR-05 | Product | Reliability | The forecast and the rate alerts still work with the last stored rates when the exchange-rate service is unavailable for up to 48 hours. |
| NFR-06 | Organizational | Tools and process | The prototype is built in Python and Streamlit, uses only free APIs, and all project files are stored in the GitHub repository. The automatic tests run on every pull request and must pass before a merge. |
| NFR-07 | External | Privacy and data | The prototype uses only fake or anonymous data (0 real bank or card details), and the survey and user tests collect no names or emails. |
 
## What the app does NOT do
 
- It does not connect to a real bank or card account; all data comes from CSV files or manual input.
- It does not make real payments or money transfers; the rate alert only tells the student that the rate is good.
- It does not give financial advice; the forecast is only an estimate based on past spending.
- It does not support spending in currencies other than MYR; the home currencies (EUR, USD, CNY, INR, SAR) are used only for exchange rates and the forecast.
