from fastapi import Depends
from app.common.errors.app_exception import AppException
from app.common.errors.error_code import ErrorCode
from app.interfaces.http.dependencies.auth import get_current_member


def require_roles(*allowed_roles: str):
    def _dep(current=Depends(get_current_member)):
        if current.role not in allowed_roles:
            raise AppException(ErrorCode.BAD_REQUEST, "Forbidden", status_code=403)
        return current

    return _dep
