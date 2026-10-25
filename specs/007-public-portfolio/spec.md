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

# Feature Specification: University-Agnostic Public Portfolio

**Feature Branch**: `007-public-portfolio`

**Created**: 2026-10-25

**Status**: Implementation candidate for draft PR review; release gates remain open.

**Input**: Prepare a public portfolio adaptation of the existing student risk and advisor briefing application. Remove institution-specific content, data, schemas and trends; use user-supplied data by default; credit verified personal and team contributions without institutional references. The original design request produced documentation only; the later instruction authorises this implementation PR.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Inspect a clean portfolio (Priority: P1)

As a portfolio visitor, I can inspect the application's capabilities and provenance without encountering excluded institutional material or overstated personal ownership.

**Why this priority**: Every public file and its reachable history must satisfy the publication conditions.

**Independent Test**: Review a candidate file manifest, public documentation and repository-history report without running the application.

**Acceptance Scenarios**:

1. **Given** an allowlisted release candidate, **When** a reviewer inspects text, notebooks, images, document metadata and reachable history, **Then** no excluded branding, names, addresses, schemas, data elements, records, distributions or derived findings remain, and every retained file has a disposition.
2. **Given** team-developed components, **When** a visitor reads Contributions and Licence, **Then** both identify the original project and team, distinguish Renny's evidenced work, preserve applicable notices and make no unverified ownership or licence grant.
3. **Given** a notice that conflicts with the exclusion condition or unclear redistribution rights, **When** release readiness is assessed, **Then** publication remains blocked for resolution; neither the notice nor the condition is silently disregarded.
4. **Given** original development history contains excluded material, **When** preparing the public adaptation, **Then** it uses a separate sanitised repository with fresh history and no original fork-network relationship or upstream hyperlink. Existing repositories remain untouched.

### User Story 2 - Configure my own data (Priority: P1)

As an operator, I can supply my own risk predictions and optional context without reproducing another organisation's schema, records or trends.

**Why this priority**: A generic data interface preserves the application while removing institution-specific coupling.

**Independent Test**: Use independently invented test records, then repeat with no configuration, empty data and invalid records; no original data or live source workspace is needed.

**Acceptance Scenarios**:

1. **Given** a fresh checkout without configuration, **When** it starts, **Then** it reports setup is required, displays no student records and makes no call to an original workspace or implicit demonstration source.
2. **Given** operator-supplied valid predictions, **When** an advisor browses, filters and selects a student, **Then** the displayed ID, score, classification and threshold match that record; missing optional context remains explicitly unavailable.
3. **Given** malformed, duplicate, ambiguous or inconsistent records, **When** they are requested, **Then** each application and dashboard view reports the contracted safe failure without fabricating values, silently picking a record or exposing raw source details. Invalid prediction data must not appear as ordinary dashboard counts or student rows, even when a display filter would hide the invalid record.
4. **Given** a configured but empty source, **When** the advisor opens the application, **Then** an empty-state message appears without example records or derived statistics from the original project.

### User Story 3 - Review a briefing using generic inputs (Priority: P2)

As an advisor, I can request, review and retrieve a briefing using permitted context, while retaining the existing validation, retry and storage safeguards.

**Why this priority**: This preserves the core demonstrated workflow and evidenced contributions.

**Independent Test**: Use controlled generation and storage doubles with invented records to exercise success, rejection, retry and retrieval.

**Acceptance Scenarios**:

1. **Given** an at-risk prediction, approved context and configured generation, **When** generation succeeds, **Then** only a validated briefing is returned and its storage confirmation follows a successful save.
2. **Given** a failed first attempt, **When** retry is eligible, **Then** at most one additional generation attempt occurs; terminal failure stores no invalid briefing and produces no substitute template result.
3. **Given** missing generation configuration or an unavailable store, **When** a briefing is requested, **Then** a safe explicit error appears; no success or persistence is falsely reported.
4. **Given** missing, suppressed or unapproved context, **When** composing or exporting a briefing, **Then** those values are omitted, source values are treated as data, and prose makes no unsupported causal, historical, institutional-service or predictive-validity claim.

### Edge Cases

