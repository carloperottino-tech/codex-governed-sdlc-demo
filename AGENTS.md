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
`0.2.0`; installed build metadata such as `0.2.0+codex.<build>` is compatible
with that line. A different semantic version requires an explicit
compatibility review.

For a request to implement or resume a GitHub Issue, the required entry skill
is `governed-sdlc-issue-to-review`. Confirm that the pinned plugin version and
that skill are active before proceeding. If either is unavailable, stop and
report the installation gap; do not recreate the missing orchestrator from
these repository instructions.

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

For the Issue-to-review workflow, GitHub and Google Drive are required source
connectors. Sites and Workspace Agents are optional presentation and
coordination surfaces and may be used only when explicitly requested. They are
never systems of record or approval authorities.

## Canonical GitHub Issue workflow

When a user asks to implement, start, take end to end, or resume a GitHub Issue,
select `governed-sdlc-issue-to-review` and let its current skill instructions
drive the work. The user does not need to enumerate every phase or plugin.

Use this source model:

- GitHub Issue discussion records the work request, scope, durable stage
  references, and accountable decisions.
- Linked, current Google Drive material supplies product, UX, architecture,
  policy, and durable collaboration context.
- The repository, branch or worktree, commits, tests, pull request, and CI
  contain implementation truth.
- The Codex task plan tracks in-session progress but is not the durable system
  of record.

The required governed states are:

```text
CONTEXT
→ PLAN_DRAFT → PLAN_APPROVED
→ DESIGN_DRAFT → DESIGN_APPROVED
→ BUILD
→ VERIFY
→ PR_REVIEW → REVIEW_APPROVED
```

Only an accountable human can approve the current Plan, current Design, or
current pull-request revision. A label, green check, generated artifact, Site,
Workspace Agent, specialist result, or agent statement is evidence, not
approval. Material changes return work to the earliest affected stage and make
downstream approvals and evidence stale.

After `REVIEW_APPROVED`, merge, packaging, release, deployment, evidence
publication, measurement, and improvement are separately authorized
continuations. An implementation request does not itself authorize Issue or
Drive writes, commits, pushes, pull-request creation, merge, release,
deployment, or external communication.

## Multi-plugin sequencing

When several plugins apply, use them as extensions around the governed
Issue-to-review stages:

1. Use `product-owner` to shape the outcome, Issue quality, and acceptance
   criteria before or during Context and Plan.
2. Resolve relevant UX, architecture, and security questions with `ux-design`,
   `enterprise-architecture`, and `security-assurance` during Plan or Design.
3. Keep `governed-sdlc-issue-to-review` as the owner of stage transitions,
   stale-state handling, and the three human gates.
4. Use `test-engineering` for deeper risk-based strategy and execution during
   Verify.
5. Use `quality-assurance` for an independent, revision-aligned readiness
   recommendation during pull-request Review; it does not approve the pull
   request.
6. After `REVIEW_APPROVED`, use `package-supply-chain` for artifact identity
   and provenance evidence.
7. Use `ship-release`, `devops-platform`, and `site-reliability` for the
   separately authorized release plan, deployment/platform action, and
   production-readiness assessment.
8. Use `service-operations` to route post-release evidence and recurring
   operational feedback into governed follow-up work.

Skip stages that do not apply, but record why a material specialist review was
not required. Do not collapse implementation, independent quality review, and
release authority into one claimed approval.

## Required governed workflow for material changes

1. For GitHub Issue-led work, use `governed-sdlc-issue-to-review` and the Issue
   as the durable workflow spine.
2. For an explicit repository-local request with no GitHub Issue, begin from
   the approved request under `delivery/<work-request-id>/`, use the applicable
   standalone `governed-sdlc` skills, and record why the Issue-led path does not
   apply.
3. Create the applicable Plan before editing application, infrastructure, or
   delivery-process code or configuration. For Issue-led work, stop for
   explicit approval of the current Plan before Design.
4. Create the applicable Design record or
   `delivery/<work-request-id>/adr.md` for material design or operating-model
   decisions. For Issue-led work, stop for explicit approval of the current
   Design before Build. Keep a proposed ADR proposed until an authorized
   decider explicitly accepts it.
5. Stop at every explicit human-approval checkpoint required by any selected
   plugin or work request. Never fabricate, infer, or backfill an approval.
6. Implement only the approved scope and validate every affected tier and
   concern.
7. Run the relevant static, unit, API, integration, Compose, security,
   compatibility, recovery, and smoke checks identified by the plan and
   selected specialist plugins.
8. Record reproducible results in
   `delivery/<work-request-id>/verification.md`.
9. Create
   `delivery/<work-request-id>/release-evidence.json` and validate it with
   `scripts/check_delivery_evidence.py`.
10. Stop before commit, push, pull request, merge, deployment, publication,
   tagging, or release unless the user explicitly authorizes that action and
   all applicable controls permit it.

If instructions conflict, follow the higher-priority instruction and record
the conflict in the plan or verification report. Do not claim that following
this file or invoking a plugin alone proves compliance.

## DEMO-101

`delivery/DEMO-101/request.md` is approved for a future live demo. It has not
been implemented in the baseline. Do not edit application code for DEMO-101
until explicitly asked to run that work request.
