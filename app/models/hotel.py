from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from models.user import User


class Hotel(Base):
    __tablename__ = "hotels"
    user=Mapped[User] = mapped_column(nullable=False)
    name=Mapped[str] = mapped_column(nullable=False)
    address=Mapped[str] = mapped_column(nullable=False)
    phone=Mapped[str] = mapped_column(nullable=False)
    photos=Mapped[str] = mapped_column(nullable=False)
    avis=Mapped[float] = mapped_column(nullable=False)
    