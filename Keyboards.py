from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from Database import User
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


def start_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()

    match user.status:
        case 'small_student':
            keyboard.row(InlineKeyboardButton(
                text="Научные группы",
                callback_data='science_group_start'))
            keyboard.row(InlineKeyboardButton(
                text="О кафедре",
                callback_data='about'))
            keyboard.row(InlineKeyboardButton(
                text="Удалить запись обо мне",
                callback_data='delete_user'))

            return keyboard
        case _:
            return delete_keyboard(user)


def science_group_keyboard(user: User):
    if user.action[-1] in ['0', '1', '2', '3']:
        page = int(user.action[-1])
    else:
        page = 0

    keyboard = InlineKeyboardBuilder()

    for group in scientific_groups[4 * page:4 * page + 4]:
        keyboard.row(InlineKeyboardButton(
            text=group['group'],
            callback_data=f"{group['callback']}_start"))

    back_button = InlineKeyboardButton(
        text="Меню",
        callback_data='science_group_back_to_start_menu')

    if page == 0:
        keyboard.row(back_button,
                     InlineKeyboardButton(
                         text=" ➡️",
                         callback_data='science_group_page+'))
    elif page == 3:
        keyboard.row(InlineKeyboardButton(
            text="⬅️ ",
            callback_data='science_group_page-'),
            back_button)
    else:
        keyboard.row(InlineKeyboardButton(
            text="⬅️ ",
            callback_data='science_group_page-'),
            back_button,
            InlineKeyboardButton(
                text=" ➡️",
                callback_data='science_group_page+')
        )

    # keyboard.row(InlineKeyboardButton(
    #     text="🔙  Назад  🔙",
    #     callback_data='science_group_🔙  Назад  🔙'))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить запись обо мне",
            callback_data='delete_user'))

    return keyboard


def areas_courseworks_contacts_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(
        text="Научные направления",
        callback_data=user.action.replace('start', 'areas_0')))
    keyboard.row(InlineKeyboardButton(
        text="Курсовые работы",
        callback_data=user.action.replace('start', 'courseworks_0')),
        InlineKeyboardButton(
            text="Контакты",
            callback_data=user.action.replace('start', 'contacts')))

    keyboard.row(InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="science_group_start"))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить запись обо мне",
            callback_data='delete_user'))

    return keyboard


def slider_keyboard(user: User,
                    total_pages: int,
                    page: int,
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
        callback_data=f'{"_".join(user.action.split("_")[:-2])}_start')

    main_part_callback = user.action.split("_")
    main_part_callback = "_".join(main_part_callback[:-2])

    if page == 0:
        keyboard.row(back_button,
                     InlineKeyboardButton(
                         text="➡",
                         callback_data=f'{main_part_callback}_{type_keyboard}_+'))

    elif page == total_pages - 1:
        keyboard.row(
            InlineKeyboardButton(
                text="⬅",
                callback_data=f'{main_part_callback}_{type_keyboard}_-'),
            back_button)

    else:
        keyboard.row(
            InlineKeyboardButton(
                text="⬅",
                callback_data=f'{main_part_callback}_{type_keyboard}_-'),
            back_button,
            InlineKeyboardButton(
                text="➡",
                callback_data=f'{main_part_callback}_{type_keyboard}_+'))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить запись обо мне",
            callback_data='delete_user'))

    return keyboard


def back_keyboard(user: User):
    """
    Клавиатура только с кнопкой назад. Меняет последнее слово в user.action на start
    :return: Объект клавиатуры
    """
    keyboard = InlineKeyboardBuilder()

    _ = user.action.split('_')
    _[-1] = 'start'

    keyboard.row(InlineKeyboardButton(
        text="⬅ Назад",
        callback_data='_'.join(_)))
    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить запись обо мне",
            callback_data='delete_user'))

    return keyboard
