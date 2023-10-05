from fastapi import APIRouter

from .user import router as router_user
from .auth import router as router_auth

main_router = APIRouter()

main_router.include_router(router_user, prefix='/user', tags=['user'])
main_router.include_router(router_auth, tags=['authentication'])
