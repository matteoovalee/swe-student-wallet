# Student Wallet — User Acceptance Test Results

Date: 23 November 2026  
Related issue: #41  
Related test case: TC-19 / NFR-03

## Participants and evidence source

Five students from Taylor's University participated, identified anonymously as P1–P5. Names and email addresses are excluded. The observations below are session notes, not participant quotations.

Abbod confirmed that all five participants were international students from Taylor's University and first-time users of the application.

## Test setup

- Application: https://swe-student-wallet-group4.streamlit.app/
- Account: Student demo account.
- Browser: Microsoft Edge; window approximately 1,040 pixels wide.
- Input: combined-import-tests.csv, containing four September and two October transactions. The 500-transaction file was not used.
- Home currency: EUR.
- Forecast as of: 2026-09-20.

## Procedure

The five participants completed their sessions consecutively using the same signed-in account and browser session. Each participant uploaded the CSV and selected Confirm import. Account state was not isolated between sessions; the previous exchange-rate target remained saved until replaced.

Timing started when Upload was selected and ended when September's Food spending was identified. It included file selection, preview, confirmation, navigation, month selection and page-update delays. Times are reproduced as supplied; the timing instrument and its precision were not documented.

The forecast describes the estimated balance at the end of September, rather than the balance on 20 September.

## Results

| Participant | Time to identify Food (seconds) | Food spending | Within 5 minutes | End-of-September forecast | Saved target (MYR per EUR) | Transfer status shown |
|---|---:|---:|---|---:|---:|---|
| P1 | 66.008 | RM65 | Yes | EUR -33.20 | 4.5000 | Good time to transfer |
| P2 | 66.003 | RM65 | Yes | EUR -33.20 | 4.6000 | Below your target |
| P3 | 58.515 | RM65 | Yes | EUR -33.20 | 4.4000 | Good time to transfer |
| P4 | 58.502 | RM65 | Yes | EUR -33.20 | 4.7000 | Below your target |
| P5 | 65.593 | RM65 | Yes | EUR -33.20 | 4.5100 | Good time to transfer |

All five sessions reportedly included successful CSV import confirmation, viewing the forecast for the requested date and saving an exchange-rate target. No external assistance was reported during the timed tasks.

The application reportedly displayed 1 EUR = 4.5177 MYR, dated 23 November 2026 and attributed to Frankfurter. Only alert targets were saved; no financial transfers occurred.

In every session, the displayed recorded balance was RM -100.00, expected additional spending through month end was RM50.00, estimated balance on 30 September was RM -150.00 and the EUR estimate was -33.20.

## Session observations

- P1: Import succeeded and the correct Food amount appeared after September was selected. October was initially selected; navigation and import required a short update delay.
- P2: Opening Forecast and alerts reset the forecast date to 23 November while retaining the previous target. The required date and a new target were set for the session.
- P3: Some budget and spending cards truncated values at the tested width. The By category table displayed the full Food amount.
- P4: After changing the month, previous figures and layout briefly remained. Results were recorded after the page settled.
- P5: The alert used the current November exchange rate while the September date controlled the balance forecast. Clearer wording could help explain the distinction.

## Interpretation and limitations

Reported task completion: 5/5 identified the correct September Food amount within five minutes. Mean time: 62.924 seconds; range: 58.502–66.008 seconds. These values summarize only the supplied sessions.

Shared account state and saved settings meant starting conditions were not identical. All participants used EUR. Whether the expected Food total was known to participants before testing was not recorded. No independent session recordings or additional participant feedback were supplied with these results.

The observations identify possible improvements to date persistence, default-month clarity, complete values on narrow windows and the distinction between forecast and exchange-rate dates. They do not establish that improvements have been implemented or retested.

TC-19 / NFR-03 status: Pass, based on the supplied session records and confirmed participant eligibility. All five first-time international student participants imported the CSV and identified the correct September Food amount within five minutes without reported assistance. Execution date: 23 November 2026.
