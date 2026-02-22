from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.common.errors.app_exception import AppException
from app.common.errors.problem_details import ProblemDetails
from app.common.errors.error_code import ErrorCode

PROBLEM_JSON = "application/problem+json"

# 운영에서 type URI를 명확히 하려면 도메인 붙이는 걸 추천
# 예: https://api.yourdomain.com/problems/<code>
PROBLEM_TYPE_BASE = "https://example.com/problems"


def _problem_type(code: str) -> str:
    return f"{PROBLEM_TYPE_BASE}/{code.lower()}"


def _title_from_code(code: str) -> str:
    # 기본 title: CODE를 Title Case로
    return code.replace("_", " ").title()


def _trace_id(request: Request) -> str:
    # 추후 미들웨어에서 request.state.trace_id 세팅하면 그걸 쓰고,
    # 없으면 임시로 uuid4 사용
    return getattr(request.state, "trace_id", None) or str(uuid4())


def _instance(request: Request) -> str:
    # 보통 요청 경로를 instance로 많이 사용
    return str(request.url.path)


def _json(problem: ProblemDetails) -> JSONResponse:
    return JSONResponse(
        status_code=problem.status,
        content=problem.model_dump(exclude_none=True),
        media_type=PROBLEM_JSON,
    )


async def app_exception_handler(request: Request, exc: AppException):
    code = str(exc.code)
    problem = ProblemDetails(
        type=exc.type or _problem_type(code),
        title=exc.title or _title_from_code(code),
        status=exc.status_code,
        detail=exc.message,
        instance=_instance(request),
        code=code,  # extension member
        errors=exc.detail,  # extension member (optional)
        trace_id=_trace_id(request),  # extension member
    )
    return _json(problem)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(map(str, err["loc"][1:])), "message": err["msg"]}
        for err in exc.errors()
    ]
    code = str(ErrorCode.VALIDATION_ERROR)
    problem = ProblemDetails(
        type=_problem_type(code),
        title="Request Validation Failed",
        status=422,
        detail="Request validation failed",
        instance=_instance(request),
        code=code,
        errors=errors,
        trace_id=_trace_id(request),
    )
    return _json(problem)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # 프레임워크 레벨 HTTPException을 ProblemDetails로 변환
    code = str(ErrorCode.BAD_REQUEST)
    problem = ProblemDetails(
        type=_problem_type(code),
        title=_title_from_code(code),
        status=exc.status_code,
        detail=str(exc.detail),
        instance=_instance(request),
        code=code,
        trace_id=_trace_id(request),
    )
    return _json(problem)


async def unhandled_exception_handler(request: Request, exc: Exception):
    code = str(ErrorCode.INTERNAL_SERVER_ERROR)
    problem = ProblemDetails(
        type=_problem_type(code),
        title="Internal Server Error",
        status=500,
        detail="Internal server error",
        instance=_instance(request),
        code=code,
        trace_id=_trace_id(request),
    )
    return _json(problem)