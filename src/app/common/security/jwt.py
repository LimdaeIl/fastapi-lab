from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from jwt import InvalidTokenError, ExpiredSignatureError

from app.common.config.settings import settings
from app.common.errors.app_exception import AppException
from app.common.errors.error_code import ErrorCode


def _create_token(payload: dict, expires_delta: timedelta) -> str:
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
    )

    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(member_id: int, role: str, token_version: int) -> str:
    return _create_token(
        payload={
            "sub": str(member_id),
            "type": "access",
            "role": role,
            "ver": token_version,
        },
        expires_delta=timedelta(minutes=settings.jwt_access_expires_min),
    )


def create_refresh_token(
    member_id: int, role: str, token_version: int
) -> tuple[str, str]:
    jti = str(uuid4())
    token = _create_token(
        payload={
            "sub": str(member_id),
            "type": "refresh",
            "jti": jti,
            "role": role,
            "ver": token_version,
        },
        expires_delta=timedelta(days=settings.jwt_refresh_expires_days),
    )
    return token, jti


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )


def safe_decode(token: str) -> dict:
    try:
        return decode_token(token)
    except ExpiredSignatureError as e:
        raise AppException(
            code=ErrorCode.TOKEN_EXPIRED,
            message="Token expired",
            status_code=401,
        ) from e
    except InvalidTokenError as e:
        raise AppException(
            code=ErrorCode.TOKEN_INVALID,
            message="Invalid token",
            status_code=401,
        ) from e


def require_token_type(payload: dict, token_type: str) -> None:
    if payload.get("type") != token_type:
        raise AppException(
            code=ErrorCode.TOKEN_INVALID,
            message="Invalid token type",
            status_code=401,
        )


def get_subject_member_id(payload: dict) -> int:
    sub = payload.get("sub")
    if not sub or not str(sub).isdigit():
        raise AppException(
            code=ErrorCode.TOKEN_INVALID,
            message="Invalid subject",
            status_code=401,
        )
    return int(sub)


def get_jti(payload: dict) -> str:
    jti = payload.get("jti")
    if not jti:
        raise AppException(
            code=ErrorCode.TOKEN_INVALID,
            message="Missing jti",
            status_code=401,
        )
    return str(jti)


def get_token_version(payload: dict) -> int:
    ver = payload.get("ver")
    if ver is None:
        raise AppException(
            code=ErrorCode.TOKEN_INVALID,
            message="Missing token version",
            status_code=401,
        )
    try:
        return int(ver)
    except ValueError as e:
        raise AppException(
            code=ErrorCode.TOKEN_INVALID,
            message="Invalid token version",
            status_code=401,
        ) from e


def get_role(payload: dict) -> str:
    role = payload.get("role")
    if role not in ("user", "admin"):
        raise AppException(
            code=ErrorCode.TOKEN_INVALID,
            message="Invalid role",
            status_code=401,
        )
    return role
