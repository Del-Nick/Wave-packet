import asyncio
import aiogram
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command

from config import token, allowed_users
from Database import User
from Keyboards import *
from Callbacks import *
from Handlers import *
from Registration import registration_callback, registration_handler
from AdminPanel import admin_panel

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher()


def logger(user: User, message: types.Message = None, callback: types.CallbackQuery = None):
    if message is not None:
        print(f'{datetime.now()}    Nickname:   {message.chat.username}     Action: {user.action}    {message.text}')

    elif callback is not None:
        print(f'{datetime.now()}    Nickname:   {callback.message.chat.username}     Action: {user.action}   {callback.data}')


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    print(message.chat.id, message.chat.username)
    user = User(message.chat.id, message.chat.username)
    logger(message=message, user=user)

    if user.status is None or user.new_user:
        await registration_handler(user, message, bot)

    elif user.status == 'employee' and user.nickname is None:
        await registration_handler(user, message, bot)

    elif user.status is not None and None in (user.nickname, user.usergroup):
        await registration_handler(user, message, bot)

    else:
        await start_handler(user, message, bot)


# callback на команду start
# @dp.callback_query(F.data.startswith("start"))
# async def cmd_start(callback: types.CallbackQuery):
#     user = User(callback.from_user.id, callback.from_user.username)
#     logger(callback=callback, user=user)
#     await start_callback(user, callback)


@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.message.chat.username in allowed_users:
        user = User(callback.message.chat.id, callback.message.chat.username)
        logger(callback=callback, user=user)

        # keyboard_to_delete = types.ReplyKeyboardRemove()
        # await bot.send_message(chat_id=user.id,
        #                        text='Удаляем клавиатуру',
        #                        reply_markup=keyboard_to_delete)

        if callback.data.startswith('registration'):
            await registration_callback(user, callback)

        elif callback.data.startswith('start'):
            await start_callback(user, callback)

        elif callback.data.startswith('about'):
                await callback.message.edit_media(InputMediaPhoto(media=error_pictures,
                                                                  caption='Упс, кажется, тут пусто'),
                                                  reply_markup=back_keyboard(user).as_markup())

        elif callback.data.startswith('science_group'):
            await science_groups_callback(user, callback)

        elif callback.data.startswith('admin'):
            await admin_panel(user=user, bot=bot, callback=callback)


@dp.message()
async def handler(message: types.Message):
    if message.chat.username in allowed_users:
        if message.photo is not None:
            print(message.photo[-1].file_id)
        user = User(message.chat.id, message.chat.username)
        logger(message=message, user=user)
        match user.action.split('->')[0]:
            case 'registration':
                await registration_handler(user, message, bot)

            case 'start':
                await start_handler(user, message, bot)

            case 'admin':
                await admin_panel(user=user, bot=bot, message=message)

            case _:
                await message.answer(text='Пока я не понимаю, но я активно учусь',
                                     reply_markup=delete_keyboard(user).as_markup())


# @dp.callback_query(F.data.startswith("registration->"))
# async def registration(callback: types.CallbackQuery):
#     user = User(callback.from_user.id, callback.from_user.username)
#     logger(callback=callback, user=user)
#     await registration_callback(user, callback)


# @dp.callback_query(F.data.startswith("science_group->"))
# async def science_groups(callback: types.CallbackQuery):
#     user = User(callback.from_user.id, callback.from_user.username)
#     logger(callback=callback, user=user)
#     if user.status is not None:
#         await science_groups_callback(user, callback)
#     else:
#         await science_groups_callback(user, callback)


# @dp.callback_query(F.data.startswith("about"))
# async def science_groups(callback: types.CallbackQuery):
#     user = User(callback.from_user.id, callback.from_user.username)
#     logger(callback=callback, user=user)
#     await callback.message.edit_media(InputMediaPhoto(media=error_pictures,
#                                                       caption='Упс, кажется, тут пусто'),
#                                       reply_markup=back_keyboard(user).as_markup())


@dp.callback_query(F.data.startswith("admin"))
async def science_groups(callback: types.CallbackQuery):
    user = User(callback.from_user.id, callback.from_user.username)
    logger(callback=callback, user=user)
    await admin_panel(user=user, callback=callback, bot=bot)


# @dp.callback_query(F.data.startswith("delete->"))
# async def delete(callback: types.CallbackQuery):
#     user = User(callback.from_user.id, callback.from_user.username)
#     logger(callback=callback, user=user)
#     await delete_user_callback(user, callback)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())