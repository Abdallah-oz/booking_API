from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.rooms import RoomCreate, RoomUpdate, RoomOut
from app.crud.rooms import (
    create_room,
    get_room_by_id,
    get_rooms_by_hotel,
    update_room,
    delete_room,
)
from app.crud.hotel import get_hotel_by_id


router = APIRouter()


def check_hotel_ownership_or_admin(hotel, current_user: User):
    if current_user.role != "admin" and hotel.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this hotel",
        )


@router.post("/hotels/{hotel_id}/rooms", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
async def create_new_room(
    hotel_id: int,
    room_data: RoomCreate,
    current_user: User = Depends(require_role("hotel", "admin")),
    session: AsyncSession = Depends(get_session),
):
    hotel = await get_hotel_by_id(session, hotel_id)
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")

    check_hotel_ownership_or_admin(hotel, current_user)

    new_room = await create_room(session, room_data, hotel_id=hotel_id)
    return new_room


@router.get("/hotels/{hotel_id}/rooms", response_model=list[RoomOut])
async def list_rooms_by_hotel(
    hotel_id: int,
    session: AsyncSession = Depends(get_session),
):
    hotel = await get_hotel_by_id(session, hotel_id)
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")

    rooms = await get_rooms_by_hotel(session, hotel_id)
    return rooms


@router.get("/hotels/{hotel_id}/rooms/{room_id}", response_model=RoomOut)
async def get_room(
    hotel_id: int,
    room_id: int,
    session: AsyncSession = Depends(get_session),
):
    room = await get_room_by_id(session, room_id)
    if room is None or room.hotel_id != hotel_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room


@router.patch("/hotels/{hotel_id}/rooms/{room_id}", response_model=RoomOut)
async def update_existing_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    room = await get_room_by_id(session, room_id)
    if room is None or room.hotel_id != hotel_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    hotel = await get_hotel_by_id(session, hotel_id)
    check_hotel_ownership_or_admin(hotel, current_user)

    updated_room = await update_room(session, room, room_data)
    return updated_room


@router.delete("/hotels/{hotel_id}/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_room(
    hotel_id: int,
    room_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    room = await get_room_by_id(session, room_id)
    if room is None or room.hotel_id != hotel_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    hotel = await get_hotel_by_id(session, hotel_id)
    check_hotel_ownership_or_admin(hotel, current_user)

    await delete_room(session, room)