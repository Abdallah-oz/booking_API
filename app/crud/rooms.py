from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.room import Room
from app.schemas.rooms import RoomCreate, RoomUpdate, RoomOut


async def create_room(
    session: AsyncSession, room_data: RoomCreate, hotel_id: int
) -> Room:
  
    new_room = Room(
        **room_data.model_dump(),
        hotel_id=hotel_id,
    )

    session.add(new_room)
    await session.commit()
    await session.refresh(new_room)

    return new_room

async def get_room_by_id(session: AsyncSession, room_id: int) -> Room | None:
    result = await session.execute(select(Room).where(Room.id == room_id))
    return result.scalar_one_or_none()

async def get_rooms_by_hotel(session: AsyncSession, hotel_id: int) -> list[Room]:
    result = await session.execute(select(Room).where(Room.hotel_id == hotel_id))
    return list(result.scalars().all())

async def update_room(
    session: AsyncSession, room: Room, room_data: RoomUpdate
) -> Room:
   
    update_data = room_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(room, key, value)

    await session.commit()
    await session.refresh(room)

    return room

async def delete_room(session: AsyncSession, room: Room) -> None:
    await session.delete(room)
    await session.commit()
