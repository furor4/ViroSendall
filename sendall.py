import asyncio
import logging

from handlers.add_button import get_kb
from main.config import bot, CHAT_ID
from database.sendall_db import SessionLocal, Settings, Keyboard

logging.basicConfig(level=logging.INFO)


async def send_all():
    session = SessionLocal()
    while True:
        settings = session.query(Settings).first()
        if settings is None:
            logging.error("Settings not found in the database. Please ensure that the settings are initialized.")
            await asyncio.sleep(15)
            continue
        await asyncio.sleep(settings.per)
        if settings.send_status:
            try:
                await periodic_send()
            except Exception as e:
                logging.error(f"Error in send_all: {e}")


async def periodic_send():
    logging.info('send')
    session = SessionLocal()
    settings = session.query(Settings).first()
    if settings is None:
        logging.error("Settings not found in the database. Please ensure that the settings are initialized.")
        return
    keyboard = session.query(Keyboard).all()
    file_id = settings.file_id
    kb = get_kb(keyboard)
    if not kb:
        kb = None

    if settings.send_status:
        try:
            await bot.delete_message(chat_id=CHAT_ID, message_id=settings.last_message_id)
        except Exception as e:
            logging.error(f"Error deleting message: {e}")

        try:
            if not file_id:
                msg = await bot.send_message(chat_id=CHAT_ID, text=settings.send_all_text, reply_markup=kb,
                                             parse_mode='HTML',
                                             disable_web_page_preview=True)
            else:
                if file_id[0] == 'A':
                    msg = await bot.send_photo(chat_id=CHAT_ID, photo=file_id, caption=settings.send_all_text,
                                               reply_markup=kb, parse_mode='HTML')
                elif file_id[0] == 'B':
                    msg = await bot.send_video(chat_id=CHAT_ID, video=file_id, caption=settings.send_all_text,
                                               reply_markup=kb, parse_mode='HTML')
                elif file_id[0] == 'C':
                    msg = await bot.send_animation(chat_id=CHAT_ID, animation=file_id, caption=settings.send_all_text,
                                                   reply_markup=kb, parse_mode='HTML')

            settings.last_message_id = msg.message_id
            session.commit()
        except Exception as e:
            logging.error(f"Error sending message: {e}")
        finally:
            session.close()
