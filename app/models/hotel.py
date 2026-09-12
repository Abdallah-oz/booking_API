"""SQLAlchemy model for hotels."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.room import Room
    from app.models.user import User


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(30))
    photos: Mapped[str] = mapped_column(String(1000))
    avis: Mapped[float] = mapped_column()

    user: Mapped["User"] = relationship()
