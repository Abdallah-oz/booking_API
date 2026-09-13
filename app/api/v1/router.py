from fastapi import APIRouter
from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import hotels
from app.api.v1 import room

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(hotels.router, prefix="/hotels", tags=["hotels"])
api_router.include_router(room.router, prefix="/rooms", tags=["rooms"])
