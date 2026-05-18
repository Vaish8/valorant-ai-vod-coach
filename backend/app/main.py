from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.database import router as database_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Backend API for the Valorant AI VOD Coach platform.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. Restrict this later in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(database_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Valorant AI VOD Coach API",
        "status": "running",
    }
