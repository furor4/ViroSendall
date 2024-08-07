from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from database.sendall_db import SessionLocal, Settings
from filters.isAdmin import IsAdmin

router = Router()


class SetPer(StatesGroup):
    setting_per = State()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == 'set_per')
async def set_per(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Установите периодичность отправления рассылки. Пример: 60s, 2m, 6h.\n\n'
                                  'Минимальная периодичность: 60 секунд')
    await callback.answer()
    await state.set_state(SetPer.setting_per)


@router.message(IsAdmin(), SetPer.setting_per)
async def process_per(message: Message, state: FSMContext):
    session = SessionLocal()
    user_input = message.text
    try:
        unit = user_input[-1]
        value = int(user_input[:-1])

        if unit == 's':
            period = value
        elif unit == 'm':
            period = value * 60
        elif unit == 'h':
            period = value * 3600
        else:
            raise ValueError('Неверный формат')

        if period < 60 or period > 86400:  # Минимум - 60 секунд, максимум - 1 день
            raise ValueError('Период должен быть от 60 секунд до 24 часов')

        setting = session.query(Settings).first()
        if not setting:
            setting = Settings(per=period)
            session.add(setting)
        else:
            setting.per = period
        session.commit()

        await message.answer(f'Периодичность отправки рассылки установлена на {period} секунд')
        await state.clear()

    except ValueError as e:
        await message.answer(str(e))
        return
