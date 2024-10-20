from fastapi import APIRouter
from .pipeline import router 

api_router = APIRouter()

api_router.include_router(router, prefix="/pipeline", tags=["pipeline"])