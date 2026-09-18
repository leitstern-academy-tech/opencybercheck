# OpenCyberCheck

Open-source cybersecurity assessment and remediation toolkit for European SMEs.

## Problem
SMEs often struggle to access affordable and transparent tools for assessing their cybersecurity posture. Existing commercial solutions can be expensive and complex, while dependence on closed cloud services may create vendor lock-in and data privacy concerns. Many current tools merely list vulnerabilities without providing a clear and prioritised path to remediation. SMEs therefore need an open-source, locally deployable toolkit that produces understandable security findings and practical remediation guidance.

## Proposed solution
OpenCyberCheck will provide an open-source, locally deployable toolkit designed to assess the cybersecurity posture of SMEs. The system analyzes structured asset and security data using transparent, customizable rules defined in machine-readable YAML or JSON formats. The toolkit prioritizes identified risks, maps technical findings to relevant security control references, and generates actionable recommendations for improvement. The results are presented in both human-readable reports and machine-processable formats, enabling users and other systems to review, reuse, and integrate the findings without reliance on a proprietary cloud platform.

## Target users
OpenCyberCheck’s primary users are European SMEs seeking a practical way to assess and improve their cybersecurity posture without deploying complex commercial platforms.

The toolkit may also support:

- Small IT service providers and cybersecurity consultants conducting structured security assessments for their clients.

- Educational institutions and training providers using transparent rules and sample scenarios to teach fundamental security controls and remediation processes in hands-on learning environments.

## Core components
The OpenCyberCheck project will be structured around the following fundamental components:

**Asset and Security Profile:** A structured YAML or JSON format used to define systems, user accounts, remote access services, backup arrangements, and other relevant security information.

**Transparent Rule Engine:** A configurable mechanism that evaluates the provided data against clearly documented security rules.

**Risk Prioritization:** A system that classifies findings based on severity, determining which issues users should address first.

**Security Control Mapping:** A reference layer that links technical findings to relevant security frameworks and regulatory references, including NIS2, CIS Controls and applicable BSI guidance without duplicating the protected standard texts.

**Remediation Guidance:** Actionable and verifiable remediation steps for each identified security issue.

**Reporting and Integration Formats:** Human-readable reports and machine-processable JSON or CSV outputs that enable the review, reuse, or integration of findings with other tools.

## Privacy and security principles

## Project status

## Roadmap

## Contributing

## License
