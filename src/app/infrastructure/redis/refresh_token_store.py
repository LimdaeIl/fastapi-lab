from datetime import timedelta

from app.infrastructure.redis.client import redis_client
from app.common.config.settings import settings


class RefreshTokenStore:
    PREFIX = "refresh"
    REVOKED_PREFIX = "revoked_refresh"

    def _key(self, jti: str) -> str:
        return f"{self.PREFIX}:{jti}"

    def _revoked_key(self, jti: str) -> str:
        return f"{self.REVOKED_PREFIX}:{jti}"

    def save(self, jti: str, member_id: int):
        ttl = timedelta(days=settings.jwt_refresh_expires_days)
        redis_client.setex(self._key(jti), ttl, member_id)

    def get_member_id(self, jti: str) -> int | None:
        val = redis_client.get(self._key(jti))
        if val is None:
            return None
        try:
            return int(val)
        except ValueError:
            return None

    def delete_if_exists(self, jti: str) -> bool:
        return redis_client.delete(self._key(jti)) == 1

    # rotate/로그아웃 시 revoked 기록(짧은 TTL)
    def mark_revoked(self, jti: str, ttl_days: int = 3) -> None:
        ttl = timedelta(days=ttl_days)
        # 값은 굳이 필요 없어서 "1"로
        redis_client.setex(self._revoked_key(jti), ttl, "1")

    def was_revoked(self, jti: str) -> bool:
        return redis_client.exists(self._revoked_key(jti)) == 1