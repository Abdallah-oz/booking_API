from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from models.user import User
from models.room import Room
import datetime


class Booking(Base):
    __tablename__ = "bookings"
    user: Mapped[User] = mapped_column(nullable=False)
    room: Mapped[Room] = mapped_column(nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(nullable=False)
    
    