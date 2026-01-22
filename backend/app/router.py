from starlette.responses import Response

from fastapi import APIRouter
from app.features.user_profile.api import v1_router as user_profile_v1_router

router = APIRouter(prefix="/api")
v1_router = APIRouter(prefix="/v1")


@router.get("/health", status_code=204)
async def health():
    return Response(status_code=204)


# Feature routers
v1_router.include_router(user_profile_v1_router)

router.include_router(v1_router)
