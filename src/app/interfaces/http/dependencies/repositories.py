# app/interfaces/http/dependencies/repositories.py

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.sqlalchemy_member_repository import (
    SqlAlchemyMemberRepository,
)
from app.domain.members.repositories.member_repository import MemberRepository


def get_member_repo(db: Session = Depends(get_db)) -> MemberRepository:
    return SqlAlchemyMemberRepository(db)
