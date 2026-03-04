from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_redis() -> redis.Redis:
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])

        if payload.get("tpye") != "access":
            raise HTTPException(401, "Invalid token type")

        sub = payload.get("sub")

        if not sub:
            raise HTTPException(401, "Invalid token subject")

    except JWTError:
        raise HTTPException(401, "Invalid token")

    q = await db.execute(select(User).where(User.email == sub))
    user = q.scalar_one_or_none()

    if not user:
        raise HTTPException(401, "User not found")
    return user
