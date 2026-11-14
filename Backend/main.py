from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.dependencies import get_current_user
from app.database import supabase
from app.routes.briefings import router as briefings_router
from app.routes.episodes import router as episodes_router
from app.services.scheduler import (
    start_scheduler,
    stop_scheduler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    start_scheduler()

    yield

    stop_scheduler()


app = FastAPI(
    title="Scheduled Research-to-Podcast Agent",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://daily-news-1-xute.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(briefings_router)
app.include_router(episodes_router)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Scheduled Podcast Agent API",
    }


@app.get("/test-db")
def test_database():

    response = (
        supabase
        .table("briefings")
        .select("id")
        .limit(1)
        .execute()
    )

    return {
        "status": "ok",
        "database": "connected",
        "data": response.data,
    }


@app.get("/test-auth")
async def test_auth(
    user=Depends(get_current_user),
):
    return {
        "status": "ok",
        "user": user,
    }