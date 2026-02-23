from typing import Generic, TypeVar, Any
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="forbid")

    data: T
    meta: dict[str, Any] | None = None
