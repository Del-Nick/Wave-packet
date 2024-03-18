from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.markdown import hide_link
from Database import User
from Keyboards import *
from Pictures import pictures


async def registration_callback(user: User, callback: CallbackQuery):
    if user.status is None:
        match callback.data:
            case 'registration_small_student':
                user.status = 'small_student'
                await callback.message.edit_text(text='Отлично! Как я могу к тебе обращаться?', reply_markup=None)

            case 'registration_student':
                user.status = 'student'
                await callback.message.edit_text(text='Отлично! Как я могу к тебе обращаться?', reply_markup=None)

            case 'registration_employee':
                user.status = 'employee'
                await callback.message.edit_text(text='Отлично! Как я могу к Вам обращаться?', reply_markup=None)

        user.action = 'registration_nickname'
        user.update()


async def delete_user_callback(user: User, callback: CallbackQuery):
    if user.delete_user():
        # await callback.message.edit_text(text='')
        await callback.message.reply_photo(
            photo='AgACAgIAAxkBAAPNZeXw2GcXuEmoKjPHSEC_kXpYbXwAAqLTMRvLwDBLU2CURMzsLTwBAAMCAAN4AAM0BA')

    else:
        await callback.message.edit_text(text='Вы слишком прекрасны. Не могу выкинуть вас из головы', reply_markup=None)


async def science_groups_callback(user: User, callback: CallbackQuery):
    match callback.data.replace('science_group_', ''):
        case 'start':
            user.action = 'science_group_page_0'
            await callback.message.edit_text(text='Выбери научную группу\n\nСтраница 1 из 4',
                                             reply_markup=science_group_keyboard(user).as_markup())

        case 'page+':
            page = int(user.action[-1]) + 1
            user.action = f'science_group_page_{page}'
            await callback.message.edit_text(text=f'Выбери научную группу\n\nСтраница {page + 1} из 4',
                                             reply_markup=science_group_keyboard(user).as_markup())

        case 'page-':
            page = int(user.action[-1]) - 1
            user.action = f'science_group_page_{page}'
            await callback.message.edit_text(text=f'Выбери научную группу\n\nСтраница {page + 1} из 4',
                                             reply_markup=science_group_keyboard(user).as_markup())

        case '🔙  Назад  🔙':
            await callback.message.edit_text(f'Вжух! Мы в главном меню',
                                             reply_markup=start_keyboard(user).as_markup())

        case _:
            if 'photonic_and_nonlinear_spectroscopy' in callback.data:
                await photonic_and_nonlinear_spectroscopy(user, callback)

    user.update()


async def photonic_and_nonlinear_spectroscopy(user: User, callback: CallbackQuery):
    match callback.data.replace('science_group_photonic_and_nonlinear_spectroscopy_', ''):
        case 'start':
            user.action = 'science_group_photonic_and_nonlinear_spectroscopy_start'
            await callback.message.edit_text(f'Группа ведет научную работу в области нелинейной оптики и лазерной '
                                             'физики, нелинейно оптической микроскопии и спектроскопии, волоконной '
                                             'оптики, биофотоники, квантовой оптики, физики сверхсильных световых '
                                             'полей, включая вопросы генерации сверхмощных и предельно коротких '
                                             'импульсов и их приложений для исследования фундаментальных вопросов '
                                             'взаимодействия с веществом. Наряду с интенсивными экспериментальными '
                                             'работами ведутся активные теоретические исследования и численное '
                                             f'суперкомпьютерное моделирование.{hide_link(pictures["photonic_and_nonlinear_spectroscopy"]["main"])}',
                                             reply_markup=areas_courseworks_contacts_keyboard(user).as_markup())

        case 'areas':
            await callback.message.edit_text('Оптика сверхкоротких импульсов\n\nНаучной группой лаборатории '
                                             'разработан и создан уникальный лазерный источник субтераваттных '
                                             'сверхкоротких импульсов среднего инфракрасного излучения.',
                                             reply_markup=areas_courseworks_contacts_keyboard(user).as_markup())
            await callback.message.reply_photo(pictures['photonic_and_nonlinear_spectroscopy']['ultra_short_pulse'])