#!/usr/bin/env bash
# Run once, from inside the cloned repo, after `gh auth login`.
# Creates labels, sprint milestones and the Sprint 1 issues.
set -euo pipefail

echo "Creating labels..."
mk() { gh label create "$1" --color "$2" --description "$3" --force >/dev/null; }
mk planning     000000 "SDLC phase: planning"
mk requirements 5319e7 "SDLC phase: requirements"
mk design       c5def5 "SDLC phase: design"
mk prototype    0052cc "SDLC phase: prototype"
mk testing      0e8a16 "SDLC phase: testing"
mk task         1d76db "A piece of work for a sprint"
mk must         b60205 "MoSCoW: must have"
mk should       d93f0b "MoSCoW: should have"
mk could        fbca04 "MoSCoW: could have"
mk wont         cccccc "MoSCoW: won't have this time"

echo "Creating milestones..."
# Deadlines are Sundays 21:00 Kuala Lumpur time (13:00 UTC)
ms() { gh api "repos/{owner}/{repo}/milestones" -f title="$1" -f due_on="$2" -f description="$3" >/dev/null; }
ms "Sprint 1" "2026-10-25T13:00:00Z" "Idea, user stories, requirements, use case list, survey online. Tag v0.1-requirements"
ms "Sprint 2" "2026-11-01T13:00:00Z" "Use cases, architecture, ER, wireframes, app skeleton. Tag v0.2-design"
ms "Sprint 3" "2026-11-08T13:00:00Z" "Core and smart features, test cases written. Tag v0.3-alpha"
ms "Sprint 4" "2026-11-15T13:00:00Z" "Test execution, UAT, fixes, retest. Tag v0.4-tested"
ms "Sprint 5" "2026-11-22T13:00:00Z" "Report, slides, rehearsals, freeze. Tag v1.0-final"

echo "Creating Sprint 1 issues..."
iss() { gh issue create --title "$1" --body "$2" --label "$3" --milestone "Sprint 1" >/dev/null; }

iss "Set up repo, board and rules for main" \
"Repo, folders, labels, milestones, Project board, rule that main only accepts pull requests.
Done by Matteo." "task,planning"
iss "Write the project plan" \
"Team and roles, sprint timeline, main activities.
Output: 01-Planning/project-plan.md" "task,planning"

iss "Write the user stories" \
"At least 10 user stories, each with an ID (US-01...), 'As a / I want / so that', MoSCoW priority and acceptance criteria. Cover all four actors (student, sponsor, admin, exchange-rate service).
Output: 02-Requirements/user-stories.md" "task,requirements"
iss "Write functional and non-functional requirements" \
"Functional requirements (FR-01...) linked to the user stories. Non-functional requirements (NFR-01...) with a measurable target each, for example 'dashboard loads in under 3 seconds with 200 transactions'. Add a short scope: what is in and what is out.
Output: 02-Requirements/requirements.md" "task,requirements"
iss "List the use cases" \
"8 to 10 use cases: name, actor, and include/extend relations where they apply. Names only for now, the diagram and descriptions come in Sprint 2.
Output: 02-Requirements/use-case-list.md" "task,requirements"

iss "Sketch the 3 main screens" \
"Low-fidelity sketches in Figma: dashboard, import transactions, forecast and alerts. Put the Figma link and PNG exports in the folder.
Output: 03-Design/wireframes/" "task,design"
iss "Slide template" \
"A clean slide template in Google Slides, built by hand. Add the link to 03-Design/README.md." "task,design"

iss "Streamlit app skeleton" \
"A Streamlit app that runs, with a sidebar and 3 empty pages (dashboard, import, forecast and alerts). Add requirements.txt and run instructions in the prototype README.
Output: 05-Final/prototype/" "task,prototype"
iss "Fake transactions CSV" \
"About 200 realistic transactions in MYR for an international student at Taylor's (food, transport, rent, subscriptions, top-ups from home).
Output: 05-Final/prototype/data/transactions.csv" "task,prototype"
iss "Exchange rates with a cached fallback" \
"A function that gets EUR to MYR rates from the Frankfurter API (https://frankfurter.dev, no key needed) and falls back to a cached CSV when the network fails. Check that MYR is available. Add a unit test for the fallback, so the CI runs something real.
Output: 05-Final/prototype/" "task,prototype"

iss "Survey for international students" \
"Short Google Forms survey, 6-8 questions, on how students track their money and exchange rates. This is our only survey. Each team member shares it with their own contacts at Taylor's, so we reach about 10-15 real answers. Put a summary of the answers in 02-Requirements/survey-results.md." "task,requirements"
iss "Test plan outline" \
"Scope, test levels (unit, integration, system, user acceptance), environment, who tests what, schedule.
Output: 04-Test/test-plan.md" "task,testing"

echo "Done. Next: create the GitHub Project board and add the issues."
