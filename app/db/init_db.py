from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud.user import get_user_by_email
from app.core.security import hash_password
from app.models.user import User


async def init_admin(session: AsyncSession) -> None:
    # 1. Vérifier si un user avec ADMIN_EMAIL existe déjà
    existing_admin = await get_user_by_email(session, settings.ADMIN_EMAIL)
    
    # 2. Si non, le créer avec le rôle admin
    if existing_admin is None:
        admin_user = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=hash_password(settings.ADMIN_PASSWORD),
            role="admin",  # ou ton Enum, selon comment tu l'as défini
        )
        session.add(admin_user)
        await session.commit()
        print(f"Admin créé : {settings.ADMIN_EMAIL}")
    else:
        print("Admin déjà existant, rien à faire")