from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RegisterMemberRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"email": "user1@example.com", "password": "Passw0rd!"},
                {"email": "admin1@example.com", "password": "Passw0rd!"},
            ]
        }
    )

    email: EmailStr = Field(description="회원 이메일")
    password: str = Field(
        min_length=8,
        max_length=72,
        description="비밀번호 (bcrypt UTF-8 72 bytes 이하)",
    )


class RegisterMemberResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "user1@example.com",
            }
        }
    )

    id: int = Field(description="회원 ID (BIGINT AUTO_INCREMENT)")
    email: EmailStr = Field(description="회원 이메일")


class MeResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "user1@example.com",
                "role": "user",
            }
        }
    )

    id: int
    email: EmailStr
    role: str


class AdminOnlyResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ok": True,
                "admin": "admin1@example.com",
            }
        }
    )

    ok: bool
    admin: EmailStr