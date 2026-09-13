from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:

    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
   
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
   
    hashed_password = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars().all())