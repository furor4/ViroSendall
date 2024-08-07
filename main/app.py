import asyncio
import logging

from main.config import bot, dp

from sendall import send_all
from handlers import admin, set_text, set_file, add_button, set_per, send_status

logging.basicConfig(level=logging.INFO)

async def main():
    dp.include_routers(admin.router, set_text.router, set_file.router, add_button.router, set_per.router,
                       send_status.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        dp.start_polling(bot),
        send_all()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        print('Бот выключен')