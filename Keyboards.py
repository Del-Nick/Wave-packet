from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from Database import User


def registration_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(
                    text="Студент 1-2 курсов",
                    callback_data='registration_small_student'),
                 InlineKeyboardButton(
                    text="Студент кафедры",
                    callback_data='registration_student'))
    keyboard.row(InlineKeyboardButton(
        text="Сотрудник кафедры",
        callback_data='registration_employee'))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить запись обо мне",
            callback_data='delete_user'))

    return keyboard


def delete_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()
    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить запись обо мне",
            callback_data='delete_user'))

    return keyboard