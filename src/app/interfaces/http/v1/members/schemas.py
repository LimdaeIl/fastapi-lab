from pydantic import BaseModel, EmailStr, ConfigDict


class MeResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"id": 1, "email": "user1@example.com", "role": "user"}
        }
    )
    id: int
    email: EmailStr
    role: str


class AdminOnlyResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"ok": True, "admin": "admin1@example.com"}}
    )
    ok: bool
    admin: EmailStr
