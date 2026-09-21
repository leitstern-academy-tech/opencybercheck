"""Deterministic rule evaluation engine for OpenCyberCheck."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

_MISSING = object()


def get_path(data: Mapping[str, Any], path: str) -> Any:
    """Return a value from a nested mapping using a dot-separated path."""
    current: Any = data

    for part in path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return _MISSING
        current = current[part]

    return current


def evaluate_condition(
    profile: Mapping[str, Any],
    condition: Mapping[str, Any],
) -> bool:
    """Evaluate one restricted condition against an assessment profile."""
    path = condition["path"]
    operator = condition["operator"]
    expected = condition.get("expected")
    actual = get_path(profile, path)

    if operator == "missing":
        return actual is _MISSING

    if actual is _MISSING:
        return False

    if operator == "equals":
        return actual == expected

    if operator == "not_equals":
        return actual != expected

    comparison_operators = {
        "less_than": lambda left, right: left < right,
        "less_than_or_equal": lambda left, right: left <= right,
        "greater_than": lambda left, right: left > right,
        "greater_than_or_equal": lambda left, right: left >= right,
    }

    if operator not in comparison_operators:
        raise ValueError(f"Unsupported condition operator: {operator}")

    try:
        return comparison_operators[operator](actual, expected)
    except TypeError as exc:
        raise ValueError(
            f"Values at '{path}' cannot be compared with operator '{operator}'"
        ) from exc


def evaluate_rule(
    profile: Mapping[str, Any],
    rule: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Evaluate one rule and return a finding when its condition matches."""
    if not evaluate_condition(profile, rule["condition"]):
        return None

    return {
        "rule_id": rule["id"],
        "rule_version": rule["version"],
        "title": rule["title"],
        "category": rule["category"],
        "severity": rule["severity"],
        "message": rule["message"],
        "remediation": rule["remediation"],
        "references": list(rule.get("references", [])),
        "tags": list(rule.get("tags", [])),
    }


def evaluate_rules(
    profile: Mapping[str, Any],
    rules: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Evaluate multiple rules and return all generated findings."""
    findings: list[dict[str, Any]] = []

    for rule in rules:
        finding = evaluate_rule(profile, rule)
        if finding is not None:
            findings.append(finding)

    return findings
