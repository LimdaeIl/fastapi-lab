from fastapi import APIRouter, Depends, status
from app.domain.members.repositories.member_repository import MemberRepository
from app.interfaces.http.dependencies.repositories import get_member_repo

from app.application.auth.login_usecase import LoginUseCase
from app.application.auth.refresh_usecase import RefreshUseCase
from app.application.auth.logout_usecase import LogoutUseCase
from app.application.auth.signup_usecase import SignupUseCase

from app.interfaces.http.v1.auth.schemas import (
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    LogoutRequest,
    SignupRequest,
    SignupResponse,
)
from app.common.responses.success_response import SuccessResponse

router = APIRouter()


@router.post("/signup", response_model=SuccessResponse[SignupResponse], status_code=201)
def signup(payload: SignupRequest, repo: MemberRepository = Depends(get_member_repo)):
    member = SignupUseCase(repo).execute(payload.email, payload.password)
    return SuccessResponse(data=SignupResponse(id=member.id, email=member.email))


@router.post(
    "/login",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
)
def login(payload: LoginRequest, repo: MemberRepository = Depends(get_member_repo)):
    access, refresh = LoginUseCase(repo).execute(payload.email, payload.password)
    return SuccessResponse(
        data=TokenResponse(access_token=access, refresh_token=refresh)
    )


@router.post(
    "/refresh",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
)
def refresh(payload: RefreshRequest, repo: MemberRepository = Depends(get_member_repo)):
    access, refresh_token = RefreshUseCase(repo).execute(payload.refresh_token)
    return SuccessResponse(
        data=TokenResponse(access_token=access, refresh_token=refresh_token)
    )


@router.post(
    "/logout", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK
)
def logout(payload: LogoutRequest, repo: MemberRepository = Depends(get_member_repo)):
    LogoutUseCase(repo).execute(payload.refresh_token)
    return SuccessResponse(data={"ok": True})
