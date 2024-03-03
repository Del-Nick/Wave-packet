from aiogram.types import Message

from Keyboards import registration_keyboard, delete_keyboard
from Database import User


async def registration_handler(user: User, message: Message):
    print(user.new_user)
    if user.new_user:
        await message.answer("Привет! Я бот кафедры волновых процессов. Чтобы мы оба меньше волновались, давай чуток "
                             "познакомимся. Выбери, в каком статусе ты находишься",
                             reply_markup=registration_keyboard(user).as_markup())

    elif 'registration_' in user.action:
        match user.action.replace('registration_', ''):
            case 'nickname':
                user.nickname = message.text

                await message.answer(f'Супер, {user.nickname}')

    else:
        user.action = 'start'
        await message.answer(text='Пока я не понимаю, но я активно учусь',
                             reply_markup=delete_keyboard(user).as_markup())