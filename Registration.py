from aiogram.types import Message
from aiogram import Bot
from aiogram.types import CallbackQuery
from Keyboards import *
from Pictures import *


async def registration_handler(user: User, message: Message, bot: Bot):
    if user.new_user:
        await message.answer("Привет! Я бот кафедры волновых процессов. Чтобы мы оба меньше волновались, давай чуток "
                             "познакомимся. Выбери, в каком статусе ты находишься",
                             reply_markup=registration_keyboard(user).as_markup())

    elif 'registration_' in user.action:
        match user.action.replace('registration_', ''):
            case 'nickname':
                user.nickname = message.text

                match user.status:
                    case 'small_student' | 'student':
                        user.action = 'registration_usergroup'
                        await message.answer(f'Супер, {user.nickname}. Укажи номер группы, в которой ты учишься',
                                             reply_markup=None)

                    case 'employee':
                        user.action = 'start'
                        await message.reply_photo(photo=main_menu,
                                                  caption=f'Супер, {user.nickname}. Пока я не знаю, что показать '
                                                          f'сотрудникам',
                                                  reply_markup=start_keyboard(user).as_markup())

            case 'usergroup':
                # Проверяем, что группа из трёх цифр
                try:
                    if len(message.text) == 3:
                        user.usergroup = int(message.text)
                        user.action = 'start'

                        match user.status:
                            case 'student':
                                await bot.send_photo(chat_id=message.chat.id,
                                                     photo=main_menu,
                                                     caption=f'Супер, {user.nickname}. Я запомнил, что ты из '
                                                             f'группы {user.usergroup}. Пока я не знаю, что показать '
                                                             f'студентам кафедры',
                                                     reply_markup=start_keyboard(user).as_markup())
                            case 'small_student':
                                await bot.send_photo(chat_id=message.chat.id,
                                                     photo=main_menu,
                                                     caption=f'Супер, {user.nickname}. Я запомнил, что ты из '
                                                             f'группы {user.usergroup}',
                                                     reply_markup=start_keyboard(user).as_markup())
                    else:
                        raise ValueError

                except ValueError:
                    await message.answer(f'Погоди, {user.nickname}. Твоя группа должна состоять из трёх цифр. Введи '
                                         f'реальную группу, пожалуйста',
                                         reply_markup=None)



    else:
        user.action = 'start'
        await message.answer(text='Пока я не понимаю, но я активно учусь',
                             reply_markup=delete_keyboard(user).as_markup())

    user.update()


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