from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, require_role
from app.crud.booking import (
    create_booking,
    get_booking_by_id,
    get_bookings_by_user,
    update_booking,
    delete_booking,
)
from app.crud.rooms import get_room_by_id
from app.crud.hotel import get_hotel_by_id
from app.db.session import get_session
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingUpdate, BookingOut
from app.services.booking_service import check_room_availability, calculate_total_price


router = APIRouter()


@router.post("/", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_new_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(require_role("client")),
    session: AsyncSession = Depends(get_session),
):
    room = await get_room_by_id(session, booking_data.room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    is_available = await check_room_availability(
        session,
        room_id=booking_data.room_id,
        start_date=booking_data.start_date,
        end_date=booking_data.end_date,
    )
    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is not available for these dates",
        )

    total_price = calculate_total_price(room, booking_data.start_date, booking_data.end_date)

    new_booking = await create_booking(
        session,
        user_id=current_user.id,
        room_id=booking_data.room_id,
        start_date=booking_data.start_date,
        end_date=booking_data.end_date,
        total_price=total_price,
    )
    return new_booking


@router.get("/me", response_model=list[BookingOut])
async def list_my_bookings(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    bookings = await get_bookings_by_user(session, current_user.id)
    return bookings


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    booking = await get_booking_by_id(session, booking_id)
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if current_user.role != "admin" and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this booking",
        )

    return booking


@router.patch("/{booking_id}", response_model=BookingOut)
async def update_existing_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    booking = await get_booking_by_id(session, booking_id)
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if current_user.role != "admin" and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this booking",
        )

    new_start = booking_data.start_date or booking.start_date
    new_end = booking_data.end_date or booking.end_date

    new_total_price = None
    if booking_data.start_date or booking_data.end_date:
        is_available = await check_room_availability(
            session,
            room_id=booking.room_id,
            start_date=new_start,
            end_date=new_end,
            exclude_booking_id=booking.id,
        )
        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is not available for these dates",
            )

        room = await get_room_by_id(session, booking.room_id)
        new_total_price = calculate_total_price(room, new_start, new_end)

    updated_booking = await update_booking(session, booking, booking_data, new_total_price)
    return updated_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    booking = await get_booking_by_id(session, booking_id)
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if current_user.role != "admin" and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this booking",
        )

    await delete_booking(session, booking)