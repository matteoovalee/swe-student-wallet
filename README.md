# Student Wallet (two currencies)

Group project for Principles of Software Engineering, Taylor's University, Sep 2026 intake.
Domain: Smart Financial.

## What it is

A web app for international students who spend in MYR with money that comes from home (EUR and others). It sorts expenses into categories automatically, forecasts the end-of-month balance in the home currency, and alerts the student when the exchange rate is good for a transfer.

Actors: student, sponsor/parent (read-only), admin, exchange-rate service (external).

Smart features:
1. Automatic expense categorisation (keyword rules on the merchant name)
2. End-of-month balance forecast in the home currency
3. "Good time to transfer" alert when the rate is above its 30-day average (a rule, not a prediction)

## Team

| Area | Member | GitHub |
|---|---|---|
| Lead, planning, architecture, review | Matteo | @matteoovalee |
| Requirements and use cases | | |
| UI/UX design | | |
| Development | | |
| Testing | | |

## Repository structure

The folders follow the SDLC phases required by the assignment.

| Folder | Phase | Content |
|---|---|---|
| `01-Planning` | Planning | team and roles, timeline, meeting notes |
| `02-Requirements` | Requirements | user stories, functional and non-functional requirements, use case diagram and descriptions |
| `03-Design` | Design | architecture, ER and sequence diagrams, wireframes, mockups |
| `04-Test` | Test | test plan, test cases, test results, traceability matrix |
| `05-Final` | Final | final prototype (`prototype/`) |

## How we work

- Scrum with one-week sprints. Each sprint is a GitHub milestone and the backlog is the GitHub Project board.
- One issue per task. Labels: the SDLC phase (`planning`, `requirements`, `design`, `prototype`, `testing`) and MoSCoW priority where it applies.
- One branch per task, named `<phase>/<issue-number>-<short-name>`, for example `requirements/12-user-stories`.
- Work reaches `main` only through a pull request that Matteo reviews. The PR says which issue it closes.
- Commit messages start with a prefix: `req:`, `design:`, `test:`, `proto:`, `docs:`, `chore:`.
- At the end of each sprint `main` gets a tag and a release: `v0.1-requirements`, `v0.2-design`, `v0.3-alpha`, `v0.4-tested`, `v1.0-final`.

## Tools

GitHub (repo, issues, Project board, Actions), draw.io (diagrams saved as `.drawio.svg`), Figma (wireframes), Google Forms (survey and UAT), Python and Streamlit (prototype), pytest (tests).

## Run the prototype

See `05-Final/prototype/README.md`.
