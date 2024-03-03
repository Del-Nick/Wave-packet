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
from Callbacks import registration_callback, delete_user_callback
from Handlers import registration_handler

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
    if user.new_user or user.status is None:
        await registration_handler(user, message)


@dp.message()
async def handler(message: types.Message):
    if message.chat.username in allowed_users:
        user = User(message.chat.id, message.chat.username)
        print(user.action, user.new_user)
        match user.action:
            case 'registration':
                await registration_handler(user, message)
            case _:
                await message.answer(text='Пока я не понимаю, но я активно учусь',
                                     reply_markup=delete_keyboard(user).as_markup())


@dp.callback_query(F.data.startswith("registration_"))
async def registration(callback: types.CallbackQuery):
    user = User(callback.from_user.id, callback.from_user.username)
    await registration_callback(user, callback)


@dp.callback_query(F.data.startswith("delete_"))
async def delete(callback: types.CallbackQuery):
    user = User(callback.from_user.id, callback.from_user.username)
    await delete_user_callback(user, callback)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
