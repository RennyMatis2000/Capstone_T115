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

# Tasks: University-Agnostic Public Portfolio

**Input**: This feature's spec, plan, research, data model, contract and quickstart.
**Prerequisites**: Later human implementation/branch/PR instruction is recorded above. Independent review gates remain distinct. Task outcomes are recorded below and in implementation-state.md.
**Tests**: Focused contract/regression checks are required by FR-015. No blanket coverage target.
**Organization**: Setup -> foundation -> independently verifiable stories -> final acceptance.
**Format**: `- [ ] Tnnn [P?] [USn?] description with paths`. Paths refer to this existing-fork branch. Current-file removals are authorised. Private evidence stays outside Git; inherited history stays unchanged.

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Record human specification/plan decisions in `specs/007-public-portfolio/checklists/requirements.md`; do not mark a draft author check as human approval.
- [x] T002 Review the private review register outside Git and record unresolved public rights wording and notice conflicts there, using the existing partner authorisation rather than requesting duplicate publication permission.

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T003 Reconcile the private review register outside Git with the current source commit; write an explicit future export allowlist in the private review register outside Git, rejecting unreviewed binaries/data/history by default.
- [x] T004 Adapted route: prepare a fresh local clone of the exact authorised fork and a new feature branch; preserve inherited history, exclude source assets from current files, and record current-file hashes privately. The fresh-history gate remains failed.

**Checkpoint**: Candidate is private and isolated. Rights dependencies may remain tracked, but no release can pass them unresolved.

## Phase 3: User Story 1 - Inspect a clean portfolio (Priority: P1)

**Goal**: All exported content and provenance satisfy the publication conditions.
**Independent Test**: Manifest, content/visual scan and attribution review; application execution is unnecessary.

- [x] T005 [US1] Create focused export-validation checks in `scripts/validate_public_export.py`, with exclusions/denylist supplied from the private review register outside Git; detect forbidden content, source-data files and accidental `.git`/internal-review inclusion without publishing the sensitive denylist.
- [x] T006 [US1] Exclude original `notebooks/`, curated CSVs, `docs/` binary reports/workbooks/wireframes, operational dashboard PDF, original `specs/` and worklogs from the candidate; reconcile every source path in the private review register outside Git. Replace only assets needed for the public application. Current-branch deletions are explicitly authorised; private provenance and inherited commits remain untouched.
- [x] T007 [US1] Adapt `docs/README.md`, `student_attrition_risk_app/README.md` and any retained `.specify/` or `.claude/` documentation to neutral descriptions, removing source schemas, original findings and private links while retaining required notices.
- [x] T008 [US1] Populate `docs/Contributions.md` from reviewed contribution evidence and `public-content-drafts/Contributions.md`; preserve team credit and qualify shared ML/dashboard work.
- [ ] T009 [US1] Resolve and populate `docs/Licence.md` from `public-content-drafts/Licence.md`; preserve applicable third-party notices and original team/project credit without inventing ownership, sublicensing rights or a licence choice. Escalate mandatory-notice/exclusion conflicts in the private review register outside Git.

**Checkpoint**: US1 can pass file/provenance inspection on its own; it does not establish runtime readiness.

## Phase 4: User Story 2 - Configure my own data (Priority: P1)

**Goal**: Data-free default; neutral operator-owned input boundary.
**Independent Test**: Missing configuration, empty source and valid/invalid invented records, without the original workspace.

- [x] T010 [US2] Add meaningful failing cases in `student_attrition_risk_app/tests/test_config.py`, `tests/test_student_service.py` and new `tests/test_public_data_contract.py` for setup-required, no implicit fallback, empty source, malformed/duplicate IDs, score ranges/threshold consistency, absent context and duplicate/malformed context. Define the same prediction-invalidity cases for the independent dashboard path; T016 must exercise that path without Python validation.
- [x] T011 [US2] Remove resource/table defaults and add neutral context/allowlist/dashboard settings in `student_attrition_risk_app/src/student_attrition_risk/config.py`, `.env.example` and `app.yaml`; require explicit prediction configuration and preserve credential-safe error handling in `main.py`. Define the deploy-time binding check in `docs/data-interface.md`: the dashboard's resolved source must equal the configured prediction table; the dashboard link stays disabled until that check passes.
- [x] T012 [US2] Implement the neutral models and repository queries in `student_attrition_risk_app/src/student_attrition_risk/models.py`, `student_repository.py` and `ports.py`; remove legacy column catalogues/dimension joins, validate the new contract and move minimal invented fixtures into tests rather than default runtime.
- [x] T013 [US2] Adapt `student_attrition_risk_app/src/student_attrition_risk/student_service.py`, `api.py` and `mcp_server.py` to neutral IDs/context, safe duplicate handling and existing error semantics; retain collision-safe lookup and limit bounds.
- [ ] T014 [US2] Own the dashboard validation boundary in `student_attrition_risk_app/dashboard/Student Attrition Risk Overview.lvdash.json`: explicitly bind the same operator prediction view as the app; route prediction widgets through one guarded SQL dataset that checks the entire unfiltered input in the same query snapshot; on invalid input expose only the fixed error status, unavailable metrics and no selectable student rows. Keep the status outside display-filter connections; distinguish empty valid data from invalid/query-failed data and prevent failed-refresh stale data from appearing current. Remove unguarded legacy sources, excluded joins/widgets and inherited bands while preserving valid score/flag filtering and selection. Follow `contracts/data-interface.md`; no silent deduplication or separate precheck is sufficient.
- [x] T015 [US2] Adapt `student_attrition_risk_app/src/student_attrition_risk/ui.py` for generic labels, configured/absent dashboard link, empty state, no invented records and consistent score/flag/threshold presentation.
- [ ] T016 [US2] Own direct-dashboard negative verification in `student_attrition_risk_app/tests/test_dashboard.py` and `test_dashboard_filtering.py`, alongside `test_student_id_lookup.py`, `test_ui.py` and fixture reconciliation. With Python validation bypassed, exercise the guarded SQL/definition using the duplicate `case-a` counterexample, a filter hiding its second row, malformed/null/nonfinite/out-of-range values, inconsistent flags, wrong/missing schema, query failure and mismatched binding. Invalid data must never return normal counts or selectable rows. Verify valid, empty and custom-threshold cases plus rounding. Inspect actual generated widget queries and visual failure/refresh behaviour in an authorised private Databricks check; record unavailable platform evidence as open rather than substituting repository tests. Update `docs/data-interface.md`.