- A document or image has no searchable text: it remains excluded until visual review, including embedded content and metadata, clears it.
- A file is labelled synthetic but encodes original ratios, categories, schemas or findings: exclude it; renaming identifiers is insufficient.
- A student ID prefix matches more than one record: reject ambiguous selection; never choose one arbitrarily.
- A score is near a classification boundary: display rounding must not contradict the supplied classification.
- An operator source has confidential or identifying data: never copy it into repository artifacts, screenshots, logs or release examples.
- A source is not labelled synthetic: do not falsely describe its records as synthetic.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Public content and reachable history MUST exclude institution-specific references, branding, data elements, schemas, source-derived trends and findings. Internal evidence stays outside all public exports.
- **FR-002**: Every candidate file MUST have an evidence-based keep, adapt, replace or exclude decision, including hidden configuration, fixtures, notebook source/output/metadata, images, PDFs, office documents and exports.
- **FR-003**: The adaptation MUST use a separate sanitised repository with fresh history; it MUST NOT copy original Git objects, refs, remotes, upstream links, discussions or release attachments.
- **FR-004**: Default operation MUST bundle no student dataset, trained model, original notebook pipeline or demonstration statistics. Minimal independently invented test fixtures are permitted solely for automated verification.
- **FR-005**: Operators MUST explicitly configure their own prediction source and optional approved context through a small neutral contract; original fact/dimension tables and feature catalogues MUST NOT be prerequisites.
- **FR-006**: Missing configuration, empty sources, invalid values, duplicate identifiers and ambiguous lookups MUST produce defined safe outcomes without implicit fallback data. Validation and safe failure MUST apply to both application and dashboard consumers of the same configured prediction source; dashboard filters MUST NOT conceal an invalid source or turn its failure into ordinary results.
- **FR-007**: Existing risk overview, filtering, selection, briefing request, validation, single retry, storage/retrieval and permitted export capabilities MUST be retained where independent of excluded data. Changes MUST stay limited to sanitisation and interface adaptation.
- **FR-008**: Risk presentation MUST use supplied scores, flags and thresholds consistently, with no inherited distribution-specific bands or unsupported predictive-performance claims.
- **FR-009**: Briefings MUST use only approved supplied context, respect unavailable/suppressed values and human review, distinguish observations from suggestions, and avoid invented facts or causal/history claims.
- **FR-010**: Credentials, workspace/dashboard/warehouse identifiers, stored briefings and operational logs MUST NOT be bundled; resource locations MUST come from operator configuration.
- **FR-011**: Contributions and Licence sections MUST credit the original project and team without institutional references, distinguish verified Renny contributions from shared work, and retain all applicable attribution and third-party notices.
- **FR-012**: Publication MUST remain blocked until redistribution rights, licence wording and any conflict between mandatory notices and exclusion conditions are resolved. Public availability or an upload/merge commit MUST NOT be treated as ownership evidence.
- **FR-013**: Implementation and a feature-branch commit/push/draft PR are authorised by the later human instruction. Do not merge, rewrite history, detach the fork, deploy or create a replacement repository under this instruction. Independent/human release approvals remain distinct.
- **FR-014**: A separate industry scenario or synthetic demonstration dataset MUST NOT be a release prerequisite. Any later optional demo MUST be independently invented, opt-in and unable to reproduce excluded structures or trends.
- **FR-015**: Validation MUST cover the changed data boundary and preserved workflows using proportionate offline regression checks, plus explicit visual and history review before publication.

### Key Entities

- **Prediction record**: Opaque student identifier, score, classification, threshold and optional scoring provenance supplied by the operator.
- **Approved context**: Optional factual attributes selected for advisor review; not an explanation of model causation.
- **Validated briefing**: Reviewed-format generated text with outcome and storage metadata.
- **Release manifest**: Candidate paths, provenance category, disposition and validation evidence.
- **Contribution record**: Bounded claim tied to development evidence and shared-credit qualifications.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All candidate files have reviewed dispositions; there are zero unresolved excluded-content findings across files, visual artifacts and reachable history.
- **SC-002**: A fresh checkout contains zero student data files or original model artifacts and reveals no student records before operator configuration.
- **SC-003**: All valid, empty, missing-configuration, invalid-value, duplicate-ID and ambiguous-selection scenarios produce their specified outcomes.
- **SC-004**: Every declared retained briefing and selection behaviour passes its acceptance scenario; no failed generation/validation is presented as success or saved as valid.
- **SC-005**: Every personal contribution claim has supporting evidence, and both Contributions and Licence credit the original team/project without excluded references.
- **SC-006**: No unresolved rights, attribution or publication-condition conflict remains when publication is authorised.

## Assumptions

- The user's reported conditional partner authorisation is accepted as the task's publication constraint; it is not evidence of a public reuse licence for every component.
- The supplied signed work-integrated-learning assignment has been reviewed. It assigns project IP to the industry partner, gives the student a non-transferable project/professional-promotion licence, and preserves confidentiality and authorship protections. It is not itself a public repository reuse licence. The supplied information sheet is explanatory guidance. Neither document establishes all other contributors' rights arrangements.
- The student/advisor domain remains; university agnostic does not require a different industry story.
- Operators supply already-scored predictions. Model training, model-quality improvement and reconstruction of the original data pipeline are outside scope.
- Technical design choices are settled in the plan. Rights, final notice wording and human approvals are release dependencies, recorded in the review register rather than invented.
- No artificial throughput, accuracy or load target is imposed on this sanitisation feature.
