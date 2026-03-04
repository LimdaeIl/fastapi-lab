from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=list[PostOut])
async def list_posts(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).order_by(Post.id.desc()))
    return q.scalars().all()


@router.post("", response_model=PostOut)
async def create_post(
    payload: PostCreate,
    db: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    post = Post(title=payload.title, content=payload.content, author_id=me.id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Not found")
    return post


@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: int,
    payload: PostUpdate,
    db: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Not found")
    if post.author_id != me.id:
        raise HTTPException(403, "Forbidden")

    if payload.title is not None:
        post.title = payload.title
    if payload.content is not None:
        post.content = payload.content

    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Not found")
    if post.author_id != me.id:
        raise HTTPException(403, "Forbidden")

    await db.delete(post)
    await db.commit()
    return {"ok": True}
