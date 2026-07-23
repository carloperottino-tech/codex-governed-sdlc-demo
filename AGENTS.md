# Repository instructions for Codex

This repository demonstrates a governed software-delivery workflow. These
instructions are repository conventions for Codex; they are not a security
boundary and do not replace Codex sandboxing, approval controls, managed
workspace policy, source-system permissions, branch protection, or CI.

## Plugin-use contract

For every request:

1. Classify the work before acting and select the smallest set of installed
   plugins whose declared scope matches the request. Do not invoke unrelated
   plugins merely because they are installed.
2. When a plugin is selected, read and follow its current contributed skill
   instructions. Treat the plugin as the workflow source of truth; do not copy,
   reconstruct, or improvise its internal playbook in this file.
3. Confirm each required plugin is installed, enabled, and compatible in the
   active Codex session. If it is missing, disabled, or incompatible, stop the
   affected workflow and report the prerequisite instead of imitating it.
4. Apply every guardrail and stop condition from every selected plugin. When
   they differ, the narrowest scope and strictest safety or approval boundary
   wins.
5. Preserve evidence provenance. A specialist recommendation, test result,
   quality assessment, or release-evidence record is not a human approval,
   deployment authorization, or release decision.

For material application, infrastructure, or delivery-process changes,
`governed-sdlc` is mandatory. The pinned compatibility line is semantic version
`0.1.0`; installed build metadata such as `0.1.0+codex.<build>` is compatible
with that line. A different semantic version requires an explicit
compatibility review.

## Key workflow routing

Use the primary plugin below when its workflow applies. Add other plugins only
for the affected concerns.

| Workflow or decision | Primary plugin | Use when |
| --- | --- | --- |
| Product outcome, scope, priority, acceptance criteria, or issue shaping | `product-owner` | The request needs a decision-ready product definition or backlog handoff |
| User journey, interaction states, accessibility, research synthesis, or UX handoff | `ux-design` | User experience evidence or behavior must be defined before implementation |
| Enterprise or solution architecture, integration, data, standards, or durable trust-boundary decisions | `enterprise-architecture` | The decision has cross-system consequences or difficult reversibility |
| Governed change intake, planning, repository implementation, ADRs, verification, and release evidence | `governed-sdlc` | Any material repository change is proposed or executed |
| Risk-based test strategy, automation, integration, negative paths, performance, or defect reproduction | `test-engineering` | Test design or execution extends beyond the implementation's focused checks |
| Independent traceability, evidence-gap review, exception review, or readiness recommendation | `quality-assurance` | Quality readiness must be assessed independently of implementation |
| Threats, data handling, trust boundaries, dependency risk, vulnerabilities, controls, or residual security risk | `security-assurance` | Security or privacy impact exists or needs explicit review |
| Versioned artifact, dependency manifest, SBOM, provenance, digest, signature status, or registry readiness | `package-supply-chain` | A release artifact is being prepared or audited |
| Environment, infrastructure, pipeline, configuration, or authorized deployment change | `devops-platform` | Platform or deployment work is planned, reviewed, or executed |
| Evidence-backed rollout, approvals, communications, rollback triggers, or post-release checks | `ship-release` | A quality-reviewed package is being prepared for a release decision |
| SLOs, telemetry, capacity, resilience, recovery, or production-readiness review | `site-reliability` | Reliability evidence is needed before release or during reliability triage |
| Support, incident follow-up, problem management, runbook improvement, or operational feedback routing | `service-operations` | Operational evidence should become a safe action, knowledge update, or new work request |

Domain-specific plugins are opt-in, not part of this customer-neutral
repository's default workflow. Use one only when the request explicitly falls
within its domain and doing so does not introduce customer names, proprietary
details, restricted data, or domain assumptions into this public repository.

Connector and presentation plugins such as GitHub, Google Drive, Sites, or
Workspace Agents support an applicable workflow; they do not replace its
primary delivery plugin. Use them only when the user or selected plugin
authorizes the corresponding source access or external action.

## Multi-plugin sequencing

When several plugins apply, order work by evidence dependency:

1. Shape the outcome and acceptance criteria with `product-owner`.
2. Resolve relevant UX, architecture, and security questions with `ux-design`,
   `enterprise-architecture`, and `security-assurance`.
3. Use `governed-sdlc` for bounded intake, planning, approved implementation,
   repository verification, and evidence assembly.
4. Use `test-engineering` for risk-based test design and execution.
5. Use `quality-assurance` for an independent, revision-aligned readiness
   assessment.
6. Use `package-supply-chain` for artifact and provenance evidence.
7. Use `ship-release`, `devops-platform`, and `site-reliability` for the
   separately authorized release plan, deployment/platform action, and
   production-readiness assessment.
8. Use `service-operations` to route post-release evidence and recurring
   operational feedback into governed follow-up work.

Skip stages that do not apply, but record why a material specialist review was
not required. Do not collapse implementation, independent quality review, and
release authority into one claimed approval.

## Required governed workflow for material changes

1. Begin with an approved work request under
   `delivery/<work-request-id>/`. Treat it as the scope and
   acceptance-criteria source.
2. Use the applicable `governed-sdlc` intake or planning skill and create
   `delivery/<work-request-id>/plan.md` before editing application,
   infrastructure, or delivery-process code or configuration.
3. Create `delivery/<work-request-id>/adr.md` for material design or operating
   model decisions. Keep a proposed ADR proposed until an authorized decider
   explicitly accepts it.
4. Stop at every explicit human-approval checkpoint required by any selected
   plugin or work request. Never fabricate, infer, or backfill an approval.
5. Implement only the approved scope and validate every affected tier and
   concern.
6. Run the relevant static, unit, API, integration, Compose, security,
   compatibility, recovery, and smoke checks identified by the plan and
   selected specialist plugins.
7. Record reproducible results in
   `delivery/<work-request-id>/verification.md`.
8. Create
   `delivery/<work-request-id>/release-evidence.json` and validate it with
   `scripts/check_delivery_evidence.py`.
9. Stop before commit, push, pull request, merge, deployment, publication,
   tagging, or release unless the user explicitly authorizes that action and
   all applicable controls permit it.

If instructions conflict, follow the higher-priority instruction and record
the conflict in the plan or verification report. Do not claim that following
this file or invoking a plugin alone proves compliance.

## DEMO-101

`delivery/DEMO-101/request.md` is approved for a future live demo. It has not
been implemented in the baseline. Do not edit application code for DEMO-101
until explicitly asked to run that work request.
