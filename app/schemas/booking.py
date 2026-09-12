from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    room_id: int
    start_date: date
    end_date: date


class BookingUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None


class BookingOut(BaseModel):
    id: int
    user_id: int
    room_id: int
    start_date: date
    end_date: date
    total_price: float

    model_config = ConfigDict(from_attributes=True)