from aiogram import Bot, Dispatcher, types, F
from Database import User


async def registration_callback(user: User, callback: types.CallbackQuery):
    print('data', callback)
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


async def delete_user_callback(user: User, callback: types.CallbackQuery):
    print('delete')
    if user.delete_user():
        await callback.message.edit_text(text='Ты хто вообще? Я тебя не знаю!', reply_markup=None)
    else:
        await callback.message.edit_text(text='Вы слишком прекрасны. Не могу выкинуть вас из головы', reply_markup=None)