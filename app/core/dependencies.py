from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.crud.user import get_user_by_id
from app.db.session import get_session
from app.models.user import User


# Indique à FastAPI/Swagger où se trouve la route de login,
# et sait extraire le token du header "Authorization: Bearer xxx"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Dependency principale de l'authentification.
    Décode le token JWT reçu, retrouve l'utilisateur correspondant en DB,
    et le retourne. Utilisable dans n'importe quelle route protégée via
    Depends(get_current_user).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # decode_access_token lève déjà une HTTPException 401 si le token
    # est invalide, expiré, ou mal signé (voir core/security.py)
    payload = decode_access_token(token)

    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception

    user = await get_user_by_id(session, user_id)
    if user is None:
        raise credentials_exception

    return user


def require_role(*allowed_roles: str):
    """
    Fabrique de dependency pour le RBAC (contrôle d'accès par rôle).
    Utilisation : Depends(require_role("admin"))
                  Depends(require_role("admin", "hotel"))
    """

    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return role_checker