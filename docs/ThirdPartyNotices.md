# Third-party tooling and dependencies

The retained `.specify/` templates/scripts/workflows and `.claude/skills/speckit-*`
are from GitHub Spec Kit, installed version 1.0.3. The MIT notice is reproduced in
[.specify/LICENSE](../.specify/LICENSE) and covers that tooling, not the team application.
Verified against the [versioned upstream notice](https://github.com/github/spec-kit/blob/v1.0.3/LICENSE).

Runtime/test dependencies are declared in `student_attrition_risk_app/pyproject.toml`
and pinned in `uv.lock`; their installed distributions retain their own licence files.
No dependency binaries, virtual environment or vendor source are distributed here.
Any later bundled distribution must include the notices applicable to those dependencies.

Application authorship and publication rights are described in [Licence.md](Licence.md).
The tooling licence must not be presented as an application reuse licence.
