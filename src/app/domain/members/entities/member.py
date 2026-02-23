from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from app.common.time import now_kst


Role = Literal["partner", "admin"]


@dataclass
class Member:
    id: int | None
    email: str
    name: str
    password: str
    role: Role
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(email: str, password: str, name: str) -> "Member":
        now = now_kst()
        return Member(
            id=None,
            email=email,
            name=name,
            password=password,
            role="partner",
            created_at=now,
            updated_at=now,
        )

    def touch(self) -> None:
        self.updated_at = now_kst()
