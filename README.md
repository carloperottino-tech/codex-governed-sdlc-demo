# Governed SDLC three-tier demo

A public, customer-neutral Hello World application demonstrating a controlled
work-request-to-release workflow with Codex and the `governed-sdlc` plugin.
The baseline is intentionally small so the delivery workflow, approval
checkpoints, and evidence are easier to inspect than the application itself.

> `DEMO-101` is intentionally not implemented. It is the change used during the
> live demonstration.

## Architecture

```text
Browser
  │  http://localhost:8080
  ▼
Nginx (presentation tier)
  │  GET /api/greeting
  ▼
FastAPI (application tier)
  │  SELECT through app/database.py
  ▼
PostgreSQL (data tier)
```

- **Presentation:** static HTML, CSS, and vanilla JavaScript served by Nginx.
  The page shows explicit loading, success, and error states.
- **Application:** FastAPI exposes `GET /api/greeting` and `GET /health`.
  Greeting reads go through a small data-access layer.
- **Data:** PostgreSQL initializes a `greetings` table and seeds
  `Hello, world!`.

Nginx is the only published service. The API and database remain on the
Compose network. The local Compose profile uses PostgreSQL trust
authentication so the demo can start without embedding a password. This is a
local-only convenience and must not be used as a production authentication
configuration. If a password is required in another environment, inject it
with `DB_PASSWORD`; do not commit it.

## Prerequisites

- Docker Engine or Docker Desktop with Docker Compose v2
- `curl` for command-line smoke checks
- Python 3.11 or newer to run tests outside containers
- Codex CLI with `codex plugin` support for the governed workflow demo

The repository was initialized and verified with Codex CLI `0.144.4`.

## Run locally

Start all three tiers:

```bash
docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080).

In another terminal, check health and the end-to-end greeting:

```bash
curl --fail --silent http://localhost:8080/health
curl --fail --silent http://localhost:8080/api/greeting
```

Expected responses:

```json
{"status":"ok"}
{"greeting":"Hello, world!"}
```

Stop the application while preserving its local database volume:

```bash
docker compose down
```

To also remove the disposable demo data:

```bash
docker compose down --volumes
```

## Test and validate

Run the API unit and contract tests:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --requirement api/requirements-dev.txt
PYTHONPATH=api pytest api/tests
```

Run the baseline security checks and validate the Compose model:

```bash
bandit --recursive api/app
pip-audit --requirement api/requirements.txt
docker compose config --quiet
docker compose build
```

CI performs the same checks, starts the stack, executes smoke tests, and
validates delivery evidence whenever application or Compose files change.

## The companion marketplace and plugin pin

