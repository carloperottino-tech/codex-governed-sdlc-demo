"""API contract tests."""

import psycopg
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_greeting(monkeypatch) -> None:
    monkeypatch.setattr(main, "read_default_greeting", lambda: "Hello, world!")

    response = client.get("/api/greeting")

    assert response.status_code == 200
    assert response.json() == {"greeting": "Hello, world!"}


def test_greeting_hides_database_errors(monkeypatch) -> None:
    def fail() -> str:
        raise psycopg.OperationalError("database detail that must not be exposed")

    monkeypatch.setattr(main, "read_default_greeting", fail)

    response = client.get("/api/greeting")

    assert response.status_code == 503
    assert response.json() == {"detail": "Greeting data is unavailable"}
    assert "database detail" not in response.text

