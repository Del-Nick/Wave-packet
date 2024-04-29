import time

from aiogram.types import Message
from Pictures import main_menu
from Keyboards import *
from Database import User
from aiogram import Bot


async def start_handler(user: User, message: Message, bot: Bot):
    match user.status:
        case 'small_student':
            user.action = 'start'
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=main_menu,
                                 caption=f'Вжух! Мы в главном меню',
                                 reply_markup=start_keyboard(user).as_markup())
        case _:
            await message.answer(text='Пока я не понимаю, но я активно учусь',
                                 reply_markup=delete_keyboard(user).as_markup())


special_symbols = set('*`_~|')
symbols_to_escaping = set(',"(&{[„–«;?…»..“]}):!')
