from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.user import User


def utc_now():
    return datetime.now(timezone.utc)

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="posts")

    @property
    def author(self) -> User:
        return self.user
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True),
      default=utc_now,
      nullable=False,
)
    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
      default=utc_now,
      onupdate=utc_now,
      nullable=False,
)