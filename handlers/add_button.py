from aiogram import Router, F, types

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from database.sendall_db import SessionLocal, Keyboard
from filters.isAdmin import IsAdmin
from keyboards.admin_menu_kb import del_button_keyboard

router = Router()


class SetButtons(StatesGroup):
    button = State()
    delete_button = State()

def get_kb(buttons: list):
    inlkb = []
    for button in buttons:
        btn = types.InlineKeyboardButton(text=button.text, url=button.url)
        inlkb += [btn]
    if len(buttons) > 0:
        kb = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[inlkb])
        return kb
    else:
        return False


@router.callback_query(IsAdmin(), StateFilter(None), F.data == 'add_button')
async def set_buttons(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите текст и ссылку для кнопки через дефис -\n\nПример:'
                                  ' "Текст - https://www.youtube.com"', disable_web_page_preview=True)
    await callback.answer()
    await state.set_state(SetButtons.button)


@router.message(IsAdmin(), SetButtons.button)
async def add_buttons(message: Message, state: FSMContext):
    text_url_list = message.text.split('\n')
    for text_url in text_url_list:
        if '-' in text_url:
            text, url = text_url.split('-')
            text = text.strip()
            url = url.strip()
            if text and url:
                session = SessionLocal()
                new_button = Keyboard(text=text, url=url)
                session.add(new_button)
                session.commit()
                session.close()
                await message.answer(f'✅ Кнопка "{text}" успешно добавлена!', reply_markup=del_button_keyboard())
            else:
                await message.answer('⛔️ Неправильный формат. Используйте формат: "Текст - https://www.youtube.com"',
                                     disable_web_page_preview=True)
        else:
            await message.answer('⛔️ Неправильный формат. Используйте формат: "Текст - https://www.youtube.com"',
                                 disable_web_page_preview=True)

    await state.clear()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == 'delete_button')
async def del_buttons(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите текст кнопки, которую хотите удалить.')
    await callback.answer()
    await state.set_state(SetButtons.delete_button)


@router.message(IsAdmin(), SetButtons.delete_button)
async def remove_buttons(message: Message, state: FSMContext):
    button_text = message.text.strip()
    session = SessionLocal()
    try:
        button = session.query(Keyboard).filter_by(text=button_text).first()
        if button:
            session.delete(button)
            session.commit()
            await message.answer(f'✅ Кнопка "{button_text}" успешно удалена!')
        else:
            await message.answer(f'⛔️ Кнопка с текстом "{button_text}" не найдена.')
    finally:
        session.close()

    await state.clear()