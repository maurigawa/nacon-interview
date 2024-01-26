from fastapi import APIRouter

from .v0.asset import router as asset_router

v0_router = APIRouter(prefix="/v0", tags=["v0"])

v0_router.include_router(asset_router)
