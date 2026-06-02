from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.database import router as database_router
from app.api.routes.events import router as events_router
from app.api.routes.health import router as health_router
from app.api.routes.matches import router as matches_router
from app.api.routes.rounds import router as rounds_router
from app.api.routes.statistics import router as statistics_router
from app.api.routes.analysis import router as analysis_router
from app.api.routes.coach_summary import router as coach_summary_router
from app.api.routes.coach_prompt import router as coach_prompt_router
from app.api.routes.llm_coaching import router as llm_coaching_router
from app.core.config import settings
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description=(
        "Backend API for the Valorant AI VOD Coach platform. "
        "Supports match sessions, rounds, structured gameplay events, "
        "statistics calculation, rule-based tactical analysis, and persisted findings."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(database_router)
app.include_router(matches_router)
app.include_router(rounds_router)
app.include_router(events_router)
app.include_router(statistics_router)
app.include_router(analysis_router)
app.include_router(coach_summary_router)
app.include_router(coach_prompt_router)
app.include_router(llm_coaching_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Valorant AI VOD Coach API",
        "status": "running",
    }
