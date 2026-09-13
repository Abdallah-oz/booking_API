from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import require_role
from app.crud.user import get_all_users
from app.crud.hotel import get_hotels
from app.crud.booking import get_all_bookings
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserOut
from app.schemas.hotel import HotelOut
from app.schemas.booking import BookingOut


router = APIRouter()


@router.get("/users", response_model=list[UserOut])
async def list_all_users(
    current_user: User = Depends(require_role("admin")),
    session: AsyncSession = Depends(get_session),
):
    users = await get_all_users(session)
    return users


@router.get("/hotels", response_model=list[HotelOut])
async def list_all_hotels(
    current_user: User = Depends(require_role("admin")),
    session: AsyncSession = Depends(get_session),
):
    hotels = await get_hotels(session)
    return hotels


@router.get("/bookings", response_model=list[BookingOut])
async def list_all_bookings(
    current_user: User = Depends(require_role("admin")),
    session: AsyncSession = Depends(get_session),
):
    bookings = await get_all_bookings(session)
    return bookings