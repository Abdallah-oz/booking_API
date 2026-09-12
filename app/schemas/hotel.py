from pydantic import BaseModel, ConfigDict


class HotelBase(BaseModel):
    name: str
    address: str
    city: str
    country: str
    description: str | None = None


class HotelCreate(HotelBase):
    pass  


class HotelUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    description: str | None = None


class HotelOut(HotelBase):
    id: int
    user_id: int
    rating: float | None = None

    model_config = ConfigDict(from_attributes=True)