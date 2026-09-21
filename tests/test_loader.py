"""Tests for OpenCyberCheck data loading and schema validation."""

from pathlib import Path

import pytest

from opencybercheck.loader import (
    OpenCyberCheckDataError,
    load_document,
    load_profile,
    load_rules,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROFILE_SCHEMA = (
    PROJECT_ROOT / "schemas" / "assessment-profile.schema.json"
)
RULE_SCHEMA = (
    PROJECT_ROOT / "schemas" / "security-rule.schema.json"
)
SAMPLE_PROFILE = (
    PROJECT_ROOT / "examples" / "sample-profile.yaml"
)
RULES_DIRECTORY = PROJECT_ROOT / "rules"


def test_load_yaml_document(tmp_path: Path) -> None:
    file_path = tmp_path / "profile.yaml"
    file_path.write_text(
        "schema_version: '0.1'\n"
        "enabled: true\n",
        encoding="utf-8",
    )

    document = load_document(file_path)

    assert document["schema_version"] == "0.1"
    assert document["enabled"] is True


def test_load_json_document(tmp_path: Path) -> None:
    file_path = tmp_path / "profile.json"
    file_path.write_text(
        '{"schema_version": "0.1", "enabled": false}',
        encoding="utf-8",
    )

    document = load_document(file_path)

    assert document["schema_version"] == "0.1"
    assert document["enabled"] is False


def test_reject_unsupported_file_format(tmp_path: Path) -> None:
    file_path = tmp_path / "profile.txt"
    file_path.write_text("not supported", encoding="utf-8")

    with pytest.raises(
        OpenCyberCheckDataError,
        match="Unsupported file format",
    ):
        load_document(file_path)


def test_reject_non_object_document(tmp_path: Path) -> None:
    file_path = tmp_path / "profile.yaml"
    file_path.write_text(
        "- first\n- second\n",
        encoding="utf-8",
    )

    with pytest.raises(
        OpenCyberCheckDataError,
        match="top-level content must be an object",
    ):
        load_document(file_path)


def test_sample_profile_matches_schema() -> None:
    profile = load_profile(
        SAMPLE_PROFILE,
        PROFILE_SCHEMA,
    )

    assert profile["schema_version"] == "0.1"
    assert profile["organisation"]["size"] == "small"


def test_invalid_profile_is_rejected(tmp_path: Path) -> None:
    file_path = tmp_path / "invalid-profile.yaml"
    file_path.write_text(
        "schema_version: '0.1'\n"
        "organisation:\n"
        "  size: small\n",
        encoding="utf-8",
    )

    with pytest.raises(
        OpenCyberCheckDataError,
        match="Validation failed",
    ):
        load_profile(
            file_path,
            PROFILE_SCHEMA,
        )


def test_repository_rules_match_schema() -> None:
    rules = load_rules(
        RULES_DIRECTORY,
        RULE_SCHEMA,
    )

    rule_ids = {rule["id"] for rule in rules}

    assert rule_ids == {
        "OCC-BACKUP-001",
        "OCC-INCIDENT-001",
        "OCC-REMOTE-001",
    }


def test_rule_identifiers_are_unique() -> None:
    rules = load_rules(
        RULES_DIRECTORY,
        RULE_SCHEMA,
    )

    rule_ids = [rule["id"] for rule in rules]

    assert len(rule_ids) == len(set(rule_ids))
