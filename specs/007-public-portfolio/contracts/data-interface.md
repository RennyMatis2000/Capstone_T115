# Generic Data Interface Contract

**Status**: Proposed public-version contract; not implemented. Keep the student/advisor domain and service architecture.

## Prediction view

Operator explicitly sets `DATABRICKS_PREDICTION_TABLE` to a safe three-part SQL identifier, with no default. Read only these named columns, never `SELECT *`:

| Column | Type / rule |
| --- | --- |
| `student_id` | Unique non-empty opaque string, 1-128 characters, letters/digits/hyphen/underscore; no direct personal identifiers |
| `risk_score` | Finite numeric [0,100]; a model score, not asserted to be calibrated probability |
| `at_risk` | Boolean consistent with `risk_score >= threshold_score` |
| `threshold_score` | Finite numeric [0,100], same scale as score, no inherited default |
| `model_reference` | Optional nullable opaque string, max 128 characters; no resource URL or secret |
| `scored_at` | Optional nullable timezone-aware timestamp; no fabricated date |

One current prediction per ID. Reject duplicates instead of taking an arbitrary first row. Invalid scores/null required fields/inconsistent flags produce safe source-data errors, not repairs. Parameterise values and validate table identifiers. An existing 16-character prefix lookup may remain only if exactly one full ID matches. Show full opaque IDs by default; no new prefix requirement.

Operators own their private source-to-view mapping. No mapping to the original institution's schema is shipped.

## Direct dashboard validation boundary

The dashboard's SQL queries bypass `StudentRepository` and Python model validation. **T014 owns a query-side guard; T016 owns verification of that guard and its visual result.** Validation in the application alone is insufficient.

**Binding**: During operator setup, substitute the application's configured `DATABRICKS_PREDICTION_TABLE` into the dashboard's neutral prediction dataset and verify that the resolved table reference is identical. Dashboard SQL does not automatically read application environment variables. Keep the resolved resource values in private deployment records, not public examples. Do not enable the dashboard link or accept the deployment while bindings are missing, different or unverified. Optional context remains an application input; it does not justify retaining unguarded legacy dashboard datasets.

**Enforcement**: All prediction widgets use one guarded SQL dataset. Within each executed dataset query, validate the whole unfiltered prediction relation against every required prediction rule before returning any displayable student rows or ordinary aggregates. This includes required schema/types, non-empty valid IDs, unique IDs, finite/ranged scores and thresholds, and flag/threshold consistency. A guard before an unrelated later query is insufficient: validation and the data it permits must refer to the same query snapshot. Widget filters/parameters may narrow only validated display results, not the input checked by the guard. A filter that hides one member of a duplicate pair cannot make that source valid. Reject the invalid input; do not repair it with distinct counts, arbitrary first-row selection or filtering out bad rows.

**Result and visible state**: The guarded dataset supplies one status result and student results only when the source is valid. The status widget is not connected to student, risk or chart filters. On validation failure, return only an invalid status with the fixed message **"Data unavailable: the configured prediction source does not meet the data contract. Review data setup."** Metrics are null/unavailable, charts contain no normal data and no student row can be selected. This must be enforced in the query result, not merely through a warning badge over otherwise visible invalid data. Valid empty input is a different state: zero counts, no student rows and an explicit empty-state message. Valid non-empty input retains normal filtering, selection and supplied custom-threshold behaviour. Normal presentation calculations remain subject to their existing documented filter scope after validation.

**Query/setup failure**: Missing columns, unreadable input, invalid binding or a failed query produce explicit unavailability, never ordinary zero counts or a successful refresh. Show fixed setup/unavailability guidance without embedding source rows or raw exceptions in custom messages. A prior cached result must not be represented as current valid data after a failed refresh; selection from such results must be unavailable. Actual Databricks query wrapping, filtering, caching and rendering must be verified before acceptance. If the platform cannot support the specified safe state, record a blocked dashboard acceptance check and resolve the presentation within the existing architecture before release; do not claim the Python error path covers it.

**Verification design**: Test the guarded query with Python validation bypassed. Two individually consistent rows sharing `case-a` (75/true/60 and 25/false/60 for score/flag/threshold) must yield invalid/unavailable metrics and no rows, never total=1 with both category counts=1. Repeat with a filter selecting only the first row. Also test malformed IDs, null/nonfinite/out-of-range scores/thresholds, inconsistent flags, missing/wrong-type columns, query failure and a mismatched binding. Valid, empty and custom-threshold cases must still succeed. Offline query/definition checks establish design/query properties only; actual Databricks generated widget SQL and visual failure/cache behaviour remain required future integration evidence.

## Optional context view

`DATABRICKS_CONTEXT_TABLE` is unset by default. If set, it is a safe three-part identifier with `student_id` and `attributes_json` (JSON-object string). At most one row per ID. No fact/dimension joins or prescribed demographic fields.

Proposed `APPROVED_CONTEXT_FIELDS` is an operator-approved snake_case key list, empty by default. Maximum 20 keys, each at most 64 characters; values are finite numbers, booleans, null or strings up to 256 characters. Reject malformed JSON, duplicate keys, nested structures and out-of-bound values. Unknown/unapproved keys never reach UI, prompts, logs or PDF. Missing row means no context; duplicate rows are a source-data error.

Preserve existing unavailable/suppressed sentinel semantics; null means absent. None becomes factual prose. No personal/sensitive attribute is enabled in the baseline. Operator approval of context does not authorise copying private records into repository artifacts.

## Interfaces and resources

- Retain health, high-risk-list, student-profile, generate/retrieve-briefing routes and five MCP tool names. Replace identifier parameter/payload vocabulary with `student_id`; document the isolated public-version contract break.
- Preserve error outcomes: unknown/ambiguous student 404; non-at-risk generation 409; invalid request 422; terminal generation/validation failure 502; configuration/source/storage failure 503; missing saved briefing 404. Invalid configured source rows are source failures, not request errors.
- Missing configuration gives setup-required guidance/503 without source calls. Configured empty data gives an empty successful list. Health/status exposes no credentials or configured resource values.
- Warehouse/authentication, optional generation endpoint, optional HTTPS dashboard URL and `BRIEFING_VOLUME` are operator settings. Hide the dashboard link when absent; commit no populated settings.
- Blank volume means ephemeral process-local storage with honest wording. No original stored briefing is migrated/exported.
- Default runtime has no bundled mock students. Tests may contain minimal independently invented fixtures/doubles. No separate demo subsystem is required.
- Live records are operator supplied, not automatically called synthetic. Only explicitly opted-in invented demo records may be labelled synthetic. No inherited performance, demographic-distribution or temporal-trend claim.

## Preserved safety

Keep four-section briefings, non-causal context, data-as-data instructions, validation before storage, one eligible retry, append-only governed storage, retrieval without generation and safe errors. Confirm storage only after save/read. Never substitute deterministic prose for a failed real briefing.
