from fastapi import APIRouter

from app.api.rest.v1.router import router as v1_router
from app.core.config import get_settings

settings = get_settings()
router = APIRouter(prefix=settings.api_v1_prefix)
router.include_router(v1_router)
