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

# Data Model: Public Portfolio

These are new public-interface concepts, not a republished source schema. Detailed rules: [data-interface.md](contracts/data-interface.md).

| Entity | Fields / relationship | Validation |
| --- | --- | --- |
| Prediction | `student_id`, `risk_score`, `at_risk`, `threshold_score`; optional `model_reference`, `scored_at` | Unique opaque ID; finite 0-100 scores; classification agrees with threshold; no credentials/resource URLs in provenance |
| Student context | `student_id`, `attributes_json` | At most one row per prediction ID; optional; allowlisted scalar attributes, no inherited catalogue |
| Risk profile | Prediction + optional context | No context is valid; unknown ID never triggers synthetic fallback |
| Dashboard result | Guarded prediction records plus a status result for the same evaluated input | Whole-input validation before presentation filters; invalid/query-failed means explicit unavailability and no ordinary metrics/selectable rows; valid empty means zero counts |
| Validated briefing | `student_id`, text, generated time, validator version, attempt count, prediction snapshot, source, storage confirmation | Only validated nonblank text stored; maximum two generation attempts |
| Release manifest | Path, disposition, review evidence/result | Every export accounted for; private provenance excluded |
| Contribution record | Contributor, bounded claim, private evidence | Authorship is distinct from ownership; merge/upload alone is insufficient |

States: unconfigured -> setup-required; configured -> empty or available; at-risk selection -> existing valid briefing or generate -> validate -> persist -> confirm. Eligible failure -> one retry -> validate -> persist or terminal failure. Configuration/storage-read failures never become success. Retrieval never generates. In-memory storage is process-local only.

No historical briefing/model migration is required. Operator runtime data remains outside release artifacts.

The dashboard consumes SQL directly, so its query-side guard is independent of Python validation. Both consumers are explicitly bound to the same operator prediction view during setup. See the contract for guard ownership, query-snapshot semantics and visible failure/refresh states.
