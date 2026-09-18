# OpenCyberCheck Architecture

## Purpose

This document describes the initial technical architecture of OpenCyberCheck. The architecture is intentionally modular so that security rules, assessment profiles, and output formats can evolve independently.

OpenCyberCheck will initially operate as a local command-line application. It will evaluate structured information supplied by the user and will not perform active network scanning or penetration testing.

## Design goals

The initial architecture is guided by the following goals:

* Local-first processing.
* Transparent and auditable security rules.
* Minimal collection of security and asset data.
* Deterministic and reproducible assessments.
* Clear separation between input data, evaluation logic, and reports.
* Human-readable and machine-processable outputs.
* Extensibility without dependence on a proprietary cloud service.

## High-level data flow

The initial assessment process consists of the following stages:

1. The user provides an assessment profile in YAML or JSON format.
2. The input validator checks the profile against the published schema.
3. The rule loader loads and validates applicable security rules.
4. The rule engine evaluates the profile against those rules.
5. The risk processor assigns severity and priority information.
6. The remediation component attaches practical improvement guidance.
7. The reporting component produces human-readable and structured results.

## Core components

### Assessment profile

The assessment profile describes relevant organisational and technical information, such as:

* Systems and devices.
* User and administrator accounts.
* Authentication controls.
* Remote-access services.
* Backup arrangements.
* Patch-management practices.
* Logging and incident-response capabilities.

The profile must not contain passwords, private keys, access tokens, or unnecessary personal information.

### Schema validator

The schema validator checks the structure, types, required fields, and supported values of an assessment profile before evaluation begins. Invalid input should produce clear error messages without exposing sensitive information.

### Rule loader

The rule loader reads security rules defined in YAML or JSON. Each rule will contain a unique identifier, title, description, severity, evaluation condition, remediation guidance, and optional security-control references.

### Rule engine

The rule engine evaluates validated profile data against the loaded rules. The initial implementation will use deterministic conditions and will not depend on opaque machine-learning decisions.

### Risk processor

The risk processor classifies findings by severity and provides a consistent basis for prioritisation. The initial severity levels are expected to include:

* Informational
* Low
* Medium
* High
* Critical

### Remediation guidance

Each finding should include understandable and verifiable remediation guidance. Recommendations should explain the expected security outcome without requiring a specific commercial product.

### Reporting

The reporting component will initially support:

* A human-readable command-line report.
* A machine-processable JSON report.
* A CSV export for further analysis.

Reports must avoid exposing credentials or unnecessary sensitive information.

## Trust boundaries

Assessment profiles, rules, and generated reports are treated as untrusted local data. The implementation should validate all input before processing it.

The initial version will not:

* Transmit assessment data to an external service.
* Execute commands contained in profile or rule files.
* Perform active exploitation or penetration testing.
* Require access to production credentials.
* Modify the assessed systems automatically.

## Initial repository structure

The planned repository structure is:

```text
docs/          Architecture and technical documentation
examples/      Non-sensitive sample assessment profiles
rules/         Machine-readable security rules
schemas/       JSON schemas for profiles and rules
src/           Application source code
tests/         Automated tests and test data
```

## Initial technology choices

The proof of concept is planned as a Python application with YAML and JSON input support. JSON Schema will be used where appropriate for structural validation.

These choices may change following implementation experience, security review, and community feedback.

## Future considerations

Future versions may add:

* A documented local API.
* Additional reporting formats.
* Rule packages for specific SME environments.
* Digitally signed rule bundles.
* Optional integrations with external systems.
* Internationalisation and multilingual remediation guidance.

Any future network-connected functionality will require a separate security and privacy review.
