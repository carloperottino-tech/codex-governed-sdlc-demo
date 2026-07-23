#!/usr/bin/env python3
"""Require complete delivery evidence when application files change."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

APPLICATION_PREFIXES = ("api/app/", "web/", "db/")
APPLICATION_FILES = {"compose.yaml"}
EVIDENCE_FILES = {
    "request.md",
    "plan.md",
    "adr.md",
    "verification.md",
    "release-evidence.json",
}
PLACEHOLDER_MARKERS = ("TODO", "TBD", "PLACEHOLDER")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    return parser.parse_args()


def changed_files(base: str, head: str) -> list[str]:
    if head == "WORKTREE":
        modified = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", base],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        return sorted({path for path in modified + untracked if path})

    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", base, head],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def is_application_file(path: str) -> bool:
    return path in APPLICATION_FILES or path.startswith(APPLICATION_PREFIXES)


def changed_evidence_ids(paths: list[str]) -> set[str]:
    ids: set[str] = set()
    for path in paths:
        parts = Path(path).parts
        if (
            len(parts) == 3
            and parts[0] == "delivery"
            and parts[2] in EVIDENCE_FILES - {"request.md"}
        ):
            ids.add(parts[1])
    return ids


def validate_markdown(path: Path, work_request: str) -> list[str]:
    content = path.read_text(encoding="utf-8")
    errors = []
    if len(content.strip()) < 80:
        errors.append(f"{path} is too short to be meaningful")
    if work_request not in content:
        errors.append(f"{path} does not identify {work_request}")
    if any(marker in content.upper() for marker in PLACEHOLDER_MARKERS):
        errors.append(f"{path} contains an unfinished placeholder marker")
    return errors


def validate_check_items(
    evidence: dict[str, Any], field: str, evidence_path: Path
) -> list[str]:
    items = evidence.get(field)
    if not isinstance(items, list) or not items:
        return [f"{evidence_path}: {field} must be a non-empty list"]

    errors = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{evidence_path}: {field}[{index}] must be an object")
            continue
        if item.get("status") != "passed":
            errors.append(f"{evidence_path}: {field}[{index}] did not pass")
        for key in ("name", "command"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(
                    f"{evidence_path}: {field}[{index}].{key} must be non-empty"
                )
    return errors


def validate_release_evidence(
    path: Path, work_request: str, application_changes: set[str]
) -> list[str]:
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        return [f"{path} is not valid JSON: {error}"]

    errors = []
    expected = {
        "schema_version": "1.0",
        "work_request": work_request,
        "status": "verified",
    }
    for key, value in expected.items():
        if evidence.get(key) != value:
            errors.append(f"{path}: {key} must equal {value!r}")

    if not isinstance(evidence.get("summary"), str) or not evidence["summary"].strip():
        errors.append(f"{path}: summary must be non-empty")

    try:
        datetime.fromisoformat(evidence["generated_at"].replace("Z", "+00:00"))
    except (AttributeError, KeyError, ValueError):
        errors.append(f"{path}: generated_at must be an ISO-8601 timestamp")

    recorded_changes = evidence.get("changed_files")
    if not isinstance(recorded_changes, list) or not all(
        isinstance(item, str) for item in recorded_changes
    ):
        errors.append(f"{path}: changed_files must be a list of paths")
    else:
        missing_changes = application_changes - set(recorded_changes)
        if missing_changes:
            errors.append(
                f"{path}: changed_files omits {', '.join(sorted(missing_changes))}"
            )

    approvals = evidence.get("approvals")
    if not isinstance(approvals, list):
        errors.append(f"{path}: approvals must be a list (empty is allowed)")
    elif any(
        not isinstance(item, dict)
        or item.get("status") not in {"approved", "not-required"}
        or not isinstance(item.get("evidence"), str)
        or not item["evidence"].strip()
        for item in approvals
    ):
        errors.append(f"{path}: approvals entries are malformed")

    errors.extend(validate_check_items(evidence, "verification", path))
    errors.extend(validate_check_items(evidence, "security_checks", path))
    return errors


def validate_work_request(
    work_request: str, application_changes: set[str]
) -> list[str]:
    directory = Path("delivery") / work_request
    errors = []

    for filename in sorted(EVIDENCE_FILES):
        path = directory / filename
        if not path.is_file():
            errors.append(f"Missing required evidence file: {path}")

    if errors:
        return errors

    for filename in EVIDENCE_FILES - {"release-evidence.json"}:
        errors.extend(validate_markdown(directory / filename, work_request))
    errors.extend(
        validate_release_evidence(
            directory / "release-evidence.json",
            work_request,
            application_changes,
        )
    )
    return errors


def main() -> int:
    args = parse_args()
    paths = changed_files(args.base, args.head)
    application_changes = {path for path in paths if is_application_file(path)}

    if not application_changes:
        print("No application changes; delivery evidence check not required.")
        return 0

    work_request_ids = changed_evidence_ids(paths)
    if not work_request_ids:
        print(
            "Application changes require changed delivery evidence in delivery/<id>/.",
            file=sys.stderr,
        )
        return 1

    errors = [
        error
        for work_request in sorted(work_request_ids)
        for error in validate_work_request(work_request, application_changes)
    ]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(
        "Validated delivery evidence for "
        + ", ".join(sorted(work_request_ids))
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
