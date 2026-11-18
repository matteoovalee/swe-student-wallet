# Sprint log

One short entry per sprint: what was planned, what was done, what we change. We do not hold separate meetings, so this log is our sprint review and retrospective.

## Sprint 1 (19-25 Oct): requirements

Planned: idea, user stories, functional and non-functional requirements, use case list, survey, test plan outline, app skeleton, exchange rates, wireframes, transactions CSV, slide template.

Done: user stories (#20, #22), requirements (#21), survey (#19), wireframes (#6), app skeleton (#17), exchange rates with cache (#18), slide template (#23), transactions CSV (#16). Not done: use case list (#5), test plan pull request (#12).

What went wrong: almost all work arrived after the deadline, and several pull requests needed changes before the merge (file in the wrong folder, wrong base currency, missing parts, Excel file instead of CSV).

What we change: issues with an example of the expected result, and a draft deadline in the middle of the sprint.

## Sprint 2 (26 Oct - 8 Nov): review

A two-week sprint, because the second week was the midterm exam week. No new issues: the first week went into reviewing the Sprint 1 pull requests, asking for changes and merging them (#16 to #23). In the midterm week there was no work on the project. Use case diagram, architecture and ER diagram did not start, so they move to Sprint 3.

## Sprint 3 (9-15 Nov): design and main screens

Planned: use case diagram, architecture, ER diagram, `categorize()` with TDD, CSV import and Dashboard, test cases, survey results. On 14 Nov we added the budget and the category correction, because the review showed that two requirements had no screen.

Done: use case diagram, architecture, ER diagram, categorize(), CSV import, Dashboard, test plan and test cases (#47, #48, #49, #50, #51, #56, #57, #58, #59, #63, #65, #60, #61). The budget and the category correction were not assigned, Matteo wrote them (#63, #65). Not done: survey results (#27) and pair programming (#33).

What went wrong: the test plan and the test cases arrived after the deadline, and the use case corrections went to the wrong branch. Two requirements were missing from the app until the review.

What we change: earlier deadlines, tests before code, and a public link to the app so that the user tests can start.

## Sixth member (11 Nov, Week 8)

Abrar (@ahnaf-297) joined on 11 Nov with the lecturer's approval, because he had no group and all the other groups already had five members. We are six (the brief says five). The other five keep their tasks and deadlines. Abrar's tasks start in Sprint 4: checking the repository and the app, two user test sessions and the GitHub screenshots for the report. Each one has a deadline before the end of the sprint. If a task is not done, another member does it and the issue gets the label `taken-over` and a comment with the date.

## Re-planning (7 Nov)

Two weeks are left before Week 10, so we have one sprint for design and the main screens (Sprint 3, 9-15 Nov) and one for the smart features, testing, report and slides (Sprint 4, 16-22 Nov). Sprint 5 is the submission week.

Scope of the prototype, by MoSCoW priority: we build the Must requirements first. Export (FR-08, Could) and sponsor invitations (FR-10, Should) stay in the requirements and in the use case diagram but are not built; the sponsor only gets a read-only demo account. Admin category management (FR-11) is built only if Sprint 4 has time. The traceability matrix marks what is not implemented.

The use case list of #5 is now inside the use case diagram issue, so Hizkia can start drawing directly.

## Re-planning (18 Nov)

The lecturer moved the group presentation to Week 11. Sprint 4 stays as planned: the smart features, the user tests and the first version of the report. The report is written in one shared document and each member writes his own chapters. Sprint 5 is for the final report and the presentation.
