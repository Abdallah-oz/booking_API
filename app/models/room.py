from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from models.hotel import Hotel

import enum

class RoomType(str, enum.Enum):
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"

class Room(Base):
    __tablename__ = "rooms"
    hotel=Mapped[Hotel] = mapped_column(nullable=False)
    type=Mapped[RoomType] = mapped_column(nullable=False)
    price=Mapped[float] = mapped_column(nullable=False)
    is_available=Mapped[bool] = mapped_column(default=True)
    