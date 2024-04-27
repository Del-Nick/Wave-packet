import re
from pprint import pprint

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.enums import ParseMode
from Database import User, Lab
from Keyboards import *
from Pictures import *
from About_departments import scientific_groups


async def start_callback(user: User, callback: CallbackQuery):
    await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                      caption=f'Вжух! Мы в главном меню'),
                                      reply_markup=start_keyboard(user).as_markup())


async def delete_user_callback(user: User, callback: CallbackQuery):
    if user.delete_user():
        # await callback.message.edit_text(text='')
        await callback.message.reply_photo(
            photo='AgACAgIAAxkBAAPNZeXw2GcXuEmoKjPHSEC_kXpYbXwAAqLTMRvLwDBLU2CURMzsLTwBAAMCAAN4AAM0BA')

    else:
        await callback.message.edit_text(text='Вы слишком прекрасны. Не могу выкинуть вас из головы', reply_markup=None)


async def science_groups_callback(user: User, bot: Bot, callback: CallbackQuery):
    labs = AllLabs(user)
    match callback.data.replace('science_group->', ''):
        case 'start':
            # При просмотре научного направления отправляются 2 сообщения, поэтому удалять нужно оба
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

            user.action = 'science_group->page_0'
            labs = [x for x in labs.labs if x[2] is not None]
            if len(labs) == 0:
                await callback.message.edit_media(InputMediaPhoto(media=error_pictures,
                                                                  caption='Упс, кажется, тут пусто'),
                                                  reply_markup=back_keyboard(user).as_markup())
            else:
                total_pages = int(len(labs) / 4) if len(labs) % 4 == 0 else int(len(labs) / 4) + 1
                match total_pages:
                    case 1:
                        await bot.send_photo(chat_id=callback.from_user.id,
                                             photo=main_menu,
                                             caption=f'Выбери научную группу',
                                             reply_markup=science_group_keyboard(user, labs, total_pages).as_markup())
                    case _:
                        await bot.send_photo(chat_id=callback.from_user.id,
                                             photo=main_menu,
                                             caption=f'Выбери научную группу\n\n📜 Страница 1 из {total_pages}',
                                             reply_markup=science_group_keyboard(user, labs, total_pages).as_markup())

        case 'page+':
            total_pages = int(len(labs.labs) / 4) if len(labs.labs) % 4 == 0 else int(len(labs.labs) / 4) + 1
            page = int(user.action[-1]) + 1
            user.action = f'science_group->page_{page}'
            await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                              caption=f'Выбери научную группу\n\n📜 Страница {page + 1} из 4'),
                                              reply_markup=science_group_keyboard(user, labs.labs,
                                                                                  total_pages).as_markup())

        case 'page-':
            total_pages = int(len(labs.labs) / 4) if len(labs.labs) % 4 == 0 else int(len(labs.labs) / 4) + 1
            page = int(user.action[-1]) - 1
            user.action = f'science_group->page_{page}'
            await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                              caption=f'Выбери научную группу\n\n📜 Страница {page + 1} из 4'),
                                              reply_markup=science_group_keyboard(user, labs.labs,
                                                                                  total_pages).as_markup())

        case 'back_to_start_menu':
            await callback.message.edit_media(InputMediaPhoto(media=main_menu,
                                                              caption=f'Вжух! Мы в главном меню'),
                                              reply_markup=start_keyboard(user).as_markup())

        case _:
            # user.action = callback.data
            await inside_scientifit_group(user=user, callback=callback, bot=bot)

    user.update()


