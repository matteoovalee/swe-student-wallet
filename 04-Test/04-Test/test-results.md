# Student Wallet — Test Results

Execution:22–23 November2026. Source reviewed and executed: `e87ecd4436c2fab5e6d89f52394871a2a5afa077`.

Manual app testing was performed by Abbod and assessed from screenshots, exported CSVs and his observations. UAT records were supplied by Abbod, who confirmed five actual first-time international students from Taylor’s. Automated verification was run separately in a local Linux/Python3.12 environment. These sources are not interchangeable.

## Outcomes

| Status | Cases | Count |
|---|---|---:|
| Pass | TC-01–TC-08,TC-11,TC-14–TC-21,TC-23 |18|
| Fail | TC-09,TC-22 |2|
| Not implemented | TC-10,TC-12,TC-13 |3|

Full actual results, dates and evidence sources are in [test-cases.md](test-cases.md). No retest after a production fix has been completed. Conditional/component checks are described explicitly in each row.

## Existing automated suite

Command: `python3 -m pytest -q` from `05-Final/prototype`.

Result: **76 passed,1 warning in4.31seconds**. See [pytest-final.txt](pytest-final.txt). The warning is from the environment’s AnyIO pytest plugin; it did not fail a test. This result does not override manual defects or missing features.

Environment: Python3.12,pytest9.2.0,Streamlit1.67.0,pandas3.1.1,Altair6.3.0. Dependencies were installed to satisfy the repository requirements. Existing source and tests were not modified.

## Supplemental verification

[supplemental-checks.txt](supplemental-checks.txt) records controlled conversion, rendered alert boundaries, two-day cache updates, simulated24/48-hour outage behavior, salted hashes, Sponsor guards and privacy review. These automated checks were separate from the student sessions. [supplemental-checks.py](supplemental-checks.py) contains the executed harness; its source root is environment-specific and must be adjusted for another checkout. Test fixtures and caches were local; no production service was disabled.

TC-07 UI used the real displayed rate and produced EUR88.54/EUR55.34. Controlled function conversion separately returned the specified EUR80/EUR50 at a fixed quote. TC-08 AppTest exercised4.99/5.00/5.01 against target5. Fresh blank-target averaging passed, but TC-09 remains failed because clearing a previously saved target did not work in the manual session.

## Evidence and limitations

Screenshots supplied by Abbod are in [evidence/](evidence/). Synthetic fixtures are in [fixtures/](fixtures/). Expected results were retained from the original test-case document.

TC-17 used201 rows rather than200; TC-17/18 times are approximate tester observations, not instrumented measurements. No exact subsecond timing is claimed. UAT timings retain the values supplied; the instrument and precision were not documented. Participants shared a session, used EUR and encountered carried-over settings. See [uat-results.md](uat-results.md).

Source review confirms that category-list management, selected-period CSV export, sponsor invitations and registration are absent. Reassigning a transaction category and downloading a generic table are distinct features.

TC-22: active ruleset [protect-main](https://github.com/matteoovalee/swe-student-wallet/rules/25620527) requires one PR approval but no required status checks. [PR workflow run45045484077](https://github.com/matteoovalee/swe-student-wallet/actions/runs/45045484077) completed successfully; enforcement is still missing. Frankfurter documents its public API as free, with no API key: https://frankfurter.dev/ (reviewed23November2026).

## Defects and follow-up

- TC-09: saved custom target cannot be cleared back to the average. Retest pending after a fix.
- TC-22: passing automated checks are not required by the active main-branch ruleset. Recheck after repository administrator adds the required workflow check.
- TC-13: admin category management is not implemented.

Ready-to-post bug descriptions are in [bug-reports.md](bug-reports.md). Direct GitHub creation returned403 Resource not accessible by integration; no issues or PR were created during this verification session. Earlier PR83 was closed without merge, so it is not a completed submission.