The companion
[`codex-enterprise-plugin-marketplace`](https://github.com/carloperottino-tech/codex-enterprise-plugin-marketplace)
repository is expected to publish:

- a marketplace named `codex-enterprise-plugin-marketplace`;
- a plugin named `governed-sdlc`;
- plugin manifest version `0.1.0`; and
- Git tag `v0.1.0` pointing at that marketplace snapshot.

Codex CLI `0.144.4` supports adding a Git marketplace at a specific ref and
installing a plugin from that marketplace:

```bash
codex plugin marketplace add \
  https://github.com/carloperottino-tech/codex-enterprise-plugin-marketplace \
  --ref v0.1.0
codex plugin add \
  governed-sdlc@codex-enterprise-plugin-marketplace
codex plugin list \
  --marketplace codex-enterprise-plugin-marketplace \
  --json
```

The final command must report `governed-sdlc` as installed and enabled with
version `0.1.0`. The repository also provides an equivalent bootstrap and
verification helper:

```bash
./scripts/bootstrap-governed-sdlc.sh
```

That script changes the invoking user's Codex plugin configuration. Review it
before running it.

At initialization time, the companion repository contains only its starter
README; it does not yet publish the marketplace manifest, plugin, or `v0.1.0`
tag. The bootstrap therefore cannot succeed until those artifacts are
published. This is the remaining companion-repository setup step, not a hidden
fallback in this repository.

### Why there is no `requirements.toml`

The installed Codex version has no native **project-level** plugin dependency
manifest. Its `requirements.toml` is a managed-policy input. In version
`0.144.4`, plugin entries there constrain plugin-provided MCP server
requirements; they do not install, enable, or version-pin a plugin.

Consequently this repository does not include a misleading
`requirements.toml`. The supported pin is the marketplace Git ref
`v0.1.0`, followed by a check that the resolved plugin manifest version is
`0.1.0`. Plugin installation remains user- or workspace-level state.

## Native Codex controls and repository conventions

| Capability | What it actually does |
| --- | --- |
| `codex plugin marketplace add --ref v0.1.0` | Natively resolves a marketplace snapshot at a Git ref. |
| `codex plugin add ...` | Natively installs the selected plugin into the user's Codex configuration/cache, subject to workspace policy. |
| Codex sandbox and approval settings | Natively constrain tool execution and requests for elevated actions. |
| Managed workspace plugin and app policy | Can control plugin availability and underlying app permissions when configured by an administrator. |
| `AGENTS.md` | Gives Codex repository instructions. It guides behavior; it is not tamper-proof enforcement or a security boundary. |
| `delivery/` artifacts | Provide a reviewable repository convention for scope, plans, decisions, verification, and release evidence. |
| CI evidence check | Mechanically fails application changes with missing, malformed, incomplete, or mismatched evidence. It validates artifacts, not the truth of unobservable human behavior. |
| Branch protection and required reviews | Must be configured manually in the Git hosting workspace to make CI/review gates merge-blocking. |

CI never treats the presence of `AGENTS.md` as proof that its instructions were
followed.

## DEMO-101 work request

The approved request is in
[`delivery/DEMO-101/request.md`](delivery/DEMO-101/request.md). Its future
workflow outputs belong beside it:

- `delivery/DEMO-101/plan.md`
- `delivery/DEMO-101/adr.md`
- `delivery/DEMO-101/verification.md`
- `delivery/DEMO-101/release-evidence.json`

Those files are deliberately absent in the baseline so no one mistakes
placeholder evidence for completed work.

## Complete live-demo sequence

1. Publish `governed-sdlc` `0.1.0` and marketplace tag `v0.1.0` in the
   companion repository.
2. Clone this repository and run `./scripts/bootstrap-governed-sdlc.sh`.
3. Verify the plugin list reports exactly version `0.1.0`.
4. Run `docker compose up --build` and show the default Hello World behavior at
   `http://localhost:8080`.
5. Show `delivery/DEMO-101/request.md`, the absent future output artifacts, and
   the relevant `AGENTS.md` instructions.
6. Start Codex in the repository and submit this exact prompt:

   > “Implement DEMO-101 using the required governed-sdlc workflow. Produce the plan and ADR, stop at any required approval checkpoint, implement the change across the appropriate tiers, run the tests, and produce the verification and release-evidence artifacts. Do not fabricate approvals.”

7. Inspect the generated plan and ADR before giving any requested approval.
   If approval is not granted, verify Codex remains stopped.
8. Record a real approval using the workflow mechanism defined by the plugin,
   then ask Codex to continue.
9. Review the implementation across the presentation, application, and data
   tiers. Confirm the unnamed request still returns `Hello, world!`.
10. Review test, security, Compose, and smoke-check output.
11. Inspect `verification.md` and `release-evidence.json`, then run:

    ```bash
    python scripts/check_delivery_evidence.py \
      --base "$(git merge-base HEAD origin/main)" \
      --head HEAD
    ```

12. Open a pull request and show CI plus any configured branch-protection and
    human-review gates. Explain that those controls, not `AGENTS.md` alone,
    provide mechanical merge enforcement.

## Repository layout

```text
.
├── .github/
│   ├── pull_request_template.md
│   └── workflows/ci.yml
├── api/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements-dev.txt
│   └── requirements.txt
├── db/
│   ├── Dockerfile
│   └── init.sql
├── delivery/
│   ├── BASELINE-001/
│   └── DEMO-101/
├── scripts/
├── web/
├── AGENTS.md
└── compose.yaml
```

This repository contains no production credentials, customer data, or
proprietary implementation details.
