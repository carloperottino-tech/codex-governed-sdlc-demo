# Repository instructions for Codex

This repository demonstrates a governed software-delivery workflow. These
instructions are repository conventions for Codex; they are not a security
boundary and do not replace Codex sandboxing, approval controls, managed
workspace policy, branch protection, or CI.

## Required workflow for material changes

1. Confirm that the `governed-sdlc` plugin version `0.1.0` is installed and
   available. Use the plugin for every material application, infrastructure,
   or delivery-process change. If it is unavailable, stop and report the
   missing prerequisite instead of imitating its workflow.
2. Begin with the approved work request under `delivery/<work-request-id>/`.
   Treat that request as the scope and acceptance-criteria source.
3. Create `delivery/<work-request-id>/plan.md` before editing application code.
4. Create `delivery/<work-request-id>/adr.md` for material design decisions.
5. Stop at every explicit human-approval checkpoint required by the plugin or
   work request. Never fabricate, infer, or backfill an approval.
6. Implement only the approved scope and validate every affected tier.
7. Run the relevant unit, API, integration, Compose, security, and smoke checks.
8. Record results in `delivery/<work-request-id>/verification.md`.
9. Create a machine-readable
   `delivery/<work-request-id>/release-evidence.json` that passes
   `scripts/check_delivery_evidence.py`.

If instructions conflict, follow the higher-priority instruction and record
the conflict in the plan or verification report. Do not claim that following
this file alone proves compliance.

## DEMO-101

`delivery/DEMO-101/request.md` is approved for a future live demo. It has not
been implemented in the baseline. Do not edit application code for DEMO-101
until explicitly asked to run that work request.

