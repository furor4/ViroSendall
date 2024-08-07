from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from database.sendall_db import SessionLocal, Settings
from filters.isAdmin import IsAdmin
import logging

router = Router()

class SetText(StatesGroup):
    writing_text = State()

@router.callback_query(IsAdmin(), StateFilter(None), F.data == 'set_text')
async def set_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите текст рассылки')
    await callback.answer()
    await state.set_state(SetText.writing_text)

@router.message(IsAdmin(), SetText.writing_text)
async def write_text(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text)
    user_data = await state.get_data()
    await message.answer(f'✅ Текст рассылки успешно установлен!\n\n{user_data["text"]}',
                         parse_mode='HTML', disable_web_page_preview=True)

    session = SessionLocal()
    try:
        settings = session.query(Settings).first()
        if settings:
            settings.send_all_text = user_data["text"]
        else:
            settings = Settings(send_all_text=user_data["text"])
            session.add(settings)
        session.commit()
        logging.info("Text successfully saved to the database")
    except Exception as e:
        session.rollback()
        logging.error(f"Error saving text to the database: {e}")
    finally:
        session.close()

    await state.clear()