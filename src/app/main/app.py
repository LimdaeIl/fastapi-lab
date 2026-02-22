from fastapi import FastAPI
from app.common.config.settings import settings
from app.interfaces.http.v1.router import router as v1_router
from app.infrastructure.db.session import engine
from app.infrastructure.db.models.base import Base
from app.infrastructure.db.models.member_model import MemberModel  # noqa: F401

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.common.errors.app_exception import AppException
from app.main.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.app_debug)
    app.include_router(v1_router, prefix="/api")

    @app.on_event("startup")
    def on_startup():
        # 초기 개발 편의용(임시). Alembic 도입 시 제거
        Base.metadata.create_all(bind=engine)

    return app

app = create_app()

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)