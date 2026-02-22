from app.domain.members.repositories.member_repository import MemberRepository
from app.common.security.password import verify_password
from app.common.security.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.infrastructure.redis.refresh_token_store import RefreshTokenStore
from app.common.errors.app_exception import AppException
from app.common.errors.error_code import ErrorCode



class LoginUseCase:

    def __init__(self, repo: MemberRepository):
        self.repo = repo
        self.refresh_store = RefreshTokenStore()

    def execute(self, email: str, password: str):
        member = self.repo.find_by_email(email)

        if not member:
            raise AppException(
                ErrorCode.INVALID_CREDENTIALS,
                "Invalid credentials",
                status_code=401,
            )

        if not verify_password(password, member.password_hash):
            raise AppException(
                ErrorCode.INVALID_CREDENTIALS,
                "Invalid credentials",
                status_code=401,
            )

        access_token = create_access_token(member.id, member.role,
                                           member.token_version)
        refresh_token, jti = create_refresh_token(member.id, member.role,
                                                  member.token_version)

        self.refresh_store.save(jti, member.id)

        return access_token, refresh_token