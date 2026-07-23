# BASELINE-001 verification

This report records verification of the uncommitted initialization worktree on
2026-07-22.

## Results

- `PYTHONPATH=/workspace pytest -p no:cacheprovider tests`: **passed**, 7
  tests.
- `bandit --recursive app`: **passed**, no issues identified.
- `pip-audit --requirement requirements.txt`: **passed**, no known
  vulnerabilities.
- `docker compose config --quiet`: **passed**.
- `docker compose build --pull`: **passed** for the Nginx, FastAPI, and
  PostgreSQL images.
- PostgreSQL and FastAPI Compose health checks: **passed**.
- `GET /health` through Nginx: **passed**, returned `{"status":"ok"}`.
- `GET /api/greeting` through Nginx, FastAPI, the data-access layer, and
  PostgreSQL: **passed**, returned `{"greeting":"Hello, world!"}`.
- Seed verification query: **passed**, PostgreSQL contained
  `1|Hello, world!`.
- `python3 scripts/check_delivery_evidence.py --base HEAD --head WORKTREE`:
  **passed** for `BASELINE-001`.

## Local port note

An unrelated pre-existing Docker container already occupied host port 8080.
The committed Compose model correctly publishes 8080, but the local smoke run
attached the built Nginx image to the same Compose network on temporary host
port 18080. No unrelated container was stopped or changed. A clean machine or
CI runner can use the documented `docker compose up --build` command on 8080.
