# Use case descriptions: Student Wallet

One description for every use case in `use-case-diagram.drawio.svg`, in the same order (UC-01 to UC-14). US, FR and NFR numbers refer to `user-stories.md` and `requirements.md`.

The included and extending use cases (UC-03, UC-05, UC-10) are shorter: when they happen and their steps.

Three use cases are in the requirements but are not built in the prototype (see `01-Planning/sprint-log.md`, 7 Nov): UC-11 and UC-14, and UC-13 only if Sprint 4 has time. Their descriptions say what the full app does.

### UC-01 Log in
- Actor: Student, Sponsor/parent, Admin
- Goal: enter the app and see only the pages of the user's role
- Related: US-13, FR-13, NFR-04
- Preconditions: the user has an account (in the prototype: one of the demo accounts)
- Main flow:
  1. The user opens the app and sees the login form.
  2. The user enters an email and a password.
  3. The app checks the password against the salted hash stored for that email.
  4. The app opens the pages of the user's role: student pages, the sponsor's read-only view, or the admin pages.
- Alternative flows:
  - 1a. The user has no account: the user registers with an email and a password, then logs in.
  - 3a. The email or the password is wrong: the app shows an error and gives no access. The user can try again.
- Postconditions: the user is logged in and the sidebar shows only the pages of their role.
- Prototype: only the three demo accounts exist. Registration (1a) is not built.

### UC-02 Import transactions from CSV
- Actor: Student
- Goal: load bank transactions into the app without typing them
- Related: US-01, FR-01, NFR-02, NFR-03
- Preconditions: the student is logged in (UC-01)
- Main flow:
  1. The student opens the Transactions page and chooses a CSV file.
  2. The app checks that the file has the columns date, merchant, amount, currency.
  3. The app gives each transaction a category (includes UC-03).
  4. The app shows a preview with the categories.
  5. The student confirms and the transactions are saved.
- Alternative flows:
  - 2a. A column is missing: the app shows which one and imports nothing.
  - 2b. A row has a date or an amount that is not valid: the app shows the line numbers and imports nothing.
  - 2c. A row is in a currency other than MYR: the row is imported, but only MYR expenses are counted in the totals.
  - 5a. The student cancels: nothing is saved.
- Postconditions: the transactions appear in the list and in the totals.

### UC-03 Categorise transactions automatically
- Included by: UC-02 (step 3), for every row of the file
- Related: US-02, FR-02, NFR-02
- Steps:
  1. The app reads the merchant name in capital letters.
  2. It looks for the keywords of each category as whole words, for example GRAB is Transport and SPOTIFY is Subscriptions.
  3. The first category with a matching keyword is given to the transaction, marked "auto".
  4. If no keyword matches, the category is "Other".
- Postconditions: every imported transaction has a category marked "auto".

### UC-04 View spending by category
- Actor: Student
- Goal: see where the money went in a month
- Related: US-04, FR-04, NFR-01
- Preconditions: the student is logged in (UC-01)
- Main flow:
  1. The student opens the Dashboard.
  2. The student chooses a month.
  3. The app adds up the MYR expenses of that month for each category.
  4. The app shows the total spending of the month, a chart and a table of the totals per category in MYR.
- Alternative flows:
  - 1a. The student has not imported any transactions yet: the app shows the sample data and a message that points to the Transactions page.
  - 3a. The month has no MYR expenses: the app says so and shows no chart.
  - 4a. A transaction is in the wrong category: the student can correct it (extended by UC-05).
- Postconditions: the category totals add up to the total spending of the month.

### UC-05 Correct a category
- Extends: UC-04, when the student sees a transaction in the wrong category
- Related: US-03, FR-03
- Steps:
  1. The student chooses the transaction and picks another category from the list.
  2. The app saves the new category and marks it as "manual" instead of "auto".
  3. The app recalculates the totals, the chart and the table.
- Postconditions: the transaction and all totals use the new category.

### UC-06 Set monthly budget
- Actor: Student
- Goal: decide how much to spend in a month and follow it
- Related: US-05, FR-05
- Preconditions: the student is logged in (UC-01)
- Main flow:
  1. The student opens the budget field on the Dashboard.
  2. The student enters an amount in MYR and saves it.
  3. The app checks that the amount is a number above zero.
  4. The app saves the budget and shows the amount used and the amount left for the month.
- Alternative flows:
  - 3a. The amount is empty, zero or not a number: the app shows an error and saves nothing.
  - 4a. The spending is above the budget: the amount left is shown as a negative number in red.
- Postconditions: the budget is saved, and the sponsor can see it (UC-12).

### UC-07 View end-of-month forecast
- Actor: Student
- Goal: know if the money will last until the next transfer from home
- Related: US-06, FR-06, NFR-05
- Preconditions: the student is logged in (UC-01) and has transactions in the month shown (by default the latest month with data)
- Main flow:
  1. The student opens the Forecast and alerts page and chooses a home currency (EUR, USD, CNY, INR or SAR).
  2. The app calculates the balance expected at the end of that month in MYR, from the spending so far.
  3. The app converts the forecast to the home currency with the current rate (forecast in MYR divided by the rate, because the rate is the MYR received for 1 unit of the home currency).
  4. The app shows the forecast in MYR and in the home currency, with the date of the rate.
