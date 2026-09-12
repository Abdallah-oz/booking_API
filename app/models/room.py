"""SQLAlchemy model for hotel rooms."""

import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.hotel import Hotel


class RoomType(str, enum.Enum):
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    type: Mapped[RoomType] = mapped_column(SqlEnum(RoomType, name="room_type"))
    price: Mapped[float] = mapped_column()
    is_available: Mapped[bool] = mapped_column(default=True)

    hotel: Mapped["Hotel"] = relationship()
