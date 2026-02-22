from dataclasses import dataclass
from datetime import datetime
from typing import Literal

Role = Literal["user", "admin"]


@dataclass
class Member:
    id: int | None
    email: str
    password_hash: str
    role: Role
    token_version: int
    created_at: datetime

    @staticmethod
    def create(email: str, password_hash: str) -> "Member":
        return Member(
            id=None,
            email=email,
            password_hash=password_hash,
            role="user",
            token_version=0,
            created_at=datetime.utcnow(),
        )