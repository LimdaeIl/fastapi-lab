from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
  __tablename__ = "users"

  id = Mapped[int] = mapped_column(Integer, primary_key=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
  password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

  posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")