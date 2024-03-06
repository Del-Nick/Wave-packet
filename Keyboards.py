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


scientific_groups = [{'group': 'Группа вычислительного эксперимента в оптике',
                      'callback': 'science_group_computational_experiment_in_optic'},

                     {'group': 'Группа квантовой оптики и нанофотоники',
                      'callback': 'science_group_quantum_optics_and_nanophotonics'},

                     {'group': 'Группа биомедицинской фотоники',
                      'callback': 'science_group_biomedical_photonics'},

                     {'group': 'Группа органической электроники',
                      'callback': 'science_group_organic_electronic'},

                     {'group': 'Группа экспериментальной и теоретической квантовой оптики',
                      'callback': 'science_group_experimental_and_theoretical_quantum_optic'},

                     {'group': 'Группа теоретических проблем оптики',
                      'callback': 'science_group_theoretical_problems_of_optic'},

                     {'group': 'Группа нелинейной поляризационной оптики',
                      'callback': 'science_group_nonlinear_polarization_optic'},

                     {'group': 'Группа фотоники и нелинейной спектроскопии',
                      'callback': 'science_group_photonic_and_nonlinear_spectroscopy'},

                     {'group': 'Группа лазерной диагностики биомолекул '
                               'и методов фотоники в исследовании объектов культурного наследия',
                      'callback': 'science_group_laser_diagnostic_biomolecules'},

                     {'group': 'Группа лазерных систем и нелинейной спектроскопии',
                      'callback': 'science_group_laser_system_and_nonlinear_spectroscopy'},

                     {'group': 'Группа терагерцовой оптоэлектроники и спектроскопии',
                      'callback': 'science_group_THz_optoelectronics_and_spectroscopy'},

                     {'group': 'Группа нелинейной оптики и сверхсильных световых полей',
                      'callback': 'science_group_nonlinear_optics_and_super-strong_light_fields'},

                     {'group': 'Группа лазерной оптоакустики',
                      'callback': 'science_group_laser_optoacoustics'},

                     {'group': 'Группа релятивистской лазерной плазмы',
                      'callback': 'science_group_relativistic_laser_plasma'},

                     {'group': 'Группа стохастических нелинейных процессов',
                      'callback': 'science_group_stochastic_nonlinear_processes'},

                     {'group': 'Центр измерительных технологий и промышленной автоматизации',
                      'callback': 'science_group_center_for_measuring_technologies'}]


def science_group_keyboard(user: User):
    keyboard = InlineKeyboardBuilder()

    for group in scientific_groups:
        keyboard.row(InlineKeyboardButton(
            text=group['group'],
            callback_data=group['callback']))

    keyboard.row(InlineKeyboardButton(
            text="🔙  Назад  🔙",
            callback_data='science_group_🔙  Назад  🔙'))

    if user.admin:
        keyboard.row(InlineKeyboardButton(
            text="Удалить запись обо мне",
            callback_data='delete_user'))

    return keyboard
