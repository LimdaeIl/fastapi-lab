from app.common.errors.error_code import ErrorCode


class AppException(Exception):
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = 400,
        detail=None,
        type: str | None = None,
        title: str | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail

        # Problem Details fields
        self.type = type  # e.g. "https://example.com/problems/invalid-credentials"
        self.title = title  # e.g. "Invalid Credentials"

        super().__init__(message)