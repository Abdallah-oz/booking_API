from enum import Enum

from pydantic import BaseModel, ConfigDict


class RoomType(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"


class RoomCreate(BaseModel):
    type: RoomType
    price: float
    is_available: bool = True


class RoomUpdate(BaseModel):
    type: RoomType | None = None
    price: float | None = None
    is_available: bool | None = None


class RoomOut(BaseModel):
    id: int
    hotel_id: int
    type: RoomType
    price: float
    is_available: bool

    model_config = ConfigDict(from_attributes=True)