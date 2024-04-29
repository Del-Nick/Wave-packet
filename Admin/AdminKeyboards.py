import re
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command
from Database import User, Lab, AllLabs
from About_departments import scientific_groups


def admin_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text="Добавить группу",
            callback_data=f'admin->add_science_group->start'),
        InlineKeyboardButton(
            text="Изменить группу",
            callback_data=f'admin->edit_science_group->start'))

    keyboard.row(
        InlineKeyboardButton(
            text="Как оформлять текст?",
            callback_data=f'admin->about_text_editing')
    )

    keyboard.row(
        InlineKeyboardButton(
            text="Просто крутая кнопка",
            callback_data=f'admin->joke'))

    keyboard.row(
        InlineKeyboardButton(
            text="В главное меню",
            callback_data='start'))

    keyboard.row(InlineKeyboardButton(
        text="Удалить меня",
        callback_data='delete_user'))

    return keyboard


def back_keyboard(user: User, callback: bool = True, button: str | list = None, field: str = ''):
    """
    Клавиатура только с кнопкой назад. Меняет последнее слово в user.action на start
    :return: Объект клавиатуры
    """

    keyboard = InlineKeyboardBuilder()

    if button is not None:
        if type(button) is list:
            keyboard.row(InlineKeyboardButton(
                text=button[0],
                callback_data=button[0]),
                InlineKeyboardButton(
                    text=button[1],
                    callback_data=button[1]))

            keyboard.row(InlineKeyboardButton(
                text="Назад",
                callback_data='back'))

        else:
            button = InlineKeyboardButton(
                text=button,
                callback_data=f'{field}{button}')

            keyboard.row(InlineKeyboardButton(
                text="Назад",
                callback_data='back'),
                button)

    else:
        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data='back'))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить меня",
            callback_data='delete_user'))

    return keyboard


def custom_keyboard(user: User, buttons: list | range, field: str = '', special_button: str = None):
    keyboard = InlineKeyboardBuilder()

    for i, button in enumerate(buttons):
        keyboard.button(text=str(button),
                        callback_data=f'{field}{button}')

    if special_button:
        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data='back'),
            InlineKeyboardButton(
                text=special_button,
                callback_data=f'{field}{special_button}'))
    else:
        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data='back'))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить меня",
            callback_data='delete_user'))

    return keyboard


def fields_to_edit():
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(text="Полное название", callback_data='full_name'),
        InlineKeyboardButton(text="Краткое название", callback_data='short_name'))

    keyboard.row(
        InlineKeyboardButton(text="Контакты", callback_data='contacts'),
        InlineKeyboardButton(text="Описание", callback_data='lab_about'))

    keyboard.row(
        InlineKeyboardButton(text="Основная картинка", callback_data='main_picture'),
        InlineKeyboardButton(text="Научные направления", callback_data='areas'))

    keyboard.row(
        InlineKeyboardButton(text="⚠Удалить группу⚠", callback_data='delete_science_group'),
        InlineKeyboardButton(text="Курсовые работы", callback_data='courseworks'))

    keyboard.row(InlineKeyboardButton(text="Назад", callback_data='back'))

    return keyboard
