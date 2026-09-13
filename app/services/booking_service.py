from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.room import Room


async def check_room_availability(
    session: AsyncSession,
    room_id: int,
    start_date: date,
    end_date: date,
    exclude_booking_id: int | None = None,
) -> bool:
    """
    Vérifie qu'aucune réservation existante sur cette room ne chevauche
    la période demandée. Retourne True si disponible.
    exclude_booking_id sert pour un update (ignorer la réservation qu'on modifie elle-même).
    """
    query = select(Booking).where(
        Booking.room_id == room_id,
        Booking.start_date < end_date,
        Booking.end_date > start_date,
    )
    if exclude_booking_id is not None:
        query = query.where(Booking.id != exclude_booking_id)

    result = await session.execute(query)
    conflicting_bookings = result.scalars().all()

    return len(conflicting_bookings) == 0


def calculate_total_price(room: Room, start_date: date, end_date: date) -> float:
    """
    Calcule le prix total en fonction du nombre de nuits et du prix/nuit de la room.
    """
    nights = (end_date - start_date).days
    return room.price * nights