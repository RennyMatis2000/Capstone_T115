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

# Implementation Plan: University-Agnostic Public Portfolio

**Branch**: `007-public-portfolio` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification `specs/007-public-portfolio/spec.md`.

## Summary

Preserve the existing Databricks advisor application and service/adapters. Use a new feature branch in the existing fork as explicitly selected by the user, adapt the prediction/context boundary to neutral views and remove institution-specific source material. Do not migrate the original synthetic-data or ML-training pipeline. Implementation and a draft PR are now authorised; complete release readiness is not established.

The source is already a public GitHub fork with excluded material in current files and history. A new branch, deleting HEAD files, detaching the fork or mirror-pushing elsewhere cannot establish a clean publication boundary. Keep attribution in neutral Contributions and Licence sections, with private provenance and contracts outside the candidate.

## Technical Context

**Language/Version**: Existing Python `>=3.11,<3.14`.
**Primary Dependencies**: Existing FastAPI, Streamlit, FastMCP, Pydantic, Databricks SDK/SQL connector, Uvicorn and ReportLab; retain reviewed `uv.lock` unless a necessary change requires otherwise.
**Storage**: Operator-owned prediction/context Delta tables or views; existing optional Unity Catalog Volume briefing store. In-memory storage is explicitly ephemeral, never described as durable.
**Testing**: Existing pytest and Ruff; focused contract and sanitisation verification. No new framework.
**Target Platform**: Databricks Apps with operator-provided resources; offline tests need no original workspace.
**Project Type**: Existing application with UI, REST and MCP interfaces sharing `StudentService`.
**Performance Goals**: Preserve bounded retrieval and workflow behaviour; no new throughput target or predictive-accuracy claim.
**Constraints**: No institution-specific identifiers, field catalogue, distributions, resource URLs or data in public artifacts. The later instruction authorises bounded code and feature-branch Git changes ending in a draft PR.
**Scale/Scope**: One public adaptation, three stories; retain application capabilities with a smaller neutral data contract. No new industry scenario, training pipeline or mandatory demo dataset.

## Constitution Check

Original constitution v1.1.0 was read in full and remains unmodified. Author implementation review records compatibility with the principles below; it is not independent or human release approval.

| Principles | Design compliance |
| --- | --- |
| I specification driven; VII plan-defined scope; XIV traceability; XV satisfaction | Numbered requirements map to tasks and release checks; latest human implementation instruction is recorded, without inventing separate gate approvals. |
| II containment; III read broadly/write narrowly; XVI preserve team work | Current-file sanitisation/removal is explicitly authorised on this branch. Private evidence and inherited commits are preserved. No upstream change is made. |
| IV minimal change; V reuse; VI no unnecessary complexity | Adapt existing repository/configuration/model/prompt boundaries. No parallel backend, new product domain or model rebuild. |
| VIII compatibility; IX modularity | Keep Python/Databricks and UI/API/MCP/service/generation/validation/retry/store separation. |
| X security/privacy; XI validation/errors | Explicit resource settings; safe identifiers and bound values; neutral validated inputs; no sensitive context by default; explicit failures. |
| XII proportionate tests | Focused contract checks and meaningful workflow regressions; no blanket coverage target. |
| XIII human review | Draft spec and plan gates remain pending; rights/publication review is separate. |
| XVII human-controlled version control | Feature branch, commit, push and draft PR are explicitly authorised. No merge, history rewrite, detachment or deployment. |

No constitution amendment is proposed. Porting governance text to a future public repository requires sanitisation/notice checks and must not misrepresent this draft as ratified governance.

## Project Structure

### Documentation (this feature)

```text
specs/007-public-portfolio/
  spec.md, plan.md, research.md, data-model.md, quickstart.md, tasks.md
  contracts/data-interface.md
  checklists/requirements.md, acceptance.md
```

The review package additionally supplies private audit/rights records and a per-file inventory, plus candidate Contributions/Licence drafts. Only individually cleared candidate files may later be exported; do not publish the review archive.

### Source Code (existing-fork feature branch)

```text
docs/README.md, Contributions.md, Licence.md, data-interface.md
student_attrition_risk_app/
  README.md, pyproject.toml, uv.lock, app.yaml, .env.example
  src/student_attrition_risk/
    config.py, student_repository.py, models.py, ports.py
    student_service.py, api.py, mcp_server.py, main.py
    ui.py, briefing_instructions.py, briefing_provider.py
    briefing_validation.py, briefing_pdf.py
    retry_workflow.py, briefing_store.py, briefing_messages.py
    databricks_client.py, streamlit_host.py, __init__.py
  dashboard/Student Attrition Risk Overview.lvdash.json
  tests/  # independently reviewed tests and minimal invented fixtures
scripts/validate_public_export.py  # bounded later validation utility
```

