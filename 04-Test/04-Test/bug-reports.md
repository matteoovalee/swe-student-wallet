# Bug reports ready for GitHub

These drafts have NOT been posted. Apply the bug label and retain the TC ID in the title.

## TC-09: Clearing a saved exchange-rate target restores the previous value

Related requirements:FR-07. Manual execution:22November2026. Source reviewed:e87ecd4436c2fab5e6d89f52394871a2a5afa077.

1. Sign in as Student and open Forecast and alerts.
2. Select EUR, enter5MYR perEUR and Save target.
3. Clear the input and Save target again.

Expected: custom target clears; default returns to the displayed30-day average (4.5393 in the session).

Actual: input returns to5.0000 and the alert keeps comparing with5. The tester repeated the attempt with the same result.

Evidence: image(20261122-154709).png; current quote4.5177. Fresh-session averaging and boundary checks pass but do not resolve this clearing failure. Retest after a fix is pending.

## TC-22: Main-branch ruleset does not require passing automated tests

Related requirement:NFR-06. Review date:23November2026.

1. Review `.github/workflows/tests.yml`: tests run on pull requests and pushes to main.
2. Review active repository ruleset25620527 (protect-main).

Expected: the pytest check must pass before merging into main.

Actual: ruleset requires one approval and blocks deletion/non-fast-forward updates, but contains no required_status_checks rule. Successful individual workflow runs do not enforce the merge gate.

Evidence: https://github.com/matteoovalee/swe-student-wallet/rules/25620527 and workflow source at e87ecd4436c2fab5e6d89f52394871a2a5afa077. Repository administrator action is needed; retest after configuration changes is pending.
