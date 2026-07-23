"""FastAPI entrypoint for the Hello World application."""

import psycopg
from fastapi import FastAPI, HTTPException, status

from app.database import GreetingNotFoundError, read_default_greeting
from app.models import GreetingResponse, HealthResponse

app = FastAPI(title="Governed SDLC Hello World API", version="1.0.0")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Report that the API process is ready to receive requests."""

    return HealthResponse(status="ok")


@app.get("/api/greeting", response_model=GreetingResponse)
def greeting() -> GreetingResponse:
    """Return the default greeting stored in PostgreSQL."""

    try:
        message = read_default_greeting()
    except (GreetingNotFoundError, psycopg.Error) as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Greeting data is unavailable",
        ) from error

    return GreetingResponse(greeting=message)

