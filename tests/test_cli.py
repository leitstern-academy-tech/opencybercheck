"""Tests for the OpenCyberCheck command-line interface."""

import json
from pathlib import Path

from opencybercheck.cli import main


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SAMPLE_PROFILE = (
    PROJECT_ROOT / "examples" / "sample-profile.yaml"
)
RULES_DIRECTORY = PROJECT_ROOT / "rules"
PROFILE_SCHEMA = (
    PROJECT_ROOT / "schemas" / "assessment-profile.schema.json"
)
RULE_SCHEMA = (
    PROJECT_ROOT / "schemas" / "security-rule.schema.json"
)


def base_arguments() -> list[str]:
    """Return CLI arguments using repository test data."""
    return [
        str(SAMPLE_PROFILE),
        "--rules",
        str(RULES_DIRECTORY),
        "--profile-schema",
        str(PROFILE_SCHEMA),
        "--rule-schema",
        str(RULE_SCHEMA),
    ]


def test_text_report_contains_expected_findings(capsys) -> None:
    exit_code = main(base_arguments())

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "OpenCyberCheck assessment report" in captured.out
    assert "Findings: 3" in captured.out
    assert "OCC-REMOTE-001" in captured.out
    assert "OCC-BACKUP-001" in captured.out
    assert "OCC-INCIDENT-001" in captured.out
    assert captured.err == ""


def test_json_report_is_machine_processable(capsys) -> None:
    arguments = [
        *base_arguments(),
        "--format",
        "json",
    ]

    exit_code = main(arguments)
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["report_version"] == "0.1"
    assert report["findings_count"] == 3
    assert len(report["findings"]) == 3


def test_json_report_can_be_written_to_file(
    tmp_path: Path,
    capsys,
) -> None:
    output_path = tmp_path / "report.json"
    arguments = [
        *base_arguments(),
        "--format",
        "json",
        "--output",
        str(output_path),
    ]

    exit_code = main(arguments)
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert captured.out == ""
    assert captured.err == ""
    assert report["findings_count"] == 3


def test_missing_profile_returns_error(capsys) -> None:
    missing_profile = PROJECT_ROOT / "examples" / "missing.yaml"
    arguments = [
        str(missing_profile),
        "--rules",
        str(RULES_DIRECTORY),
        "--profile-schema",
        str(PROFILE_SCHEMA),
        "--rule-schema",
        str(RULE_SCHEMA),
    ]

    exit_code = main(arguments)
    captured = capsys.readouterr()

    assert exit_code == 2
    assert captured.out == ""
    assert "File does not exist" in captured.err
