"""PostgreSQL data-access functions."""

from collections.abc import Callable
from os import environ
from typing import Any, Protocol

import psycopg


class Cursor(Protocol):
    def __enter__(self) -> "Cursor": ...

    def __exit__(self, *args: object) -> None: ...

    def execute(self, query: str) -> None: ...

    def fetchone(self) -> tuple[Any, ...] | None: ...


class Connection(Protocol):
    def __enter__(self) -> "Connection": ...

    def __exit__(self, *args: object) -> None: ...

    def cursor(self) -> Cursor: ...


class GreetingNotFoundError(RuntimeError):
    """Raised when the database has no default greeting."""


def connection_parameters() -> dict[str, str | int]:
    """Build connection parameters entirely from environment variables."""

    parameters: dict[str, str | int] = {
        "host": environ.get("DB_HOST", "localhost"),
        "port": int(environ.get("DB_PORT", "5432")),
        "dbname": environ.get("DB_NAME", "hello_world"),
        "user": environ.get("DB_USER", "hello_world"),
        "connect_timeout": 5,
    }

    password = environ.get("DB_PASSWORD")
    if password:
        parameters["password"] = password

    return parameters


def connect() -> Connection:
    """Open a PostgreSQL connection using the configured environment."""

    return psycopg.connect(**connection_parameters())


def read_default_greeting(
    connection_factory: Callable[[], Connection] = connect,
) -> str:
    """Read the first seeded greeting through the data-access layer."""

    with connection_factory() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT message FROM greetings ORDER BY id LIMIT 1")
            row = cursor.fetchone()

    if row is None:
        raise GreetingNotFoundError("No greeting is configured")

    return str(row[0])

