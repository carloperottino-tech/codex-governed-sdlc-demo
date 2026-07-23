"""API response models."""

from pydantic import BaseModel


class GreetingResponse(BaseModel):
    """A greeting returned by the application."""

    greeting: str


class HealthResponse(BaseModel):
    """Service health state."""

    status: str

