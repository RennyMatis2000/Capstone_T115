# Student Risk and Advisor Briefing application

Use Python 3.11–3.13 and the locked dependencies. From this folder:

```powershell
uv sync --locked --dev
uv run ruff check .
uv run pytest
uv run uvicorn student_attrition_risk.main:app --host 127.0.0.1 --port 8000
```

The UI is served at `/ui/`, REST at `/api`, MCP at `/mcp` and API reference at `/docs`.
Without operator settings, data requests fail with setup guidance and no source call.
Supply environment variables privately; `.env.example` lists keys and is not loaded
automatically. Never commit populated settings. See [the data interface](../docs/data-interface.md).

The existing service owns generation, four-section validation, at most one eligible
retry, saving validated text, and retrieval. Missing generation is a configuration error;
it never produces substitute template prose. A blank `BRIEFING_VOLUME` uses process-local
ephemeral storage, lost on restart. A configured Volume provides append-only governed
storage; real endpoint and Volume integration have not been tested in this adaptation.

The UI overview validates the complete prediction input before applying classification
and minimum-score filters. It shows supplied scores/thresholds and full opaque IDs.
Any source failure clears selected records and briefing actions on rerun. Optional
approved context is not evidence of individual model causation. Generated content
needs human review; deterministic validation does not establish every semantic claim.
PDF download remains available for a validated briefing.

The external dashboard link stays disabled while platform refresh/cache acceptance is
open. Its one-dataset SQL guard and binding renderer have independent offline negative
tests. Those tests do not establish Databricks runtime behaviour or import compatibility.

See [team credit](../docs/Contributions.md), [rights](../docs/Licence.md) and
[implementation evidence](../specs/007-public-portfolio/implementation-state.md).
