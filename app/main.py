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