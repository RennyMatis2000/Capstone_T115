"""Check current candidate files. This does not audit inherited Git history or grant release approval."""
import argparse
import json
import re
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-patterns", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.private_patterns.resolve().is_relative_to(root):
        parser.error("Private scanning inputs must stay outside the repository.")
    patterns = [re.compile(pattern, re.I) for pattern in json.loads(
        args.private_patterns.read_text(encoding="utf-8"))]
    paths = subprocess.check_output([
        "git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"
    ], cwd=root).decode().split("\0")
    findings = []
    checked = 0
    for name in dict.fromkeys(filter(None, paths)):
        path = root / name
        if not path.is_file():
            continue
        checked += 1
        if any(part in {".git", "internal-review", "notebooks"} for part in path.relative_to(root).parts):
            findings.append({"path": name, "reason": "excluded path"})
        if path.suffix.lower() in {".pdf", ".docx", ".xlsx", ".csv", ".ipynb", ".png", ".zip"}:
            findings.append({"path": name, "reason": "unreviewed asset or data"})
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            findings.append({"path": name, "reason": "unreviewed binary"})
            continue
        if any(pattern.search(text) for pattern in patterns):
            findings.append({"path": name, "reason": "private rule match"})
    print(json.dumps({"checked_files": checked, "findings": findings}, indent=2))
    return bool(findings)

if __name__ == "__main__":
    raise SystemExit(main())
