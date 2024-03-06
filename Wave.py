import asyncio
import aiogram
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command

from config import token, allowed_users
from Database import User
from Keyboards import *
from Callbacks import *
from Handlers import *

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user = User(message.chat.id, message.chat.username)

    if user.status is None or user.new_user:
        await registration_handler(user, message)

    elif user.status == 'employee' and user.nickname is None:
        await registration_handler(user, message)

    elif user.status is not None and None in (user.nickname, user.usergroup):
        await registration_handler(user, message)
    else:
        await start_handler(user, message)


@dp.message()
async def handler(message: types.Message):
    if message.chat.username in allowed_users:
        if message.photo is not None:
            print(message.photo[-1].file_id)
        user = User(message.chat.id, message.chat.username)
        match user.action.split('_')[0]:
            case 'registration':
                await registration_handler(user, message)

            case 'start':
                await start_handler(user, message)

            case _:
                await message.answer(text='Пока я не понимаю, но я активно учусь',
                                     reply_markup=delete_keyboard(user).as_markup())


@dp.callback_query(F.data.startswith("registration_"))
async def registration(callback: types.CallbackQuery):
    user = User(callback.from_user.id, callback.from_user.username)
    await registration_callback(user, callback)


@dp.callback_query(F.data.startswith("science_group_"))
async def science_groups(callback: types.CallbackQuery):
    print(callback.data)
    user = User(callback.from_user.id, callback.from_user.username)
    if user.status is not None:
        await science_groups_callback(user, callback)
    else:
        await registration_handler(user, callback.message)


@dp.callback_query(F.data.startswith("delete_"))
async def delete(callback: types.CallbackQuery):
    user = User(callback.from_user.id, callback.from_user.username)
    await delete_user_callback(user, callback)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
