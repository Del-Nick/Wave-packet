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

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить меня",
            callback_data='delete_user'))

    return keyboard


def delete_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()
    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="/start",
            callback_data='/start'),
            InlineKeyboardButton(
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
                keyboard.row(
                    InlineKeyboardButton(
                        text="Удалить меня",
                        callback_data='delete_user'),
                    InlineKeyboardButton(
                        text="Админ панель",
                        callback_data='admin->start')
                )

            return keyboard
        case _:
            return delete_keyboard(user)


def science_group_keyboard(user: User, labs: list):
    try:
        page = int(re.search(r'\d{1,2}', user.action).group())
    except ValueError:
        page = 0

    keyboard = InlineKeyboardBuilder()

    for group_name, collback_name in [(x[2], x[3]) for x in labs[4 * page:4 * page + 4]]:
        keyboard.row(InlineKeyboardButton(
            text=group_name,
            callback_data=f"{collback_name}->start"))

    back_button = InlineKeyboardButton(
        text="Меню",
        callback_data='science_group->back_to_start_menu')

    if page == 0:
        keyboard.row(back_button,
                     InlineKeyboardButton(
                         text="▶",
                         callback_data='science_group->page+'))
    elif page == 3:
        keyboard.row(InlineKeyboardButton(
            text="◀",
            callback_data='science_group->page-'),
            back_button)
    else:
        keyboard.row(InlineKeyboardButton(
            text="◀",
            callback_data='science_group->page-'),
            back_button,
            InlineKeyboardButton(
                text="▶",
                callback_data='science_group->page+')
        )

    # keyboard.row(InlineKeyboardButton(
    #     text="🔙  Назад  🔙",
    #     callback_data='science_group_🔙  Назад  🔙'))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить меня",
            callback_data='delete_user'))

    return keyboard


def areas_courseworks_contacts_keyboard(user: User, lab: Lab):
    keyboard = InlineKeyboardBuilder()

    buttons = ['Научные направления']

    keyboard.row(InlineKeyboardButton(
        text="Научные направления",
        callback_data=user.action.replace('start', 'areas->0')))

    keyboard.row(InlineKeyboardButton(
        text="Курсовые работы",
        callback_data=user.action.replace('start', 'courseworks_0')),
        InlineKeyboardButton(
            text="Контакты",
            callback_data=user.action.replace('start', 'contacts')))

    keyboard.row(InlineKeyboardButton(
        text="Назад",
        callback_data="science_group->start"))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить меня",
            callback_data='delete_user'))

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

    if page == 0:
        keyboard.row(back_button,
                     InlineKeyboardButton(
                         text="▶",
                         callback_data=f'{lab.callback_name}->{type_keyboard}_+'))

    elif page == total_pages - 1:
        keyboard.row(
            InlineKeyboardButton(
                text="◀",
                callback_data=f'{lab.callback_name}->{type_keyboard}_-'),
            back_button)

    else:
        keyboard.row(
            InlineKeyboardButton(
                text="◀",
                callback_data=f'{lab.callback_name}->{type_keyboard}_-'),
            back_button,
            InlineKeyboardButton(
                text="▶",
                callback_data=f'{lab.callback_name}->{type_keyboard}_+'))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить меня",
            callback_data='delete_user'))

    return keyboard


def back_keyboard(user: User, button: str = None):
    """
    Клавиатура только с кнопкой назад. Меняет последнее слово в user.action на start
    :return: Объект клавиатуры
    """
    keyboard = InlineKeyboardBuilder()

    _ = user.action.split("->")[0]
    if 'science_group' in _ or 'about' in _:
        user.action = 'start'
    else:
        user.action = f'{_}->start'

    if button is not None:
        button = InlineKeyboardButton(
            text=button,
            callback_data=button)

        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data=user.action),
            button)

    else:
        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data=user.action))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить меня",
            callback_data='delete_user'))

    return keyboard


def back_keyboard_without_callback(user: User, button: str = None):
    """
    Клавиатура только с кнопкой назад. Меняет последнее слово в user.action на start
    :return: Объект клавиатуры
    """

    keyboard = InlineKeyboardBuilder()

    _ = user.action.split("->")[0]
    if 'science_group' in _ or 'about' in _:
        _ = 'start'
    else:
        _ += '->back'

    if button is not None:
        button = InlineKeyboardButton(
            text=button,
            callback_data=button)

        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data=_),
            button)

    else:
        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data=_))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить меня",
            callback_data='delete_user'))

    return keyboard


def admin_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text="Добавить группу",
            callback_data=f'admin->add_science_group->start'),
        InlineKeyboardButton(
            text="Удалить группу",
            callback_data='admin->delete_science_group->start'))

    keyboard.row(
        InlineKeyboardButton(
            text="Редактировать группу",
            callback_data=f'admin->edit_science_group->start'))

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


def fields_to_edit():
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(text="Полное название", callback_data='full_name'),
        InlineKeyboardButton(text="Краткое название", callback_data='short_name'))

    keyboard.row(
        InlineKeyboardButton(text="Callback", callback_data='callback_name'),
        InlineKeyboardButton(text="Описание", callback_data='about'))

    keyboard.row(
        InlineKeyboardButton(text="Основная картинка", callback_data='main_picture'),
        InlineKeyboardButton(text="Научные направления", callback_data='areas'))

    keyboard.row(
        InlineKeyboardButton(text="Контакты", callback_data='contacts'),
        InlineKeyboardButton(text="Курсовые работы", callback_data='courseworks'))

    keyboard.row(
        InlineKeyboardButton(text="⚠Удалить группу⚠", callback_data='delete_science_group'),
        InlineKeyboardButton(text="Назад", callback_data='admin->back'))

    return keyboard
