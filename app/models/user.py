#on cree les table de notre base de donnees
import enum

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Role(str, enum.Enum):
    ADMIN = "admin"
    CLIENT = "client"
    HOTEL= "hotel"
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]= mapped_column(unique=True, email=True)
    hashed_password: Mapped[str]
    role: Mapped[Role] = mapped_column(default=Role.CLIENT)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[str] = mapped_column(nullable=False)



