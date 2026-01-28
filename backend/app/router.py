from starlette.responses import Response

from fastapi import APIRouter
from app.features.user_profile.api import v1_user_profile_router

router = APIRouter(prefix="/api")
v1_router = APIRouter(prefix="/v1")


@router.get("/health", status_code=204)
async def health():
    return Response(status_code=204)


# Feature routers
v1_router.include_router(v1_user_profile_router)

router.include_router(v1_router)
