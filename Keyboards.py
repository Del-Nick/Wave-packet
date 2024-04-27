import re

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command
from Database import User, Lab, AllLabs
from About_departments import scientific_groups


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

    return keyboard


def delete_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()
    if user.admin:
        keyboard.row(InlineKeyboardButton(
                text="Удалить меня",
                callback_data='delete_user'))

    return keyboard


def start_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()

    match user.status:
        case 'small_student':
            keyboard.row(InlineKeyboardButton(
                text="Научные группы",
                callback_data='science_group->start'))
            keyboard.row(InlineKeyboardButton(
                text="О кафедре",
                callback_data='about'))

            if user.admin:
                keyboard.row(InlineKeyboardButton(
                        text="Админ панель",
                        callback_data='admin->start'))

            return keyboard
        case _:
            return delete_keyboard(user)


def science_group_keyboard(user: User, labs: list, total_page: int):
    try:
        page = int(re.search(r'\d{1,2}', user.action).group())
    except ValueError:
        page = 0

    keyboard = InlineKeyboardBuilder()

    for group_name, collback_name in [(x[2], x[3]) for x in labs[4 * page:4 * page + 4]]:
        keyboard.row(InlineKeyboardButton(
            text=group_name,
            callback_data=f"science_group->{collback_name}->start"))

    back_button = InlineKeyboardButton(
        text="Меню",
        callback_data='science_group->back_to_start_menu')

    if total_page > 1:
        keyboard.row(InlineKeyboardButton(
            text="◀",
            callback_data='science_group->page-'),
            back_button,
            InlineKeyboardButton(
                text="▶",
                callback_data='science_group->page+')
        )

    else:
        keyboard.row(back_button)

    return keyboard


def areas_courseworks_contacts_keyboard(user: User, lab: Lab):
    keyboard = InlineKeyboardBuilder()

    _ = f'science_group->{lab.callback_name}'

    if lab.areas:
        keyboard.row(InlineKeyboardButton(text="Научные направления",
                                          callback_data=_ + '->areas->page_0'))

    if lab.courseworks and lab.contacts:
        keyboard.row(InlineKeyboardButton(text="Курсовые работы",
                                          callback_data=_ + '->courseworks->page_0'),
                     InlineKeyboardButton(text="Контакты",
                                          callback_data=_ + '->contacts')
                                          )
    elif lab.courseworks:
        keyboard.row(InlineKeyboardButton(text="Курсовые работы",
                                          callback_data=_ + '->courseworks->page_0'))
    elif lab.contacts:
        keyboard.row(InlineKeyboardButton(text="Контакты",
                                          callback_data=_ + '->contacts'))

    keyboard.row(InlineKeyboardButton(
        text="Назад",
        callback_data="science_group->start"))

    return keyboard


def slider_keyboard(user: User,
                    total_pages: int,
                    page: int,
                    lab: Lab,
                    type_keyboard: str = 'areas'):
    '''
    Клавиатура для листания научных направлений кафедры
    :param type_keyboard: Меню, которое будет листаться
    :param total_pages: Количество научных направлений кафедры
    :param page: Страница в научных направлениях кафедры
    :param user: класс пользователя из базы данных
    :return: объект клавиатуры
    '''

    # if 'courseworks' in user.action:
    #     type_keyboard = 'courseworks'

    keyboard = InlineKeyboardBuilder()

    back_button = InlineKeyboardButton(
        text="Назад",
        callback_data=f'{"->".join(user.action.split("->")[:-2])}->start')

    if total_pages > 1:
        keyboard.row(
            InlineKeyboardButton(
                text="◀",
                callback_data=f'{lab.callback_name}->{type_keyboard}->page_{page}-'),
            back_button,
            InlineKeyboardButton(
                text="▶",
                callback_data=f'{lab.callback_name}->{type_keyboard}->page_{page}+'))

    else:
        keyboard.row(back_button)

    return keyboard


def back_keyboard(user: User, button: str = None):
    """
    Клавиатура только с кнопкой назад. Меняет последнее слово в user.action на start
    :return: Объект клавиатуры
    """
    keyboard = InlineKeyboardBuilder()

    _ = user.action.split("->")
    if 'page' in user.action:
        action = '->'.join(_[:-2]) + '->start'
    else:
        action = '->'.join(_[:-1]) + '->start'

    if button is not None:
        button = InlineKeyboardButton(
            text=button,
            callback_data=button)

        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data=action),
            button)

    else:
        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data=action))

    return keyboard


def back_keyboard_without_callback(user: User, button: str = None):
    """
    Клавиатура только с кнопкой назад. Меняет последнее слово в user.action на start
    :return: Объект клавиатуры
    """

    keyboard = InlineKeyboardBuilder()

    _ = user.action.split("->")
    if 'page' in user.action:
        action = '->'.join(_[:-2]) + '->start'
    else:
        action = '->'.join(_[:-1]) + '->start'

    if button is not None:
        button = InlineKeyboardButton(
            text=button,
            callback_data=button)

        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data=action),
            button)

    else:
        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data=action))

    return keyboard
