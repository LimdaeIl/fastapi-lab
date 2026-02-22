from sqlalchemy.orm import Session

from app.domain.members.entities.member import Member
from app.domain.members.repositories.member_repository import MemberRepository
from sqlalchemy import update
from app.infrastructure.db.models.member_model import MemberModel

class SqlAlchemyMemberRepository(MemberRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, member: Member) -> Member:
        row = MemberModel(
            email=member.email,
            password_hash=member.password_hash,

        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)  # 여기서 row.id가 채워짐
        return Member(
            id=row.id,
            email=row.email,
            password_hash=row.password_hash,
            role=row.role,
            token_version=row.token_version,
            created_at=row.created_at,
        )

    def find_by_email(self, email: str) -> Member | None:
        row = self.db.query(MemberModel).filter(MemberModel.email == email).first()
        if not row:
            return None
        return Member(
            id=row.id,
            email=row.email,
            password_hash=row.password_hash,
            role=row.role,
            token_version=row.token_version,
            created_at=row.created_at,
        )

    def find_by_id(self, member_id: int) -> Member | None:
        row = self.db.get(MemberModel, member_id)
        if not row:
            return None
        return Member(
            id=row.id,
            email=row.email,
            password_hash=row.password_hash,
            role=row.role,
            token_version=row.token_version,
            created_at=row.created_at,
        )

    def bump_token_version(self, member_id: int) -> None:
        self.db.execute(
            update(MemberModel)
            .where(MemberModel.id == member_id)
            .values(token_version=MemberModel.token_version + 1)
        )
        self.db.commit()