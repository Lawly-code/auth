from fastapi import APIRouter

from modules import auth, documents, subscribes, users


router = APIRouter()

router.include_router(auth.router)
router.include_router(documents.router)
router.include_router(subscribes.router)
router.include_router(users.router)

