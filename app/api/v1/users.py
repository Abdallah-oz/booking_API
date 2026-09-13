from fastapi import APIRouter
from fastapi import Depends
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserOut



router=APIRouter()


@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user