from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.sqlalchemy_member_repository import SqlAlchemyMemberRepository

from app.application.auth.login_usecase import LoginUseCase
from app.application.auth.refresh_usecase import RefreshUseCase
from app.application.auth.logout_usecase import LogoutUseCase

from app.interfaces.http.v1.auth.schemas import (
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    LogoutRequest,
)

from app.common.responses.success_response import SuccessResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    repo = SqlAlchemyMemberRepository(db)
    usecase = LoginUseCase(repo)

    access, refresh = usecase.execute(payload.email, payload.password)

    return SuccessResponse(
        data=TokenResponse(
            access_token=access,
            refresh_token=refresh,
        )
    )


@router.post(
    "/refresh",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    repo = SqlAlchemyMemberRepository(db)
    usecase = RefreshUseCase(repo)

    access, refresh_token = usecase.execute(payload.refresh_token)

    return SuccessResponse(
        data=TokenResponse(
            access_token=access,
            refresh_token=refresh_token,
        )
    )


@router.post(
    "/logout",
    response_model=SuccessResponse[dict],
    status_code=status.HTTP_200_OK,
)
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    repo = SqlAlchemyMemberRepository(db)
    usecase = LogoutUseCase(repo)

    usecase.execute(payload.refresh_token)

    return SuccessResponse(data={"ok": True})