# Operator prediction and approved context interface

The public adaptation changes identifier and prediction payload fields to the neutral
contract. Operators provide already-scored predictions; no training pipeline ships.

| Setting | Behaviour |
| --- | --- |
| `DATABRICKS_PREDICTION_TABLE` | Required explicit safe three-part identifier; no default |
| `DATABRICKS_HOST`, `DATABRICKS_WAREHOUSE_ID` | Operator SQL connection; unified auth or privately supplied token |
| `DATABRICKS_CONTEXT_TABLE` | Optional safe three-part view with `student_id`, `attributes_json` |
| `APPROVED_CONTEXT_FIELDS` | Up to 20 unique snake_case keys, empty by default |
| `DATABRICKS_MODEL_NAME` | Optional managed generation endpoint; absent means briefing unavailable |
| `BRIEFING_VOLUME` | Optional safe Volume path; absent means ephemeral memory storage |

Required columns are `student_id` (unique opaque string, 1–128 ASCII letters/digits,
hyphen or underscore), `risk_score` and `threshold_score` (finite numeric 0–100),
and `at_risk` (Boolean exactly matching `risk_score >= threshold_score`). Optional
nullable `model_reference` is an opaque 1–128-character identifier using the same
alphabet; nullable `scored_at` is a timezone-aware timestamp. No model-performance
claim follows from these fields. SQL schema types must match; strings are not scores.

The application discovers optional columns, selects named fields, validates the whole
relation, and rejects duplicates before filtering, limiting or lookup. Exact ID lookup
is preferred; a 16-character prefix is accepted only when it identifies one full ID.
Unknown/ambiguous selection is 404, non-at-risk generation 409, malformed REST IDs 422,
terminal generation/validation 502, source/configuration/storage outage 503. A configured
empty source returns an empty list successfully. Health exposes no resource settings.

Context has at most one row per student. JSON must be an object with unique keys and
scalar finite numbers, booleans, null or strings up to 256 characters. Nested objects,
arrays, duplicate keys and malformed content fail safely. Only allowlisted keys leave
the adapter. Null/unavailable/suppressed values are omitted from prompts; suppression
is shown as an explicit privacy marker in the UI/PDF. No baseline context key is enabled.
Operators are responsible for privacy approval and any small-group suppression before
supplying context; the adaptation has no demographic joins or inherited category list.

REST retains health, high-risk list, profile, generate/retrieve briefing routes.
MCP retains `get_student_prediction`, `get_student_profile`, `get_high_risk_students`,
`generate_student_briefing`, `get_student_briefing`; their identifier parameter is now
`student_id`. Prior field names are not accepted as aliases. Stored legacy briefings
are not migrated. An operator must use a fresh private storage prefix for this contract.

## Independent dashboard path

`render_dashboard(settings, bound_table, model_reference=False, scored_at=False)`
prepares an offline definition only. The bound table must equal the app's prediction
setting, with optional flags matching actual optional columns. The template is deliberately
unbound. Source values must never be saved back to the public repository.

Every widget uses the same guarded dataset. Its query validates schema, the entire
unfiltered relation, duplicate IDs, score/threshold ranges and flag consistency in one
query before returning student rows. Invalid input returns a status row only, null
metrics and no selectable students. Empty valid input returns zero counts and a distinct
message. Student widget filters operate on those results; the status widget has no
student/risk filter connection. Query/setup failure is an error, never a zero result.

**Platform acceptance remains blocked.** The external link is not offered by this
application. Databricks documents separate dashboard caching that can retain old results;
therefore guarded SQL alone cannot establish the required failed-refresh state.
Use the live application overview until actual visualization SQL, import/rendering,
failure, refresh and cache behaviour have been verified in authorised operator resources.
Offline SQLite execution adapts only table metadata bindings and typed-NULL syntax;
it proves relational guard behaviour, not Databricks optimizer or UI behaviour.

References: [dashboard caching](https://docs.databricks.com/aws/en/dashboards/caching),
[view visualization SQL](https://docs.databricks.com/aws/en/dashboards/manage/visualizations/).
