from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters.isAdmin import IsAdmin

from keyboards.admin_menu_kb import admin_menu_keyboard

router = Router()

@router.message(IsAdmin(), Command('admin'))
async def admin_menu(message: Message):
    await message.answer('👮🏻 Админ меню', reply_markup=admin_menu_keyboard())