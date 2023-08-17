from fastapi import APIRouter

from .user import router as router_user

main_router = APIRouter()

main_router.include_router(router_user, prefix='/user', tags=['user'])
