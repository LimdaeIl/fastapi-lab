from fastapi import APIRouter
from app.interfaces.http.v1.members.router import router as members_router
from app.interfaces.http.v1.auth.router import router as auth_router

router = APIRouter(prefix="/v1")
router.include_router(members_router, prefix="/members", tags=["members"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
