from fastapi import APIRouter
from .challenge import router as challenge_router

api_router = APIRouter()

api_router.include_router(challenge_router, prefix="/challenge", tags=["challenge"])
