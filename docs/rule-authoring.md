# Security Rule Authoring Guide

## Purpose

OpenCyberCheck security rules are transparent, machine-readable checks defined in YAML or JSON. Each rule evaluates one value in an assessment profile and produces a finding when its condition matches.

Rules must remain deterministic, understandable, and safe to review. They must not contain executable code, shell commands, templates, or network requests.

## Rule structure

Each rule contains the following required fields:

- `id`: Stable and unique rule identifier.
- `version`: Semantic version of the rule.
- `title`: Short human-readable title.
- `description`: Explanation of the security concern.
- `category`: Assessment category associated with the rule.
- `severity`: Severity assigned to a matching finding.
- `condition`: Restricted condition evaluated against the profile.
- `message`: Message shown when the condition matches.
- `remediation`: Practical and product-neutral improvement guidance.

Rules may also include:

- `references`: Relevant framework or regulatory references.
- `tags`: Searchable lowercase labels.

## Rule identifiers

Rule identifiers use the following format:

```text
OCC-CATEGORY-NNN
```

Examples:

```text
OCC-AUTH-001
OCC-BACKUP-001
OCC-REMOTE-001
OCC-INCIDENT-001
```

Once published, an identifier should not be reused for a different security check.

## Supported categories

The initial rule schema supports:

- `authentication`
- `remote_access`
- `backups`
- `patch_management`
- `logging`
- `incident_response`

New categories require an update to the security-rule schema.

## Severity levels

Supported severity values are:

- `informational`
- `low`
- `medium`
- `high`
- `critical`

Severity should reflect the likely security impact and urgency of remediation. It should not be increased solely to attract attention.

## Conditions

A condition contains a dot-separated profile path, an operator, and—except for the `missing` operator—an expected value.

Example:

```yaml
condition:
  path: "remote_access.mfa_enabled"
  operator: "equals"
  expected: false
```

Supported operators are:

- `equals`
- `not_equals`
- `less_than`
- `less_than_or_equal`
- `greater_than`
- `greater_than_or_equal`
- `missing`

Example of a numeric threshold:

```yaml
condition:
  path: "backups.days_since_last_restore_test"
  operator: "greater_than"
  expected: 90
```

Example of an absent-field check:

```yaml
condition:
  path: "logging.retention_days"
  operator: "missing"
```

The current proof of concept supports one condition per rule. More complex logical combinations may be considered in a future schema version.

## Complete example

```yaml
id: "OCC-REMOTE-001"
version: "0.1.0"

title: "Multi-factor authentication is not enabled for remote access"

description: >-
  Remote access without multi-factor authentication increases the risk of
  unauthorised access when a password is stolen, reused, or guessed.

category: "remote_access"
severity: "high"

condition:
  path: "remote_access.mfa_enabled"
  operator: "equals"
  expected: false

message: >-
  Multi-factor authentication is not enabled for remote access.

remediation: >-
  Enable multi-factor authentication for every account permitted to access
  organisational systems remotely. Prefer phishing-resistant authentication
  methods where supported.

references:
  - framework: "CIS Controls v8"
    reference: "Safeguard 6.3 — Require MFA for Externally-Exposed Applications"

tags:
  - "mfa"
  - "remote-access"
  - "authentication"
```

## Remediation guidance

Remediation guidance should be:

- Clear and actionable.
- Verifiable after implementation.
- Independent of a specific commercial product.
- Proportionate to the severity of the finding.
- Understandable to an SME IT administrator or service provider.

Avoid vague recommendations such as “improve security” or “follow best practices.”

## References

References should identify relevant framework controls or regulatory provisions without copying protected standard text.

A reference may contain:

```yaml
- framework: "NIS2 Directive"
  reference: "Article 21(2)(b) — Incident handling"
```

References provide context and are not a declaration of legal or regulatory compliance.

## Security requirements

Rule files must not:

- Execute commands or scripts.
- Contain credentials or personal data.
- Make network requests.
- Modify the assessed system.
- Include confidential customer information.
- Claim that a single rule proves regulatory compliance.

## Validation and testing

Before submitting a rule:

1. Confirm that it matches `schemas/security-rule.schema.json`.
2. Test it against a non-sensitive sample profile.
3. Verify that it produces a finding when expected.
4. Verify that it does not produce a finding for a compliant value.
5. Add or update automated tests where appropriate.
6. Run the complete test suite:

```bash
python -m pytest
```

## Contributions

Before proposing a substantial rule set or schema change, open an issue describing the use case and intended assessment behaviour.

Follow the contribution requirements in [`CONTRIBUTING.md`](../CONTRIBUTING.md) and report security concerns according to [`SECURITY.md`](../SECURITY.md).
