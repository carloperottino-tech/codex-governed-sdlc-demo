"""Unit tests for the data-access layer."""

from collections.abc import Sequence
from typing import Any

import pytest

from app.database import GreetingNotFoundError, connection_parameters, read_default_greeting


class FakeCursor:
    def __init__(self, row: tuple[Any, ...] | None) -> None:
        self.row = row
        self.query = ""

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def execute(self, query: str) -> None:
        self.query = query

    def fetchone(self) -> tuple[Any, ...] | None:
        return self.row


class FakeConnection:
    def __init__(self, row: tuple[Any, ...] | None) -> None:
        self.cursor_instance = FakeCursor(row)

    def __enter__(self) -> "FakeConnection":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def cursor(self) -> FakeCursor:
        return self.cursor_instance


@pytest.mark.parametrize(
    ("row", "expected"),
    [
        (("Hello, world!",), "Hello, world!"),
        (("A second greeting",), "A second greeting"),
    ],
)
def test_read_default_greeting(row: Sequence[str], expected: str) -> None:
    connection = FakeConnection(tuple(row))

    result = read_default_greeting(lambda: connection)

    assert result == expected
    assert connection.cursor_instance.query == (
        "SELECT message FROM greetings ORDER BY id LIMIT 1"
    )


def test_read_default_greeting_requires_a_record() -> None:
    with pytest.raises(GreetingNotFoundError):
        read_default_greeting(lambda: FakeConnection(None))


def test_connection_parameters_use_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DB_HOST", "database.example")
    monkeypatch.setenv("DB_PORT", "6543")
    monkeypatch.setenv("DB_NAME", "greetings")
    monkeypatch.setenv("DB_USER", "service")
    monkeypatch.setenv("DB_PASSWORD", "injected-at-runtime")

    assert connection_parameters() == {
        "host": "database.example",
        "port": 6543,
        "dbname": "greetings",
        "user": "service",
        "password": "injected-at-runtime",
        "connect_timeout": 5,
    }