**Structure Decision**: Preserve package and architecture. Only the above application files, reviewed tests, clean docs, required notices and reviewed Spec Kit tooling are export candidates. Original notebooks, curated data, binary documents, specs/worklogs, contracts and operational exports are excluded by default. No directory is copied wholesale.

## Phase 0: Research

[research.md](research.md) records decisions and alternatives. The private audit supplies source locations and contribution evidence. Unknown rights are release dependencies with a no-grant default, not invented technical requirements. The signed assignment changes ownership wording, not the partner's supplied exclusion conditions.

## Phase 1: Design

1. **Data access**: Replace fact/dimension joins and inherited field lists with an operator-owned prediction view plus optional context view under [the contract](contracts/data-interface.md). Reuse repository/service boundaries; rename inherited wire/field vocabulary across models and tests. This is a bounded public-version contract change, not a second adapter framework.
2. **Configuration**: Remove original defaults from `config.py`, `.env.example` and `app.yaml`. Prediction source is explicit. Missing configuration uses the existing safe configuration-error path with setup guidance and no original-network calls. Configured empty data produces an empty view. Configure the dashboard URL; hide its link when absent. Default runtime selects no bundled mock records.
3. **Context**: No copied field catalogue or legacy dimension joins. Optional JSON context uses an operator allowlist, empty by default. Missing/null/suppressed values remain distinct. Do not expose sensitive categories merely because old code handled them.
4. **Presentation and direct-query validation**: Preserve overview, score/flag filtering and selection. The Lakeview dashboard queries SQL independently of Python, so its input guard is owned by T014 and its negative verification by T016. Bind it to the same operator prediction view as the application, using explicit deploy-time substitution and a binding check; application environment variables do not automatically configure a dashboard. Use one guarded SQL dataset for prediction widgets: validate the complete unfiltered input inside each executed dataset query before producing display rows/aggregates. Reject duplicate IDs, invalid required values and inconsistent flags; never silently deduplicate, drop bad rows or rely on a separate earlier precheck. The dataset returns an unfilterable status result; invalid input yields a fixed safe message, null/unavailable metrics and no selectable student rows. Empty valid input instead yields the normal empty state and zero counts. Remove source-dependent demographic widgets, use supplied flags/thresholds and preserve collision-safe lookup/rounding. See the [direct dashboard contract](contracts/data-interface.md#direct-dashboard-validation-boundary) for failure and snapshot semantics.
5. **Briefing**: Retain generation, four-section instructions, validation, at most one retry, append-only validated storage, retrieval and permitted PDF export. Update schema-dependent labels, context checks and exported metadata only. Remove unconditional synthetic-record wording for live inputs. Missing generation remains an error, never a template fallback.
6. **Provenance**: Credit creators/project separately from rights ownership. Do not add a copyright claim in Renny's name for assigned team IP. Retain applicable third-party notices; resolve exact-text conflicts before release.
7. **Publication**: Prepare a bounded sanitisation PR in the existing fork. Fresh-history acceptance is not satisfied. Do not detach or rewrite history. Keep private evidence and excluded identifiers out of all new content and commit metadata.

## Validation and Review Gates

| Gate | Required result | Status now |
| --- | --- | --- |
| Installed `review-spec` | Human approves spec and assumptions | Pending |
| Installed `review-plan` | Human approves plan/tasks and interface changes | Pending |
| Rights/attribution | Existing partner authorisation scope recorded; suitable rights wording and notices resolved without claiming ungranted downstream reuse rights | Open |
| Candidate validation | All [publication acceptance criteria](acceptance.md) checks pass with evidence | Not run; no implementation |
| Draft PR | User explicitly selected the existing fork and will review it | Authorised; merge/release remains pending |

All draft SDD artifacts were requested together. They are prepared for review without running the full workflow engine, which would continue to implementation. Human gates are preserved, not marked approved.

## Complexity Tracking

No architectural violation identified. Changing inherited field coupling is necessary; keeping original schemas under new table names fails sanitisation. A schema-mapping engine, new industry scenario and replacement ML pipeline are unnecessary.
