from fastapi import FastAPI
from app.api.v1.router import api_router
from app.config import settings
from app.db.session import AsyncSessionLocal
from app.db.init_db import init_admin
from app.api.v1.router import api_router
from app.config import settings

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code exécuté AU DÉMARRAGE
    async with AsyncSessionLocal() as session:
        await init_admin(session)
    yield
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")


from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import NotFoundException, PermissionDeniedException, ConflictException


@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )


@app.exception_handler(PermissionDeniedException)
async def permission_denied_handler(request: Request, exc: PermissionDeniedException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.detail},
    )


@app.exception_handler(ConflictException)
async def conflict_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.detail},
    )