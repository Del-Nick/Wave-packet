import asyncio
import logging
from datetime import datetime

from aiogram import Dispatcher, types

from config import token, allowed_users
from Callbacks import *
from Handlers import *
from Registration import registration_callback, registration_handler
from Admin.Admin import admin_panel
from Database import User, HistoryMessages

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher()


def logger(user: User, message: types.Message = None, callback: types.CallbackQuery = None):
    HistoryMessages(user, callback, message)
    if message is not None:
        _ = f'{datetime.now()}  |  Nickname: {message.chat.username}  |  Action: {user.action}  |  '
        if message.photo is not None:
            _ += f'Photo: {message.photo[-1].file_id}'
        if message.text is not None:
            _ += f'Message: {message.text}'
    else:
        _ = f'{datetime.now()}  |  Nickname: {callback.message.chat.username}  |  Action: {user.action}  |  ' \
            f'Callback: {callback.data}'

    with open('message & actions history.txt', mode='a+', encoding='utf-8') as f:
        f.write(f'{_}\n')
    print(_)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
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

    user.update()

    # Если у предыдущего сообщения бота была клавиатура, удаляем её
    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.message_id - 1,
        reply_markup=None
    )


# callback на команду start
# @dp.callback_query(F.data.startswith("start"))
# async def cmd_start(callback: types.CallbackQuery):
#     user = User(callback.from_user.id, callback.from_user.username)
#     logger(callback=callback, user=user)
#     await start_callback(user, callback)


@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    print(callback.data)
    if callback.message.chat.username in allowed_users:
        user = User(callback.message.chat.id, callback.message.chat.username)
        logger(callback=callback, user=user)

        if callback.data.startswith('registration'):
            await registration_callback(user=user, callback=callback)

        elif callback.data.startswith('start'):
            await start_callback(user=user, callback=callback)

        elif callback.data.startswith('about'):
            await callback.message.edit_media(InputMediaPhoto(media=error_pictures,
                                                              caption='Упс, кажется, тут пусто'),
                                              reply_markup=back_keyboard(user).as_markup())

        elif callback.data.startswith('science_group'):
            await science_groups_callback(user=user, callback=callback, bot=bot)

        elif callback.data.startswith('admin'):
            await admin_panel(user=user, bot=bot, callback=callback)

        elif user.action.startswith('admin'):
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
                print('\n', message.md_text, '\n')
                await start_handler(user=user, bot=bot, message=message)

            case 'admin':
                await admin_panel(user=user, bot=bot, message=message)

            case _:
                await message.answer(text='Пока я не понимаю, но я активно учусь',
                                     reply_markup=delete_keyboard(user).as_markup())


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
