from pydantic import BaseModel, EmailStr, ConfigDict, Field


class LoginRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"email": "user1@example.com", "password": "Passw0rd!"},
                {"email": "admin1@example.com", "password": "Passw0rd!"},
            ]
        }
    )

    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class TokenResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...(access)",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...(refresh)",
                "token_type": "bearer",
            }
        }
    )

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...(refresh)"
            }
        }
    )

    refresh_token: str


class LogoutRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...(refresh)"
            }
        }
    )

    refresh_token: str


class SignupRequest(BaseModel):
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


class SignupResponse(BaseModel):
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
