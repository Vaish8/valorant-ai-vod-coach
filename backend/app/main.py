from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.database import router as database_router
from app.api.routes.health import router as health_router
from app.api.routes.matches import router as matches_router
from app.core.config import settings
from app.db.init_db import init_db
from app.api.routes.events import router as events_router
from app.api.routes.rounds import router as rounds_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Backend API for the Valorant AI VOD Coach platform.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only. Restrict this later in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(database_router)
app.include_router(matches_router)
app.include_router(rounds_router)
app.include_router(events_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Valorant AI VOD Coach API",
        "status": "running",
    }