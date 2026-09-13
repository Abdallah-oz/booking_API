from datetime import date

from pydantic import BaseModel, ConfigDict, model_validator


class BookingCreate(BaseModel):
    room_id: int
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self) -> "BookingCreate":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class BookingUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None

    @model_validator(mode="after")
    def check_dates(self) -> "BookingUpdate":
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class BookingOut(BaseModel):
    id: int
    user_id: int
    room_id: int
    start_date: date
    end_date: date
    total_price: float

    model_config = ConfigDict(from_attributes=True)