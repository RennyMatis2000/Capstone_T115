# Implementation and release evidence

**Date:** 25 October 2026. **Branch:** `007-public-portfolio`.

The latest human instruction authorises implementation and a feature-branch commit,
push and PR in the existing public fork; the user will review it. That instruction
supersedes the original documentation-only scope and separate-repository route.
Independent review re-verification and separate human spec/plan approvals have not
been claimed. No merge, approval, deployment, fork detachment or history rewrite occurs.

## Implemented current-file work

- Removed original notebooks, curated data, reports, worklogs, binary documents,
  wireframes, operational dashboard export and earlier source-coupled specifications.
- Kept the existing Spec Kit configuration, workflow, constitution and templates;
  imported only neutral feature documents. Local feature state uses its existing mechanism.
- Removed populated resource defaults, legacy field catalogues and dimension joins.
  Runtime has no fixture data. Required predictions and optional allowlisted JSON context
  now follow the neutral contract. Source failures expose safe fixed guidance.
- Preserved shared service/API/MCP boundaries, four-section briefing validation,
  one eligible retry, validation before append-only storage, retrieval, and PDF export.
  Context is data, never causal evidence; unapproved/null/suppressed prompt values are omitted.
- Kept risk overview, classification/score filters, chart, full-ID lookup and collision-safe
  16-character prefix lookup in the live application. Every rerun validates source input;
  a failed read clears selection. Score formatting preserves boundary consistency.
- Prepared one guarded direct-SQL dataset and a checked binding renderer. The unbound
  template fails setup. Invalid input yields status only, null metrics and no student rows;
  valid empty input yields zero counts. The external dashboard link stays disabled.
- Added bounded team credit and rights wording without a new public reuse licence.
  Preserved the version-specific Spec Kit MIT notice separately from application rights.

## Actual verification

- Locked dependencies unchanged; Python 3.11.15 offline environment.
- Pytest: **316 passed, 1 skipped**. The skip is the inherited comparison with a category
  colour map that no longer exists in the neutral dashboard. App contrast tests still run.
  Two dependency deprecation warnings remain; neither is a failed application assertion.
- Ruff checks pass for application code/tests and the export scanner.
- Direct SQL checks bypass Python prediction validation. They execute the generated
  relational guard using SQLite with only metadata/table binding and typed-NULL syntax
  adaptations. Coverage includes duplicate `case-a` rows (75/true/60 and 25/false/60),
  a filter hiding one duplicate, malformed IDs including a final newline, null/nonfinite/
  out-of-range scores and thresholds, inconsistent flags, wrong types, missing columns,
  omitted optional-provenance bindings, empty/valid/custom-threshold data and outer filters.
  Missing columns cause a query error; they never return ordinary zero counts.
- Application contract checks cover missing setup/no source call, duplicates before
  selection/limit, safe 503 responses, JSON validation/allowlist/suppression and no-context
  briefings. Retained retry, storage, API/MCP and UI regressions run offline with doubles.
- An invented one-page PDF was extracted and visually reviewed outside Git: layout,
  full ID, score/threshold, unavailable date, suppression marker and four sections pass.
- Current UTF-8 candidate files pass private-pattern and asset/path checks. All original
  binary assets are excluded; no original image/report is asserted cleared by a text scan.
  Private inventory, manifest, detailed scan inputs and verification outputs stay outside Git.

Offline checks prove application/query properties only. No original service was contacted.
No Databricks generated widget SQL, dashboard import/render/refresh/cache behaviour,
real endpoint, SQL connector or Volume integration has been established on operator infrastructure.

## Acceptance disposition

| Criteria | Disposition |
| --- | --- |
| AC-01,02,04 | Current files reviewed and scanned; this does not clear inherited history or platform metadata |
| AC-03 / FR-003 | **Not satisfied**: existing commits and fork relationship remain accessible by explicit route choice |
| AC-05 | Offline setup/no fallback/empty behaviour verified |
| AC-06,07 | Application and generated-query offline evidence passes; live dashboard/platform evidence remains open |
| AC-08,09,10 | Offline regressions and invented PDF checks pass; live integrations are not claimed |
| AC-11 | Bounded creator credit added; supporting provenance remains private |
| AC-12,13 | Existing partner authorisation acknowledged; final inherited-rights/notice/platform scope remains open |
| AC-14 | Explicit implementation/branch/PR instruction recorded; independent/human gate approvals are not invented |
| AC-15 | No separate scenario or bundled demo dataset; tests use minimal invented records |
| AC-16 | Draft PR authorised, full release acceptance **not satisfied**; human review still required |

The draft PR must not be presented as complete publication-condition compliance.
See [tasks.md](tasks.md) for completed versus partial tasks and
[acceptance.md](acceptance.md) for the original full release criteria.
