from aiogram import Router

from .register import router as test_router
from .echo import router as echo_router
from .chatmember import router as chat_router

router = Router()
router.include_router(test_router)
router.include_router(echo_router)
router.include_router(chat_router)
