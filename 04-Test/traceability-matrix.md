# Student Wallet Traceability Matrix

This is the first mapping of requirements to user stories, use cases and test cases. Pending means the case still needs to be run. The final matrix, with the results, comes with issue #42.

Sources: [requirements](../02-Requirements/requirements.md), [user stories](../02-Requirements/user-stories.md), [use case diagram](../02-Requirements/use-case-diagram.drawio.svg) and [use case descriptions](../02-Requirements/use-case-descriptions.md). The test cases are in [test-cases.md](test-cases.md).

The last column lists the pytest files that already check the requirement automatically (in `05-Final/prototype/tests/`). A dash means there is no automated test yet.

## Functional requirements

| Requirement | User story | Use case | Test cases | Automated tests | Status |
|---|---|---|---|---|---|
| FR-01 | US-01 | UC-02 | TC-01, TC-02 | - | Pending |
| FR-02 | US-02 | UC-03 | TC-03 | test_categorize.py, test_category_edit.py | Pending |
| FR-03 | US-03 | UC-05 | TC-04 | test_category_edit.py, test_dashboard.py | Pending |
| FR-04 | US-04 | UC-04 | TC-05 | test_dashboard.py | Pending |
| FR-05 | US-05 | UC-06 | TC-06 | test_budget.py, test_dashboard.py | Pending |
| FR-06 | US-06 | UC-07 | TC-07 | - | Pending |
| FR-07 | US-07 | UC-08, UC-10 | TC-08, TC-09 | - | Pending |
| FR-08 | US-08 | UC-14 | TC-10 | - | Not implemented |
| FR-09 | US-09 | UC-12 | TC-11 | - | Pending |
| FR-10 | US-10 | UC-11 | TC-12 | - | Not implemented |
| FR-11 | US-11 | UC-13 | TC-13 | - | Pending |
| FR-12 | US-12 | UC-09 | TC-14 | - | Pending |
| FR-13 | US-13 | UC-01 | TC-15, TC-16 | - | Pending (registration not built) |

## Non-functional requirements

| Requirement | User story | Use case | Test cases | Automated tests | Status |
|---|---|---|---|---|---|
| NFR-01 | - | UC-04 | TC-17 | - | Pending |
| NFR-02 | - | UC-02, UC-03 | TC-18 | - | Pending |
| NFR-03 | - | UC-02, UC-04 | TC-19 | - | Pending |
| NFR-04 | - | UC-01, UC-12 | TC-20 | - | Pending |
| NFR-05 | - | UC-07, UC-09, UC-10 | TC-21 | - | Pending |
| NFR-06 | - | - | TC-22 | - | Pending |
| NFR-07 | - | - | TC-23 | - | Pending |
