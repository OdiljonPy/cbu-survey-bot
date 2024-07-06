import logging
from aiogram import Bot


async def on_startup_notify(bot: Bot):
    from data.config import ADMINS
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.error(msg=f"{err} id: {admin}")
