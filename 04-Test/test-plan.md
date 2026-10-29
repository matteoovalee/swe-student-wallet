# Student Wallet: Test Plan

## 1. Purpose and Scope

We will test Student Wallet to check that its features meet the requirements and that students can complete everyday tasks easily.

The tests will cover:

- Registration, login and access for student, parent/sponsor and admin accounts.
- Importing transactions from CSV files and exporting transactions for a selected period.
- Automatic expense categories, manual category changes, and monthly spending charts and totals.
- Monthly budgets, the amount spent and the amount remaining.
- End-of-month balance forecasts in MYR and the student's home currency.
- Daily exchange-rate updates, alerts based on a chosen target or the 30-day average, and saved rates when the service fails.
- Parent/sponsor invitations, acceptance, read-only access and removal of access.
- Admin category changes, including moving transactions before removing a category.

Real bank connections, payments and money transfers are outside the scope of this prototype.

## 2. How We Will Test

**Unit testing:** We will use pytest to check calculations and category rules separately. For example, a budget of RM2,000 with RM500 spent should leave RM1,500.

**Integration testing:** We will check that features work together. Importing transactions or changing categories should update the totals, budget display and forecast correctly.

**System testing:** We will test the whole app with correct and incorrect inputs, including wrong passwords, CSV files with missing columns and actions that a user's role does not allow.

We will also check the following requirements:

- The dashboard loads in under 3 seconds with 200 transactions.
- A 500-row CSV imports and receives categories in under 10 seconds.
- Passwords are stored as salted hashes, and parent/sponsor accounts cannot change student data.
- Forecasts and alerts use the last saved rates during a simulated service outage of up to 48 hours.

**User acceptance testing (UAT):** At least five students will try the app with fake data. We will check whether a new user can import a CSV and view spending by category within five minutes without help. We will record task completion, difficulties and feedback without collecting names or emails.

## 3. Test Environment and Data

We will test the Python and Streamlit app on team laptops and the online version, recording the browser, operating system and app version for each session.

Test data will include fake transactions, valid and invalid CSV files, controlled exchange rates and dummy accounts for each role. No real bank or card details will be used. Currency checks will cover MYR, EUR, USD, CNY, INR and SAR.

Automatic tests must pass on each pull request before merging.

## 4. Proposed Responsibilities

| Member | Testing responsibility |
|---|---|
| Abbod | Prepare test cases, organise system tests, record results and bugs, and retest fixes. |
| Xiang | Run code-level and integration tests, investigate bugs and fix the code. |
| Hizkia | Check that the tests cover the requirements and user stories. |
| Sai | Check screen behaviour and help with usability testing. |
| Matteo | Review the plan, coordinate the team and review remaining issues. |

The team will confirm these responsibilities and help test the app.

## 5. Schedule

| Dates in 2026 | Planned work |
|---|---|
| 2-8 November, Sprint 3 | Write test cases, prepare data, and start unit and integration tests as features become available. |
| 9-12 November, Sprint 4 | Run system and user tests, check performance and permissions, and record bugs. |
| 13-15 November, Sprint 4 | Fix and retest bugs, check affected features again, and complete the test records. |

## 6. Results and Completion

In Sprint 3, each test case will include its requirement, steps, expected and actual results, and a status of Pass, Fail or Blocked.

We will keep records in `04-Test/` and report bugs through GitHub issues with steps to reproduce them. Before finishing, all planned tests must have a recorded status, critical bugs must be fixed and retested, and remaining limitations must be documented for team review.
