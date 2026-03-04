from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.api.auth import router as auth_router
from app.api.posts import router as posts_router

app = FastAPI(title="FastAPI Lab")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router)
app.include_router(posts_router)


@app.get("/", summary="간단한 API", tags=["Simple"])
async def root():
    return {"message": "Hello World"}
