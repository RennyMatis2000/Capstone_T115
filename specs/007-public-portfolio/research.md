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

# Research: Public Portfolio

**Date**: 2026-10-25. Decisions are draft design decisions, not permission grants.

| Topic | Decision | Rationale | Alternatives considered |
| --- | --- | --- | --- |
| Release vehicle | Separate sanitised repository, fresh history | Source is a public fork with excluded files/history | Cleaning HEAD leaves history; detaching preserves metadata; mirror push copies it |
| Domain | Keep student risk/advisor workflow | University agnostic is compatible with the existing domain | Different industry scenario is optional and unnecessary |
| Data | User-supplied predictions and approved context; no bundled dataset | Removes original schema/distribution dependence | Old synthetic CSVs remain unsafe; rebuilding ML adds unjustified scope |
| Demo | No demonstration dataset in baseline | Configuration and isolated test doubles suffice | A later tiny invented opt-in demo could aid screenshots without realism/validity claims |
| Architecture | Existing service/adapters and briefing seams | Responsibilities are already separated | No new framework, service or mapping engine |
| Data boundary | Neutral prediction view plus optional allowlisted context | Removes field catalogue and dimension joins with limited changes | Renaming original table locations fails exclusion |
| Direct dashboard path | Guarded SQL dataset bound explicitly to the application's operator prediction view; validate whole input before display filters | Dashboard SQL bypasses Python validation; duplicate/inconsistent records must not become normal aggregates | Python-only checks, a separate earlier precheck and silent deduplication do not establish safe dashboard results |
| Rights | Separate authorship, assigned ownership, publication and downstream reuse | Signed assignment is not a public software licence; reported partner authorisation remains relevant | No MIT/Apache or sole copyright claim without supported grant |
| Attribution | Neutral original project/team credit in Contributions and Licence | Preserves creator credit without institutional names/upstream links | Uncredited presentation misstates provenance; upstream link exposes excluded content |

Private audit records contain baseline, concrete evidence and contract analysis. No original data statistic or accuracy claim is reused.

GitHub confirms forks display their upstream and share repository-network Git data: [Forks](https://docs.github.com/en/pull-requests/reference/forks). Detaching preserves commit metadata: [Detaching a fork](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/detaching-a-fork). Public visibility differs from an open-source licence: [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository). Checked 2026-10-25.

Technical unknowns have conservative contract defaults. Rights wording, contributor agreement coverage and notice conflicts remain explicit release dependencies; commit authorship cannot settle them.

For the dashboard guard, Databricks documents that viewers can access dataset data even when visualizations do not show it, so SQL must restrict the returned data: [Dashboard datasets](https://docs.databricks.com/aws/en/dashboards/manage/data-modeling/datasets). Generated widget SQL can differ from the full dataset query and reflects active filters; inspect it as part of verifying guard scope: [Dashboard visualizations](https://docs.databricks.com/aws/en/dashboards/manage/visualizations). Checked 2026-10-25. These facts motivate query-side enforcement; they do not establish that the planned safe display/refresh behaviour is already implemented or proven on the platform.
