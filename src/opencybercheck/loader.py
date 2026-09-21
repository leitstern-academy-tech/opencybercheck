"""Safe loading and schema validation for OpenCyberCheck data files."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class OpenCyberCheckDataError(ValueError):
    """Raised when an input file cannot be loaded or validated."""


def load_document(file_path: str | Path) -> dict[str, Any]:
    """Load a YAML or JSON document without executing arbitrary code."""
    path = Path(file_path)

    if not path.is_file():
        raise OpenCyberCheckDataError(f"File does not exist: {path}")

    try:
        with path.open("r", encoding="utf-8") as file_handle:
            if path.suffix.lower() == ".json":
                document = json.load(file_handle)
            elif path.suffix.lower() in {".yaml", ".yml"}:
                document = yaml.safe_load(file_handle)
            else:
                raise OpenCyberCheckDataError(
                    f"Unsupported file format: {path.suffix or '(none)'}"
                )
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise OpenCyberCheckDataError(
            f"Unable to parse structured data in: {path}"
        ) from exc
    except OSError as exc:
        raise OpenCyberCheckCheckDataError(f"Unable to read file: {path}") from exc

    if not isinstance(document, Mapping):
        raise OpenCyberCheckDataError(
            f"The top-level content must be an object: {path}"
        )

    return dict(document)


def validate_document(
    document: Mapping[str, Any],
    schema: Mapping[str, Any],
    document_name: str,
) -> None:
    """Validate a document and return concise, deterministic errors."""
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )

    if not errors:
        return

    messages: list[str] = []

    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path)
        location = location or "<root>"
        messages.append(f"{location}: {error.message}")

    raise OpenCyberCheckDataError(
        f"Validation failed for {document_name}:\n- "
        + "\n- ".join(messages)
    )


def load_profile(
    profile_path: str | Path,
    schema_path: str | Path,
) -> dict[str, Any]:
    """Load and validate an assessment profile."""
    profile = load_document(profile_path)
    schema = load_document(schema_path)
    validate_document(profile, schema, str(profile_path))
    return profile


def load_rules(
    rules_directory: str | Path,
    schema_path: str | Path,
) -> list[dict[str, Any]]:
    """Load and validate all supported rule files in a directory."""
    directory = Path(rules_directory)

    if not directory.is_dir():
        raise OpenCyberCheckDataError(
            f"Rules directory does not exist: {directory}"
        )

    schema = load_document(schema_path)
    rule_paths = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml", ".json"}
    )

    if not rule_paths:
        raise OpenCyberCheckDataError(
            f"No supported security rule files found in: {directory}"
        )

    rules: list[dict[str, Any]] = []
    rule_ids: set[str] = set()

    for rule_path in rule_paths:
        rule = load_document(rule_path)
        validate_document_document(rule, schema, str(rule_path))

        rule_id = rule["id"]
        if rule_id in rule_ids:
            raise OpenCyberCheckDataError(
                f"Duplicate security rule identifier: {rule_id}"
            )

        rule_ids.add(rule_id)
        rules.append(rule)

    return rules
