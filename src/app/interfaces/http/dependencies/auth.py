from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.common.errors.app_exception import AppException
from app.common.errors.error_code import ErrorCode
from app.common.security.jwt import safe_decode, require_token_type, get_subject_member_id, get_token_version
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.sqlalchemy_member_repository import SqlAlchemyMemberRepository

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_member(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AppException(ErrorCode.TOKEN_INVALID, "Not authenticated", status_code=401)

    payload = safe_decode(credentials.credentials)
    require_token_type(payload, "access")
    member_id = get_subject_member_id(payload)
    token_ver = get_token_version(payload)

    repo = SqlAlchemyMemberRepository(db)
    member = repo.find_by_id(member_id)
    if not member:
        raise AppException(ErrorCode.TOKEN_INVALID, "User not found", status_code=401)

    if member.token_version != token_ver:
        raise AppException(ErrorCode.TOKEN_REVOKED, "Token revoked", status_code=401)

    return member