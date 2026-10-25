# Implementation decision — 25 October 2026

The user explicitly authorised implementation, a new feature branch, commit/push
and a pull request in the existing public fork, with human review before merge.
This supersedes the earlier documentation-only scope and fresh-repository route.
No independent spec/plan approval, review re-verification or release approval is asserted.

This branch sanitises current files only. The earlier fresh-history requirement
(FR-003 / AC-03) remains **not satisfied**: inherited commits and the fork
relationship remain accessible. No history rewrite, detachment, merge, deployment
or new repository is authorised by this implementation decision.

The original requirements below remain the design baseline where compatible with
this explicit route. See [implementation-state.md](implementation-state.md) for
task outcomes, evidence and unresolved release gates. A draft PR is the authorised
review outcome; it is not a declaration that all publication conditions passed.

# Publication Acceptance Criteria

**Purpose**: Release gate for an implemented sanitised candidate.
**Created**: 2026-10-25. Current-file evidence is recorded in implementation-state.md; unchecked gates are not passed.

This is future implementation/release evidence, not a Spec Kit reviewer-owned requirements-quality checklist. It lives outside `checklists/` so the implementation workflow cannot mistake post-implementation checks for prerequisites to beginning implementation.

## Content and History

- [x] AC-01 Every exported path has keep/adapt/replace clearance; no original dataset, curated distribution, trained model, stored briefing, binary report or private contract is included. (FR-001,002,004)
- [x] AC-02 Text/structured-file scans plus visual/metadata review find zero unresolved excluded identifiers, field catalogues, schemas, values, trends, branding or embedded material. Renaming/synthetic labels alone are insufficient. (FR-001,002)
- [ ] AC-03 Destination is a separate repository with fresh history, no fork-network parent, inherited Git objects/refs/remotes, original author email metadata or upstream link. Every reachable branch/tag/commit is reviewed. (FR-003)
- [x] AC-04 Candidate docs, settings, images and exported PDFs contain no original workspace/dashboard/warehouse/model/Volume locations, credentials or original output values. (FR-010)

## Data and Behaviour

- [x] AC-05 Fresh checkout has no bundled dataset and gives setup guidance without mock fallback or original-resource calls; configured empty view gives an empty result. (FR-004,006)
- [ ] AC-06 Valid neutral predictions/context work without original fact/dimension schema; invalid/null/nonfinite/inconsistent/duplicate input has the contracted safe outcome in **both** the application and direct dashboard SQL paths. With Python validation bypassed, the duplicate `case-a` pair, even when a display filter hides one row, yields the dashboard's fixed invalid status, unavailable metrics and no student rows. Repeat for invalid scores/thresholds/flags and wrong/missing schema; no silent deduplication/discard is allowed. Missing optional context works. (FR-005,006)
- [ ] AC-07 Verify that resolved dashboard SQL binds the application's intended operator prediction source, and that every prediction widget uses the guarded dataset; a missing/mismatched binding or failed query/refresh is explicit unavailability, with no stale result presented as current or selectable. Verify the guard's whole-input scope in generated widget queries and the unfiltered status display. Valid, empty and custom-threshold inputs retain correct overview, filtering, full-ID/collision-safe prefix selection and rounding; an empty valid source shows zero counts rather than the invalid-source state. Offline query checks and actual platform visual/refresh evidence are recorded separately. (FR-005,006,007,008,015)
- [x] AC-08 Briefing success, refusal, validation, one retry, terminal failure, storage outage, saved retrieval and PDF export preserve required behaviour. No third attempt or fallback success; storage confirmation follows save/read. (FR-007,009)
- [x] AC-09 Approved/unapproved/null/unavailable/suppressed context and prompt-injection-like strings are handled as contracted; no unsupported causal/history, service, model-validity or synthetic-data claim is shown. (FR-008,009)
- [x] AC-10 Meaningful changed-boundary regressions, retained pytest/Ruff checks and any authorised integration checks have recorded results; unverified integrations remain explicitly open. (FR-015)

## Attribution and Rights

- [x] AC-11 Contributions and Licence both credit the original project/team without institutional references; every Renny claim has private evidence and shared work is qualified. Authorship is not described as sole ownership. (FR-011)
- [ ] AC-12 Signed-assignment implications, existing partner publication authorisation, applicable inherited rights and final public rights wording are recorded. No ungranted downstream reuse licence is asserted. (FR-012)
- [ ] AC-13 Required notices/attribution are preserved. Any owner-naming or exact-notice conflict with exclusion conditions has an authorised compatible resolution; no silent deletion or fabricated owner. (FR-011,012)

## Decision

- [ ] AC-14 Human spec/plan review and an explicit later implementation instruction are recorded; the SDD draft was not treated as approval to change application code. (FR-013)
- [x] AC-15 No separate industry scenario or demo dataset is required. If a later demo is elected, it is opt-in, independently invented, reviewed and unrelated to original data/schema/trends. (FR-014)
- [ ] AC-16 Explicit later publication instruction identifies the exact candidate manifest/revision and all open release issues are closed. No push, deployment or publication occurs under this documentation request. (FR-012,013)

## Requirement-to-Task Traceability

| Requirements | Tasks | Checks |
| --- | --- | --- |
| FR-001,002 | T003-T007,T022,T023 | AC-01,02 |
| FR-003 | T004,T023,T024 | AC-03 |
| FR-004 | T006,T011,T012,T021 | AC-01,05 |
| FR-005,006 | T010-T014,T016 | AC-05,06,07 |
| FR-007,008 | T013-T020 | AC-07,08,09 |
| FR-009 | T017-T020 | AC-08,09 |
| FR-010 | T005,T007,T011,T015,T022 | AC-04 |
| FR-011,012 | T002,T008,T009,T024 | AC-11,12,13,16 |
| FR-013 | T001,T004,T023,T024 | AC-14,16 |
| FR-014 | T003,T024 | AC-15 |
| FR-015 | T010,T016,T017,T020-T023 | AC-10 |


Checked content/behaviour items above refer to current-file inspection and offline
verification only; they do not assert live platform evidence or clear inherited history.
AC-03 remains not satisfied. AC-06/07,12/13,14/16 remain open or partial as detailed in
[implementation-state.md](implementation-state.md). The later instruction authorises
the bounded draft PR; it does not close every release condition.
