from aiogram.types import CallbackQuery, InputMediaPhoto
from Database import User
from Keyboards import science_group_keyboard, start_keyboard


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
        await callback.message.reply_photo(
            photo='AgACAgIAAxkBAAPNZeXw2GcXuEmoKjPHSEC_kXpYbXwAAqLTMRvLwDBLU2CURMzsLTwBAAMCAAN4AAM0BA')

    else:
        await callback.message.edit_text(text='Вы слишком прекрасны. Не могу выкинуть вас из головы', reply_markup=None)


async def science_groups_callback(user: User, callback: CallbackQuery):
    match callback.data.replace('science_group_', ''):
        case 'start':
            await callback.message.edit_text(text='Выбери научную группу',
                                             reply_markup=science_group_keyboard(user).as_markup())

        case '🔙  Назад  🔙':
            await callback.message.edit_text(f'Вжух! Мы в главном меню',
                                             reply_markup=start_keyboard(user).as_markup())

        case _:
            pass
