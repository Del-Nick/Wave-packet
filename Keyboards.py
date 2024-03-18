from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
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


scientific_groups = [[{'group': 'Вычислительный эксперимент в оптике',
                       'callback': 'science_group_computational_experiment_in_optic'},

                      {'group': 'Квантовая оптика и нанофотоника',
                       'callback': 'science_group_quantum_optics_and_nanophotonics'},

                      {'group': 'Группа биомедицинской фотоники',
                       'callback': 'science_group_biomedical_photonics'},

                      {'group': 'Органическая электроника',
                       'callback': 'science_group_organic_electronic'}],

                     [{'group': 'Экспериментальная и теоретическая квантовая оптика',
                       'callback': 'science_group_experimental_and_theoretical_quantum_optic'},

                      {'group': 'Теоретические проблемы оптики',
                       'callback': 'science_group_theoretical_problems_of_optic'},

                      {'group': 'Нелинейная поляризационная оптика',
                       'callback': 'science_group_nonlinear_polarization_optic'},

                      {'group': 'Фотоника и нелинейная спектроскопия',
                       'callback': 'science_group_photonic_and_nonlinear_spectroscopy'}],

                     [{'group': 'Лазерная диагностика биомолекул'
                                'и методов фотоники в исследовании объектов культурного наследия',
                       'callback': 'science_group_laser_diagnostic_biomolecules'},

                      {'group': 'Лазерные системы и нелинейная спектроскопия',
                       'callback': 'science_group_laser_system_and_nonlinear_spectroscopy'},

                      {'group': 'Терагерцовая оптоэлектроника и спектроскопия',
                       'callback': 'science_group_THz_optoelectronics_and_spectroscopy'},

                      {'group': 'Нелинейная оптика и сверхсильные световые поля',
                       'callback': 'science_group_nonlinear_optics_and_super-strong_light_fields'}],

                     [{'group': 'Лазерная оптоакустика',
                       'callback': 'science_group_laser_optoacoustics'},

                      {'group': 'Релятивистская лазерная плазма',
                       'callback': 'science_group_relativistic_laser_plasma'},

                      {'group': 'Стохастические нелинейные процессы',
                       'callback': 'science_group_stochastic_nonlinear_processes'},

                      {'group': 'Центр измерительных технологий и промышленной автоматизации',
                       'callback': 'science_group_center_for_measuring_technologies'}]]


def science_group_keyboard(user: User):
    if user.action[-1] in ['0', '1', '2', '3']:
        page = int(user.action[-1])
    else:
        page = 0

    keyboard = InlineKeyboardBuilder()

    for group in scientific_groups[page]:
        keyboard.row(InlineKeyboardButton(
            text=group['group'],
            callback_data=f"{group['callback']}_start"))

    back_button = InlineKeyboardButton(
        text="⬇️ Меню ⬇️",
        callback_data='science_group_🔙  Назад  🔙')

    if page == 0:
        keyboard.row(back_button,
                     InlineKeyboardButton(
                         text=f"Страница 2 ➡️",
                         callback_data='science_group_page+'))
    elif page == 3:
        keyboard.row(InlineKeyboardButton(
            text=f"⬅️ Страница 3",
            callback_data='science_group_page-'),
            back_button)
    else:
        keyboard.row(InlineKeyboardButton(
            text=f"⬅️ Страница {page}",
            callback_data='science_group_page-'),
            back_button,
            InlineKeyboardButton(
                text=f"Страница {page + 2} ➡️",
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
        text="Научные напрвления",
        callback_data=user.action.replace('start', 'areas')),
        InlineKeyboardButton(
            text="Курсовые работы",
            callback_data=user.action.replace('start', 'courseworks')))
    keyboard.row(InlineKeyboardButton(
        text="Контакты",
        callback_data=user.action.replace('start', 'contacts')))

    keyboard.row(InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data=f"{'_'.join(user.action.split('_')[:-2])}_start"))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить запись обо мне",
            callback_data='delete_user'))

    return keyboard