from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.sendall_db import Settings, SessionLocal
from filters.isAdmin import IsAdmin

router = Router()

@router.callback_query(IsAdmin(), F.data == 'stop_send')
async def stop_send(callback: CallbackQuery):
    session = SessionLocal()
    settings = session.query(Settings).first()
    if settings:
        settings.send_status = False
        session.commit()
        await callback.message.answer('🔴 Рассылка остановлена.')
    session.close()
    await callback.answer()

@router.callback_query(IsAdmin(), F.data == 'continue_send')
async def continue_send(callback: CallbackQuery):
    session = SessionLocal()
    settings = session.query(Settings).first()
    if settings:
        settings.send_status = True
        session.commit()
        await callback.message.answer('🟢 Рассылка возобновлена.')
    session.close()
    await callback.answer()