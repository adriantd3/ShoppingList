from fastapi import APIRouter

from app.api.rest.v1.endpoints import auth, health, lists, security_demo, sharing

router = APIRouter()
router.include_router(health.router)
router.include_router(auth.router)
router.include_router(lists.router)
router.include_router(sharing.lists_router)
router.include_router(sharing.public_router)
router.include_router(security_demo.router)
