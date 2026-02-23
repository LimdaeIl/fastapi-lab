from fastapi import APIRouter, Depends


from app.interfaces.http.dependencies.auth import get_current_member
from app.interfaces.http.dependencies.permissions import require_roles

from app.interfaces.http.v1.members.schemas import (
    MeResponse,
    AdminOnlyResponse,
)

from app.common.responses.success_response import SuccessResponse

router = APIRouter()


@router.get("/ping", response_model=SuccessResponse[dict])
def ping():
    return SuccessResponse(data={"ok": True, "domain": "members"})


@router.get(
    "/me",
    response_model=SuccessResponse[MeResponse],
)
def me(current_member=Depends(get_current_member)):
    return SuccessResponse(
        data=MeResponse(
            id=current_member.id,
            email=current_member.email,
            role=current_member.role,
        )
    )


@router.get(
    "/admin-only",
    response_model=SuccessResponse[AdminOnlyResponse],
)
def admin_only(current_member=Depends(require_roles("admin"))):
    return SuccessResponse(
        data=AdminOnlyResponse(
            ok=True,
            admin=current_member.email,
        )
    )
