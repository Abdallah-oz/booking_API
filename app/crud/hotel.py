from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import Hotel
from app.schemas.hotel import HotelCreate, HotelUpdate


async def create_hotel(
    session: AsyncSession, hotel_data: HotelCreate, owner_id: int
) -> Hotel:
  
    new_hotel = Hotel(
        **hotel_data.model_dump(),
        user_id=owner_id,
    )

    session.add(new_hotel)
    await session.commit()
    await session.refresh(new_hotel)

    return new_hotel


async def get_hotel_by_id(session: AsyncSession, hotel_id: int) -> Hotel | None:

    result = await session.execute(select(Hotel).where(Hotel.id == hotel_id))
    return result.scalar_one_or_none()


async def get_hotels(session: AsyncSession) -> list[Hotel]:
    """
    Retourne tous les hôtels.
    """
    result = await session.execute(select(Hotel))
    return list(result.scalars().all())


async def update_hotel(
    session: AsyncSession, hotel: Hotel, hotel_data: HotelUpdate
) -> Hotel:
   
    update_data = hotel_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(hotel, key, value)

    await session.commit()
    await session.refresh(hotel)

    return hotel


async def delete_hotel(session: AsyncSession, hotel: Hotel) -> None:
   
    await session.delete(hotel)
    await session.commit()