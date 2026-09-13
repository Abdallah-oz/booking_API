from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings


# --- Configuration du hashing ---
# CryptContext gère l'algorithme de hashing (ici bcrypt).
# "deprecated=auto" permet de migrer facilement vers un autre algo plus tard
# sans casser la compatibilité avec les anciens hash déjà en base.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Transforme un mot de passe en clair en un hash irréversible.
    Utilisé au moment du register, avant de sauvegarder en DB.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie qu'un mot de passe en clair correspond à un hash stocké.
    Utilisé au moment du login. Ne "déhash" jamais rien, il re-hash
    plain_password et compare les deux hash entre eux.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Crée un JWT signé à partir des données fournies (ex: {"sub": "1", "role": "client"}).
    Ajoute automatiquement une date d'expiration ("exp").
    """
    to_encode = data.copy()  # évite de modifier le dict original passé en argument

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Décode et vérifie un JWT reçu dans une requête.
    Vérifie la signature (avec SECRET_KEY) et l'expiration automatiquement.
    Lève une erreur HTTP 401 si le token est invalide, expiré, ou falsifié.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )