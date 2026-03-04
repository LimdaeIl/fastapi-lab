from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import SignupIn, LoginIn, TokenOut
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.api.deps import get_redis

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(payload: SignupIn, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(select(User).where(User.email == payload.email))
    if exists.scalar_one_or_none():
        raise HTTPException(409, "Email already exists")

    user = User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    await db.commit()
    return {"ok": True}


@router.post("/login", response_model=TokenOut)
async def login(
    payload: LoginIn,
    db: AsyncSession = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
):
    q = await db.execute(select(User).where(User.email == payload.email))
    user = q.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Bad credentials")

    access = create_access_token(user.email)
    refresh = create_refresh_token(user.email)

    # refresh를 Redis에 저장 (로그아웃/세션 무효화 용도)
    await r.set(f"refresh:{user.email}", refresh)
    return TokenOut(access_token=access, refresh_token=refresh)


@router.post("/logout")
async def logout(email: str, r: redis.Redis = Depends(get_redis)):
    # 데모 단순화를 위해 email을 받지만, 실전에서는 access token에서 추출 권장
    await r.delete(f"refresh:{email}")
    return {"ok": True}
