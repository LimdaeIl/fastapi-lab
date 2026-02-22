from app.common.errors.app_exception import AppException
from app.common.errors.error_code import ErrorCode
from app.common.security.jwt import (
    safe_decode,
    require_token_type,
    get_jti,
    get_subject_member_id,
    get_token_version,
    create_access_token,
    create_refresh_token,
)
from app.infrastructure.redis.refresh_token_store import RefreshTokenStore
from app.domain.members.repositories.member_repository import MemberRepository


class RefreshUseCase:
    def __init__(self, member_repo: MemberRepository):
        self.refresh_store = RefreshTokenStore()
        self.member_repo = member_repo

    def _revoke_session_once(self, member_id: int, token_ver: int) -> None:
        """
        같은 refresh 재시도가 여러 번 들어와도 token_version이 무한히 오르지 않게:
        '현재 DB 버전 == 토큰 ver'일 때만 bump.
        """
        member = self.member_repo.find_by_id(member_id)
        if not member:
            return
        if member.token_version == token_ver:
            self.member_repo.bump_token_version(member_id)

    def execute(self, refresh_token: str) -> tuple[str, str]:
        payload = safe_decode(refresh_token)
        require_token_type(payload, "refresh")

        jti = get_jti(payload)
        member_id = get_subject_member_id(payload)
        token_ver = get_token_version(payload)

        member = self.member_repo.find_by_id(member_id)
        if not member:
            raise AppException(
                code=ErrorCode.TOKEN_INVALID,
                message="Invalid refresh token",
                status_code=401,
            )

        # 로그아웃/세션폐기 후 토큰이면 즉시 거절
        if member.token_version != token_ver:
            raise AppException(
                code=ErrorCode.TOKEN_REVOKED,
                message="Token revoked",
                status_code=401,
            )

        stored_member_id = self.refresh_store.get_member_id(jti)

        if stored_member_id is None:
            # revoked 기록이 있으면 -> rotate된 토큰 재사용(=replay) 확정
            if self.refresh_store.was_revoked(jti):
                self._revoke_session_once(member_id, token_ver)
                raise AppException(
                    code=ErrorCode.REFRESH_REUSE_DETECTED,
                    message="Refresh reuse detected. Session revoked.",
                    status_code=401,
                )

            # revoked 기록이 없으면 단순 invalid
            raise AppException(
                code=ErrorCode.TOKEN_INVALID,
                message="Invalid refresh token",
                status_code=401,
            )

        if stored_member_id != member_id:
            self._revoke_session_once(member_id, token_ver)
            raise AppException(
                code=ErrorCode.REFRESH_REUSE_DETECTED,
                message="Refresh reuse detected. Session revoked.",
                status_code=401,
            )

        # 정상 rotate: 기존 refresh 삭제 + revoked 마킹
        deleted = self.refresh_store.delete_if_exists(jti)
        if deleted:
            self.refresh_store.mark_revoked(jti, ttl_days=3)

        # 새 토큰 발급 (member.token_version 그대로)
        new_access = create_access_token(member_id, member.role, member.token_version)
        new_refresh, new_jti = create_refresh_token(member_id, member.role, member.token_version)
        self.refresh_store.save(new_jti, member_id)

        return new_access, new_refresh