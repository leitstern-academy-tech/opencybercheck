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
OpenCyberCheck will follow privacy-by-design and secure-by-default principles:

**Local-First Processing:** Security and asset data are processed locally by default, without the need to transmit them to a proprietary cloud service.

**Data Minimization:** The toolkit will be designed to request and retain only the information necessary to perform the selected security checks.

**User Control:**  Users retain full control over assessment data, configuration files, and generated reports.

**Transparent Assessments:** Findings are generated through documented and auditable rules, rather than opaque or "black-box" decision-making mechanisms.

**Secure Handling of Sensitive Data:**  The toolkit will not require credentials or unnecessary sensitive data, and such information should not be included in configuration files or generated reports.

**Non-Intrusive Operation:**  The initial version analyzes information provided directly by the user; it does not conduct intrusive testing or active penetration activities.

## Project status
OpenCyberCheck is currently in the early planning and design phase. The project's public repository, initial scope, and open-source license have been established.

The next steps are:

- Defining the technical architecture and rule schema.
- Developing a minimal proof of concept (PoC).
- Validating the initial security checks using sample data.

The project is not yet ready for production use. Its interfaces and assessment rules may change during the development process.

## Roadmap
OpenCyberCheck's initial development roadmap consists of six stages:

**Architecture and Rule Schema:** Defining the project architecture, data model, threat model, and machine-readable security rule format.

**Rule Engine:** Developing the core engine to load, validate, and evaluate transparent YAML or JSON security rules.

**Assessment Profile:** Creating structured asset and security profiles, complete with sample input data and validation mechanisms.

**Risk and Remediation:** Integrating severity classifications, security control references, and practical remediation guidance into the system.

**Reporting and Interfaces:** Implementing human-readable reports and JSON/CSV outputs, alongside initial command-line or API interfaces.

**Testing and Public Release:** Finalizing automated tests, documentation, and packaging to release the first publicly usable development release.

The roadmap is subject to updates based on technical developments, user feedback, and available resources. Planned changes will be shared publicly in this project repository.

## Contributing
We welcome contributions, suggestions, and feedback. You can support the project, which is currently in its early development stage, by:

Suggesting relevant use cases and security rules.
Reviewing documentation and technical designs.
Testing sample assessment profiles and reporting reproducible issues.
Improving remediation guidance and security control mappings.
Sharing non-sensitive sample data for testing purposes.

Before initiating substantial changes, please open an issue to discuss your proposed approach. Pull requests should be focused and include relevant documentation and tests where appropriate.

Do not upload credentials, personal data, customer information, or sensitive infrastructure details to the repository. Please report suspected security vulnerabilities privately to info@lsacademytech.com rather than through a public issue.

Unless otherwise specified, all contributions will be licensed under the repository’s AGPL-3.0 license.

## License
OpenCyberCheck is licensed under the GNU Affero General Public License version 3.0 (AGPL-3.0).

You may use, study, modify, and redistribute this software in accordance with the terms of the license. If you modify the software and make it available to users over a network, you must also make the corresponding source code available under the AGPL-3.0.

See the LICENSE file for the complete license terms.
