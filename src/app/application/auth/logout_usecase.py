from app.common.security.jwt import (
    safe_decode,
    require_token_type,
    get_jti,
    get_subject_member_id,
    get_token_version,
)
from app.infrastructure.redis.refresh_token_store import RefreshTokenStore
from app.domain.members.repositories.member_repository import MemberRepository


class LogoutUseCase:
    def __init__(self, member_repo: MemberRepository):
        self.refresh_store = RefreshTokenStore()
        self.member_repo = member_repo

    def execute(self, refresh_token: str) -> None:
        payload = safe_decode(refresh_token)
        require_token_type(payload, "refresh")

        jti = get_jti(payload)
        member_id = get_subject_member_id(payload)
        token_ver = get_token_version(payload)

        deleted = self.refresh_store.delete_if_exists(jti)
        if deleted:
            self.refresh_store.mark_revoked(jti, ttl_days=3)

            # 이미 버전이 올라간 상태면 더 올리지 않게(중복 bump 방지)
            member = self.member_repo.find_by_id(member_id)
            if member and member.token_version == token_ver:
                self.member_repo.bump_token_version(member_id)
