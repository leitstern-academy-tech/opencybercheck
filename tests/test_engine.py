"""Tests for the deterministic OpenCyberCheck rule engine."""

from opencybercheck.engine import (
    evaluate_condition,
    evaluate_rule,
    evaluate_rules,
)


def example_rule() -> dict:
    """Return a minimal valid rule for engine tests."""
    return {
        "id": "OCC-REMOTE-001",
        "version": "0.1.0",
        "title": "Remote access MFA is missing",
        "description": "Remote access should be protected by MFA.",
        "category": "remote_access",
        "severity": "high",
        "condition": {
            "path": "remote_access.mfa_enabled",
            "operator": "equals",
            "expected": False,
        },
        "message": "MFA is not enabled for remote access.",
        "remediation": "Enable MFA for all remote-access accounts.",
        "references": [],
        "tags": ["mfa", "remote-access"],
    }


def test_equals_condition_matches_false_value() -> None:
    profile = {
        "remote_access": {
            "mfa_enabled": False,
        }
    }
    condition = {
        "path": "remote_access.mfa_enabled",
        "operator": "equals",
        "expected": False,
    }

    assert evaluate_condition(profile, condition) is True


def test_equals_condition_does_not_match_true_value() -> None:
    profile = {
        "remote_access": {
            "mfa_enabled": True,
        }
    }
    condition = {
        "path": "remote_access.mfa_enabled",
        "operator": "equals",
        "expected": False,
    }

    assert evaluate_condition(profile, condition) is False


def test_numeric_comparison_matches() -> None:
    profile = {
        "backups": {
            "days_since_last_restore_test": 120,
        }
    }
    condition = {
        "path": "backups.days_since_last_restore_test",
        "operator": "greater_than",
        "expected": 90,
    }

    assert evaluate_condition(profile, condition) is True


def test_missing_operator_detects_absent_value() -> None:
    profile = {
        "logging": {
            "security_logging_enabled": True,
        }
    }
    condition = {
        "path": "logging.retention_days",
        "operator": "missing",
    }

    assert evaluate_condition(profile, condition) is True


def test_rule_returns_finding_when_condition_matches() -> None:
    profile = {
        "remote_access": {
            "mfa_enabled": False,
        }
    }

    finding = evaluate_rule(profile, example_rule())

    assert finding is not None
    assert finding["rule_id"] == "OCC-REMOTE-001"
    assert finding["severity"] == "high"
    assert finding["category"] == "remote_access"


def test_rule_returns_none_when_condition_does_not_match() -> None:
    profile = {
        "remote_access": {
            "mfa_enabled": True,
        }
    }

    finding = evaluate_rule(profile, example_rule())

    assert finding is None


def test_multiple_rules_return_only_matching_findings() -> None:
    profile = {
        "remote_access": {
            "mfa_enabled": False,
        }
    }

    matching_rule = example_rule()
    non_matching_rule = {
        **example_rule(),
        "id": "OCC-REMOTE-002",
        "condition": {
            "path": "remote_access.mfa_enabled",
            "operator": "equals",
            "expected": True,
        },
    }

    findings = evaluate_rules(
        profile,
        [matching_rule, non_matching_rule],
    )

    assert len(findings) == 1
    assert findings[0]["rule_id"] == "OCC-REMOTE-001"
