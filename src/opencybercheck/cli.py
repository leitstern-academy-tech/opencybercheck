"""Command-line interface for OpenCyberCheck."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from opencybercheck.engine import evaluate_rules
from opencybercheck.loader import (
    OpenCyberCheckDataError,
    load_profile,
    load_rules,
)


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="opencybercheck",
        description=(
            "Evaluate a structured cybersecurity assessment profile "
            "using transparent local security rules."
        ),
    )

    parser.add_argument(
        "profile",
        type=Path,
        help="Path to an assessment profile in YAML or JSON format.",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=Path("rules"),
        help="Directory containing security rules (default: rules).",
    )
    parser.add_argument(
        "--profile-schema",
        type=Path,
        default=Path("schemas/assessment-profile.schema.json"),
        help="Assessment profile schema path.",
    )
    parser.add_argument(
        "--rule-schema",
        type=Path,
        default=Path("schemas/security-rule.schema.json"),
        help="Security rule schema path.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format (default: text).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file. Standard output is used when omitted.",
    )

    return parser


def create_report(findings: list[dict[str, Any]]) -> dict[str, Any]:
    """Create a deterministic machine-processable report."""
    return {
        "report_version": "0.1",
        "findings_count": len(findings),
        "findings": findings,
    }


def render_text(findings: list[dict[str, Any]]) -> str:
    """Render findings as a human-readable text report."""
    if not findings:
        return "OpenCyberCheck assessment completed: no findings."

    lines = [
        "OpenCyberCheck assessment report",
        f"Findings: {len(findings)}",
        "",
    ]

    for index, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"{index}. [{finding['severity'].upper()}] {finding['title']}",
                f"   Rule: {finding['rule_id']}",
                f"   Category: {finding['category']}",
                f"   Finding: {finding['message']}",
                f"   Remediation: {finding['remediation']}",
                "",
            ]
        )

    return "\n".join(lines).rstrip()


def write_output(content: str, output_path: Path | None) -> None:
    """Write a report to standard output or an explicitly selected file."""
    if output_path is None:
        print(content)
        return

    try:
        output_path.write_text(content + "\n", encoding="utf-8")
    except OSError as exc:
        raise OpenCyberCheckDataError(
            f"Unable to write report: {output_path}"
        ) from exc


def main(argv: list[str] | None = None) -> int:
    """Run the OpenCyberCheck command-line application."""
    parser = build_parser()
    arguments = parser.parse_args(argv)

    try:
        profile = load_profile(
            arguments.profile,
            arguments.profile_schema,
        )
        rules = load_rules(
            arguments.rules,
            arguments.rule_schema,
        )
        findings = evaluate_rules(profile, rules)

        if arguments.format == "json":
            content = json.dumps(
                create_report(findings),
                indent=2,
                ensure_ascii=False,
            )
        else:
            content = render_text(findings)

        write_output(content, arguments.output)
    except OpenCyberCheckDataError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Rule evaluation error: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