**Checkpoint**: US2 works with operator views or isolated test doubles; no original pipeline is required.

## Phase 5: User Story 3 - Generic briefing review (Priority: P2)

**Goal**: Preserve core briefing workflow without source-specific context or misleading labels.
**Independent Test**: Controlled generation/store doubles exercise all outcomes without a live model.

- [x] T017 [US3] Add focused failing regression cases in `student_attrition_risk_app/tests/test_briefing_orchestration.py`, `test_briefing_workflow_retry.py` and `test_briefing_pdf.py` for empty/unapproved/suppressed context, live-data labelling and safe exports.
- [x] T018 [US3] Adapt `student_attrition_risk_app/src/student_attrition_risk/briefing_instructions.py`, `briefing_provider.py`, `briefing_validation.py` and `briefing_pdf.py` to neutral allowed context; retain four-section validation and non-causal/human-review wording without unconditional synthetic claims.
- [x] T019 [US3] Verify neutral identifier/metadata compatibility in `student_attrition_risk_app/src/student_attrition_risk/retry_workflow.py`, `briefing_store.py` and `briefing_messages.py`; change only schema-dependent references while preserving one retry and save-before-confirm behaviour.
- [x] T020 [US3] Run targeted and retained workflow regressions in `student_attrition_risk_app/tests/`, including `test_briefing_storage_confirmation.py`, `test_volume_briefing_store.py`, `test_mcp_tools.py` and `test_api.py`; record results against `specs/007-public-portfolio/acceptance.md`.

**Checkpoint**: US3 outcomes pass independently with neutral predictions/context. No demo dataset or real-model accuracy result is needed.

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T021 Run `specs/007-public-portfolio/quickstart.md` and all retained Ruff/pytest checks from `student_attrition_risk_app/`; record actual results and environment limitations in the private review register outside Git.
- [x] T022 Visually inspect any newly created public screenshots/PDFs, inspect notebook/office metadata if any are exceptionally retained, and review final content against the private review register outside Git; no original asset passes merely because a text scan is clean.
- [ ] T023 Complete `specs/007-public-portfolio/acceptance.md` against the candidate and, after separately authorised fresh Git initialisation, every reachable branch/tag/commit, remote and repository metadata surface. No original fork/history may enter the destination.
- [ ] T024 Record final rights/notice dispositions and explicit publication decision in the private review register outside Git; stop before push/publication unless specifically instructed. Optional demo data is not a condition of completion.

## Dependencies & Execution Order

T001 -> T002 -> T003 -> T004. US1 T005-T009, US2 T010-T016 and US3 T017-T020 follow the foundation. US3 integration depends on US2's neutral models; its doubles-based test design can begin independently. T021-T024 follow all required stories. T009/T024 cannot pass while rights/mandatory-notice questions remain unresolved.

Within stories: failing tests before interface changes; models/repository before service/API; neutral data bindings and query guards before end-to-end UI checks. T014 depends on T011's source-binding contract; its SQL guard does not rely on T012/T013's Python validation. T016 validates both paths separately before T021/T023 combined acceptance. Acceptance is incremental, but publication requires all three stories.

## Parallel Opportunities and Examples

No automatic delegation is requested by this task list. After T004, US1 documentation review and US2 test design can occur independently. After T012, dashboard rebinding T014 and prompt test design T017 can occur independently because they change different files. T008 and T009 share attribution decisions and should be reviewed sequentially. Tasks sharing models, fixtures or UI must not race.

## Implementation Strategy

First establish a private, data-free candidate and provenance (US1 inspection MVP). Next prove user-supplied data behaviour (US2), then preserve briefing functionality (US3). Run combined acceptance only after each story's independent checks pass. The implementation decision above supplies the later Git/PR authorisation. Deployment remains outside scope.

**Task count**: 24 total: setup 2, foundation 2, US1 5, US2 7, US3 4, final 4.


## Bounded completion notes

T004 follows the user's later existing-fork choice, not the original fresh-history route.
T009 remains partial: public wording grants no new reuse licence; final rights/notice
resolution is still open. T014/T016 have implemented SQL guards and offline negative
checks, but live dashboard wrapping/render/cache evidence is unavailable. The external
dashboard link is withheld; the live app retains overview/filter/selection behaviour.
T023/T024 cannot pass full release acceptance while inherited history, rights and platform
issues remain open. The authorised deliverable is a draft PR for human review.
