from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def admin_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text = 'Изменить текст 💬', callback_data = 'set_text'),
        InlineKeyboardButton(text = 'Добавить фото/видео/гиф 💾', callback_data = 'set_file')
    )
    builder.row(
        InlineKeyboardButton(text = 'Установить период ⌛', callback_data = 'set_per'),
        InlineKeyboardButton(text = 'Добавить кнопку 🎛️', callback_data = 'add_button')
    )
    builder.row(
        InlineKeyboardButton(text = 'Продолжить рассылку 🟢', callback_data = 'continue_send'),
        InlineKeyboardButton(text = 'Остановить рассылку 🔴', callback_data = 'stop_send')
    )

    return builder.as_markup()

def del_file_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text = 'Удалить файл 🚫', callback_data = 'del_file')
    )

    return builder.as_markup()

def del_button_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Удалить кнопку 🚫', callback_data='delete_button')
    )

    return builder.as_markup()