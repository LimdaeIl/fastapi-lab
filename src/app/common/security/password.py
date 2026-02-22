import bcrypt

from app.common.errors.app_exception import AppException
from app.common.errors.error_code import ErrorCode

BCRYPT_MAX_PASSWORD_BYTES = 72


def _to_bytes(password: str) -> bytes:
    return password.encode("utf-8")


def validate_password_for_bcrypt(password: str) -> None:
    if len(_to_bytes(password)) > BCRYPT_MAX_PASSWORD_BYTES:
        raise AppException(
            code=ErrorCode.BAD_REQUEST,
            message="Password is too long (bcrypt supports up to 72 bytes in UTF-8). Please use a shorter password.",
            status_code=400,
        )


def hash_password(password: str) -> str:
    validate_password_for_bcrypt(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(_to_bytes(password), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    validate_password_for_bcrypt(password)
    return bcrypt.checkpw(_to_bytes(password), hashed.encode("utf-8"))