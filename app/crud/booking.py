from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.schemas.booking import BookingUpdate


async def create_booking(
    session: AsyncSession,
    user_id: int,
    room_id: int,
    start_date,
    end_date,
    total_price: float,
) -> Booking:
    """
    Crée une réservation en base.
    Ne reçoit PAS de BookingCreate directement : user_id vient du token,
    total_price est calculé par services/booking_service.py AVANT d'appeler
    cette fonction. Cette fonction ne fait que l'insertion en DB.
    """
    new_booking = Booking(
        user_id=user_id,
        room_id=room_id,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
    )

    session.add(new_booking)
    await session.commit()
    await session.refresh(new_booking)

    return new_booking


async def get_booking_by_id(session: AsyncSession, booking_id: int) -> Booking | None:
    result = await session.execute(select(Booking).where(Booking.id == booking_id))
    return result.scalar_one_or_none()


async def get_bookings_by_user(session: AsyncSession, user_id: int) -> list[Booking]:
    result = await session.execute(select(Booking).where(Booking.user_id == user_id))
    return list(result.scalars().all())


async def get_bookings_by_room(session: AsyncSession, room_id: int) -> list[Booking]:
    result = await session.execute(select(Booking).where(Booking.room_id == room_id))
    return list(result.scalars().all())


async def update_booking(
    session: AsyncSession,
    booking: Booking,
    booking_data: BookingUpdate,
    new_total_price: float | None = None,
) -> Booking:
    """
    Met à jour une réservation existante.
    new_total_price est recalculé par services/booking_service.py si les
    dates changent (car un changement de dates change le prix total).
    """
    update_data = booking_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(booking, key, value)

    if new_total_price is not None:
        booking.total_price = new_total_price

    await session.commit()
    await session.refresh(booking)

    return booking


async def delete_booking(session: AsyncSession, booking: Booking) -> None:
    await session.delete(booking)
    await session.commit()
    
    
async def get_all_bookings(session: AsyncSession) -> list[Booking]:
    result = await session.execute(select(Booking))
    return list(result.scalars().all())