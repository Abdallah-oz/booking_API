from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, require_role
from app.crud.hotel import (
    create_hotel,
    get_hotel_by_id,
    get_hotels,
    update_hotel,
    delete_hotel,
)
from app.db.session import get_session
from app.models.user import User
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelOut


router = APIRouter()


@router.post("/", response_model=HotelOut, status_code=status.HTTP_201_CREATED)
async def create_new_hotel(
    hotel_data: HotelCreate,
    current_user: User = Depends(require_role("hotel", "admin")),
    session: AsyncSession = Depends(get_session),
):
    new_hotel = await create_hotel(session, hotel_data, owner_id=current_user.id)
    return new_hotel


@router.get("/", response_model=list[HotelOut])
async def list_hotels(
    session: AsyncSession = Depends(get_session),
):
    hotels = await get_hotels(session)
    return hotels


@router.get("/{hotel_id}", response_model=HotelOut)
async def get_hotel(
    hotel_id: int,
    session: AsyncSession = Depends(get_session),
):
    hotel = await get_hotel_by_id(session, hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found",
        )
    return hotel


@router.patch("/{hotel_id}", response_model=HotelOut)
async def update_existing_hotel(
    hotel_id: int,
    hotel_data: HotelUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    hotel = await get_hotel_by_id(session, hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found",
        )

    if current_user.role != "admin" and hotel.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this hotel",
        )

    updated_hotel = await update_hotel(session, hotel, hotel_data)
    return updated_hotel


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_hotel(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    hotel = await get_hotel_by_id(session, hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found",
        )

    if current_user.role != "admin" and hotel.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this hotel",
        )

    await delete_hotel(session, hotel)
    return None