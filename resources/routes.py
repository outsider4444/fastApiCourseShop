from fastapi import APIRouter
from . import auth, complaint, users

# объединение endpoints

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(complaint.router)
api_router.include_router(users.router)
