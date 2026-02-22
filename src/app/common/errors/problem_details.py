from typing import Any
from pydantic import BaseModel, ConfigDict


class ProblemDetails(BaseModel):
    """
    RFC 9457 (Problem Details for HTTP APIs) compatible payload.
    Extension members are allowed (e.g., code, errors, trace_id).
    """
    model_config = ConfigDict(extra="allow")

    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None

    # optional extension members (common)
    code: str | None = None
    errors: Any | None = None
    trace_id: str | None = None