- Alternative flows:
  - 2a. There are no transactions in that month: the app shows a message and no forecast.
  - 3a. The exchange-rate service is not available: the app uses the last stored rates and says so on the screen (NFR-05).
- Postconditions: the forecast is shown, and it changes when the transactions change.

### UC-08 Set target exchange rate
- Actor: Student
- Goal: choose the rate at which a transfer from home is worth it
- Related: US-07, FR-07
- Preconditions: the student is logged in (UC-01)
- Main flow:
  1. The student opens the Forecast and alerts page.
  2. The app shows the current rate (MYR received for 1 unit of the home currency) and the average of the last 30 days.
  3. The student enters a target rate and saves it.
  4. The app saves the target. From now on, new rates are compared with it (UC-10).
- Alternative flows:
  - 3a. The student leaves the field empty: the target is the 30-day average.
  - 3b. The value is not a number above zero: the app shows an error and keeps the old target.
- Postconditions: the target rate is saved for the student's home currency.

### UC-09 Update exchange rates
- Actor: Exchange-rate service (external system, frankfurter.dev)
- Started by: the app, at least once a day
- Goal: keep the rates between MYR and the home currencies up to date
- Related: US-12, FR-12, NFR-05
- Preconditions: none
- Main flow:
  1. At least once a day, the app asks the service for the rates between MYR and EUR, USD, CNY, INR and SAR.
  2. The service sends the rates and their date.
  3. The app stores the rates and keeps the last 30 days for the average.
  4. The app checks the new rates against the targets (extended by UC-10).
- Alternative flows:
  - 2a. The service does not answer or sends an error: the app keeps the last valid rates and shows their date.
  - 2b. No rates were ever stored: the app uses the saved demo rates and says that they are not live.
- Postconditions: the latest valid rates are stored.

### UC-10 Send rate alert
- Extends: UC-09, after new rates are stored, when the current rate reaches or passes the student's target (or the 30-day average if no target is set)
- Related: US-07, FR-07, NFR-05
- Steps:
  1. The app compares the current rate with the target of each student for that home currency.
  2. When the rate is equal to or above the target, the app shows an alert with the rate and the time, for example "Good time to transfer: 1 EUR = x MYR, above your target".
- Postconditions: the student sees the alert on the Forecast and alerts page.

### UC-11 Invite sponsor
- Actor: Student (sends the invitation), Sponsor/parent (accepts it)
- Goal: let a parent or sponsor follow the budget, only with the student's agreement
- Related: US-10, FR-10
- Preconditions: the student is logged in (UC-01)
- Main flow:
  1. The student enters the email of the sponsor and sends an invitation.
  2. The sponsor receives the invitation and accepts it.
  3. The app links the sponsor's account to the student in read-only mode.
- Alternative flows:
  - 2a. The sponsor does not accept: the sponsor sees no data.
  - 3a. Later, the student removes the access: from that moment the sponsor sees no data.
- Postconditions: the sponsor can view the student's budget (UC-12).
- Prototype: not built. The demo sponsor account is already linked to the demo student.

### UC-12 View student budget
- Actor: Sponsor/parent
- Goal: check that the money sent is being managed
- Related: US-09, FR-09, NFR-04
- Preconditions: the sponsor is logged in (UC-01) and linked to the student (UC-11)
- Main flow:
  1. The sponsor opens the Dashboard.
  2. The app shows the student's monthly budget, the amount used and left, and the spending by category.
  3. The sponsor can choose another month.
- Alternative flows:
  - 2a. The student has not set a budget: the app shows the spending only, with a message that no budget is set.
  - 2b. The sponsor tries to change data: there is no button to add, edit or delete, and the app refuses any write request.
- Postconditions: no data is changed.

### UC-13 Manage categories
- Actor: Admin
- Goal: keep the category list useful for all students
- Related: US-11, FR-11
- Preconditions: the admin is logged in (UC-01)
- Main flow:
  1. The admin opens the Categories page and sees the list of categories.
  2. The admin adds a new category, or renames one.
  3. The app saves the change and it is available to all users.
- Alternative flows:
  - 2a. The name already exists: the app shows an error and saves nothing.
  - 2b. The admin removes a category: the app asks for the category that will receive its transactions, moves them, then removes the category.
  - 2c. The admin cancels the removal: nothing changes.
- Postconditions: the category list is updated for all users.
- Prototype: built only if Sprint 4 has time.

### UC-14 Export transactions
- Actor: Student
- Goal: keep a copy of the transactions offline
- Related: US-08, FR-08
- Preconditions: the student is logged in (UC-01)
- Main flow:
  1. The student chooses a period and clicks Export.
  2. The app creates a CSV file with the columns date, merchant, amount, currency and category.
  3. The student downloads the file.
- Alternative flows:
  - 2a. There are no transactions in the period: the app says so and creates no file.
- Postconditions: the student has a CSV file of the period.
- Prototype: not built.
