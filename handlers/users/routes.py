from aiogram import Router
from . import start
from . import help
from . import echo
from . import quiz_handler

user_router = Router()
user_router.include_routers(
    *[
        start.router,
        help.router,
        quiz_handler.router,
        echo.router
    ]
)
