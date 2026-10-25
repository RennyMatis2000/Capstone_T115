# Offline validation and private operator setup

Run in `student_attrition_risk_app/`:

```powershell
uv sync --locked --dev
uv run ruff check .
uv run pytest
uv run uvicorn student_attrition_risk.main:app --host 127.0.0.1 --port 8000
```

An unconfigured checkout bundles no student records and reports setup guidance / 503
for data requests. Set operator values privately using `.env.example` as the key list.
The application reads process environment settings; the file is a reference, not an
automatic environment loader. Never commit populated credentials or resource values.

See [the data contract](contracts/data-interface.md) and
[operator setup](../../docs/data-interface.md). Configured empty input is successful
and shows zero counts. Every read validates all source predictions before filtering.
The UI refreshes source validation on every rerun and clears selected data on failure.

Dashboard definitions are prepared offline with `render_dashboard(settings, bound_table)`
from `student_attrition_risk.dashboard`. Its explicit binding must equal the app setting.
Pass `model_reference=True` / `scored_at=True` if those optional columns exist. Keep
the generated definition private. The unbound template deliberately fails setup.

The external dashboard link is withheld. No authorised platform test has established
the required widget wrapping, refresh failure and cache safety. Inspect actual
visualization SQL and failure behaviour before accepting that integration. The app's
overview, risk filter, score filter, chart and full-ID lookup provide the usable path.

Briefing tests use controlled generation and storage doubles. No model accuracy,
live endpoint, Volume integration, deployment or platform acceptance is claimed.
See [implementation-state.md](implementation-state.md) for actual results and open gates.
