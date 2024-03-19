from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.enums import ParseMode
from Database import User
from Keyboards import *
from Pictures import pictures, main_menu
from About_departments import scientific_groups


async def start_callback(user: User, callback: CallbackQuery):
    await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                      caption=f'Вжух! Мы в главном меню'),
                                      reply_markup=start_keyboard(user).as_markup())


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
            await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                              caption='Выбери научную группу\n\nСтраница 1 из 4'),
                                              reply_markup=science_group_keyboard(user).as_markup())

        case 'page+':
            page = int(user.action[-1]) + 1
            user.action = f'science_group_page_{page}'
            await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                              caption=f'Выбери научную группу\n\nСтраница {page + 1} из 4'),
                                              reply_markup=science_group_keyboard(user).as_markup())

        case 'page-':
            page = int(user.action[-1]) - 1
            user.action = f'science_group_page_{page}'
            await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                              caption=f'Выбери научную группу\n\nСтраница {page + 1} из 4'),
                                              reply_markup=science_group_keyboard(user).as_markup())

        case 'back_to_start_menu':
            await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                              caption=f'Вжух! Мы в главном меню'),
                                              reply_markup=start_keyboard(user).as_markup())

        case _:
            if 'photonic_and_nonlinear_spectroscopy' in callback.data:
                await photonic_and_nonlinear_spectroscopy(user, callback)

    user.update()


async def photonic_and_nonlinear_spectroscopy(user: User, callback: CallbackQuery):
    def get_num_groups_in_list():
        # Информация о группах костыльно сделана. Поэтому приходится искать, какой индекс у группы, которую смотрит юзер
        for num, group in enumerate(scientific_groups):
            if 'photonic_and_nonlinear_spectroscopy' in group['callback']:
                return num

    if 'start' in callback.data:
        user.action = 'science_group_photonic_and_nonlinear_spectroscopy_start'
        await callback.message.edit_media(
            InputMediaPhoto(media=pictures['photonic_and_nonlinear_spectroscopy']['main'],
                            caption='Группа ведет научную работу в области нелинейной оптики и лазерной '
                                    'физики, нелинейно оптической микроскопии и спектроскопии, волоконной '
                                    'оптики, биофотоники, квантовой оптики, физики сверхсильных световых '
                                    'полей, включая вопросы генерации сверхмощных и предельно коротких '
                                    'импульсов и их приложений для исследования фундаментальных вопросов '
                                    'взаимодействия с веществом. Наряду с интенсивными экспериментальными '
                                    'работами ведутся активные теоретические исследования и численное '
                                    'суперкомпьютерное моделирование.'),
            reply_markup=areas_courseworks_contacts_keyboard(user).as_markup())

    elif 'courseworks' in callback.data:
        num = get_num_groups_in_list()

        try:
            page = int(user.action.split('_')[-1])
        except ValueError:
            page = 0

        total_pages = len(scientific_groups[num]['courseworks'])

        match callback.data.replace('science_group_photonic_and_nonlinear_spectroscopy_courseworks_', ''):
            case '+':
                page += 1
                user.action = f'science_group_photonic_and_nonlinear_spectroscopy_courseworks_{page}'

                print('я тут')

                await callback.message.edit_media(
                    InputMediaPhoto(media=pictures['photonic_and_nonlinear_spectroscopy']['main'],
                                    caption=f"{scientific_groups[num]['courseworks'][page]}\n\n\n"
                                            f"Страница {page + 1} из {total_pages}"),
                    reply_markup=slider_keyboard(user,
                                                 page=page,
                                                 total_pages=total_pages,
                                                 type_keyboard='courseworks').as_markup())

            case '-':
                page -= 1
                user.action = f'science_group_photonic_and_nonlinear_spectroscopy_courseworks_{page}'

                await callback.message.edit_media(
                    InputMediaPhoto(media=pictures['photonic_and_nonlinear_spectroscopy']['main'],
                                    caption=f"{scientific_groups[num]['courseworks'][page]}\n\n\n"
                                            f"Страница {page + 1} из {total_pages}"),
                    reply_markup=slider_keyboard(user,
                                                 page=page,
                                                 total_pages=total_pages,
                                                 type_keyboard='courseworks').as_markup())

            case _:
                user.action = f'science_group_photonic_and_nonlinear_spectroscopy_courseworks_{page}'
                await callback.message.edit_media(
                    InputMediaPhoto(media=pictures['photonic_and_nonlinear_spectroscopy']['main'],
                                    caption=f"{scientific_groups[num]['courseworks'][page]}\n\n\n"
                                            f"Страница {page + 1} из {total_pages}"),
                    reply_markup=slider_keyboard(user,
                                                 page=page,
                                                 total_pages=total_pages,
                                                 type_keyboard='courseworks').as_markup())

    elif 'contacts' in callback.data:
        user.action = 'science_group_photonic_and_nonlinear_spectroscopy_contacts'
        num = get_num_groups_in_list()

        await callback.message.edit_media(
            InputMediaPhoto(media=pictures['photonic_and_nonlinear_spectroscopy']['main'],
                            caption=scientific_groups[num]['contacts']),
            reply_markup=back_keyboard(user).as_markup(),
            parse_mode=ParseMode.HTML)

    elif 'areas' in callback.data:
        num = get_num_groups_in_list()

        # TODO: Подумать, как написать. Во время первого запроса выдаёт ошибку
        try:
            page = int(user.action.split('_')[-1])
        except ValueError:
            page = 0

        match callback.data.replace('science_group_photonic_and_nonlinear_spectroscopy_areas_', ''):
            case '+':
                page += 1
                user.action = f'science_group_photonic_and_nonlinear_spectroscopy_areas_{page}'
                await callback.message.edit_media(
                    InputMediaPhoto(media=scientific_groups[num]['areas'][page]["picture"],
                                    caption=f'{scientific_groups[num]["areas"][page]["text"]}\n\n'
                                            f'Страница {page + 1} из {len(scientific_groups[num]["areas"])}'),
                    reply_markup=slider_keyboard(user, total_pages=num, page=page).as_markup())

            case '-':
                page -= 1
                user.action = f'science_group_photonic_and_nonlinear_spectroscopy_areas_{page}'
                await callback.message.edit_media(
                    InputMediaPhoto(media=scientific_groups[num]['areas'][page]["picture"],
                                    caption=f'{scientific_groups[num]["areas"][page]["text"]}\n\n'
                                            f'Страница {page + 1} из {len(scientific_groups[num]["areas"])}'),
                    reply_markup=slider_keyboard(user, total_pages=num, page=page).as_markup())

            case _:
                user.action = f'science_group_photonic_and_nonlinear_spectroscopy_areas_{page}'
                await callback.message.edit_media(
                    InputMediaPhoto(media=scientific_groups[num]['areas'][page]["picture"],
                                    caption=f'{scientific_groups[num]["areas"][page]["text"]}\n\n'
                                            f'Страница {page + 1} из {len(scientific_groups[num]["areas"])}'),
                    reply_markup=slider_keyboard(user, total_pages=num, page=page).as_markup())