# TODO: функция не работает вообще, вывода нет. Переписать
async def inside_scientifit_group(user: User, bot: Bot, callback: CallbackQuery):
    _ = callback.data.split('->')
    if len(_) == 3:
        _, callback_name, action = callback.data.split('->')
    else:
        _, callback_name, action, page = callback.data.split('->')

    lab = Lab(callback_name=callback_name)

    match action:
        case 'start':
            print(user.action)
            # При просмотре научных направлений отправляется 2 сообщения с медиагруппой и текстом. Редактировать нельзя
            if 'area' in user.action:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id - 1)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id - 2)
                await bot.send_photo(chat_id=callback.from_user.id,
                                     photo=lab.main_picture,
                                     caption=f'*{lab.full_name}*\n\n{lab.about}',
                                     reply_markup=areas_courseworks_contacts_keyboard(user, lab).as_markup(),
                                     parse_mode='Markdown')
            else:
                await callback.message.edit_media(
                    InputMediaPhoto(media=lab.main_picture,
                                    caption=f'*{lab.full_name}*\n\n{lab.about}',
                                    parse_mode='Markdown'),
                    reply_markup=areas_courseworks_contacts_keyboard(user, lab).as_markup())

            user.action = f'science_group->{callback_name}->start'

        case 'courseworks':
            total_pages = len(lab.courseworks)

            if page[-1] == '+':
                page = int(page.replace('page_', '').replace('+', ''))
                page = 0 if page + 1 == total_pages else page + 1

            elif page[-1] == '-':
                page = int(page.replace('page_', '').replace('-', ''))
                page = total_pages - 1 if page - 1 < 0 else page - 1

            user.action = f'science_group->{lab.callback_name}->courseworks_{page}'

            await callback.message.edit_media(
                InputMediaPhoto(media=lab.main_picture,
                                caption=f"{lab.courseworks[page]}\n\n\n"
                                        f"📜 Страница {page + 1} из {total_pages}"),
                reply_markup=slider_keyboard(user,
                                             page=page,
                                             total_pages=total_pages,
                                             lab=lab,
                                             type_keyboard='courseworks').as_markup())

        case 'contacts':
            user.action = f'science_group->{lab.callback_name}->contacts'

            contacts = ''
            for contact in lab.contacts:
                emoji = '👨‍🎓' if contact['sex'] == 'male' else '👩‍🎓'
                contacts += (f'{emoji} {contact["person"]}\n'
                             f'📍 {contact["room"]}\n'
                             f'📧 {contact["email"]}\n\n')

            await callback.message.edit_media(
                InputMediaPhoto(media=lab.main_picture,
                                caption=contacts),
                reply_markup=back_keyboard(user).as_markup(),
                parse_mode=ParseMode.HTML)

        case 'areas':
            total_pages = len(lab.areas)

            if page[-1] == '+':
                page = int(page.replace('page_', '').replace('+', ''))
                page = 0 if page + 1 == total_pages else page + 1

            elif page[-1] == '-':
                page = int(page.replace('page_', '').replace('-', ''))
                page = total_pages - 1 if page - 1 < 0 else page - 1

            else:
                page = int(page.replace('page_', ''))

            user.action = f'science_group->photonics_and_spectroscopy->areas->page_{page}'

            if len(lab.areas[page]['pictures']) > 0:
                if len(lab.areas[page]['pictures']) > 1:
                    pictures = []
                    for pic in lab.areas[page]['pictures']:
                        pictures.append(InputMediaPhoto(media=pic['picture'],
                                                        caption=pic['desc']))
                else:
                    pictures = InputMediaPhoto(media=lab.areas[page]['pictures'][0]['picture'],
                                               caption=f"_{lab.areas[page]['pictures'][0]['desc']}_",
                                               parse_mode='Markdown')

                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
                await bot.send_media_group(chat_id=user.id,
                                           media=pictures)
                await bot.send_message(chat_id=user.id,
                                       text=f'_Описание изображений доступно при нажатии на картинку_\n\n'
                                            f'{lab.areas[page]["about"]}\n\n'
                                            f'📜 Страница {page + 1} из {len(lab.areas)}',
                                       parse_mode='Markdown',
                                       reply_markup=slider_keyboard(user, total_pages=len(lab.areas), page=page,
                                                                    lab=lab).as_markup())

            else:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
                await bot.send_message(chat_id=user.id,
                                       text=f'{lab.areas[page]["about"]}\n\n'
                                            f'📜 Страница {page + 1} из {len(lab.areas)}',
                                       parse_mode='Markdown',
                                       reply_markup=slider_keyboard(user, total_pages=len(lab.areas), page=page,
                                                                    lab=lab).as_markup())
