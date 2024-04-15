import re

from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.enums import ParseMode
from aiogram import Bot

from numpy.random import randint
from dataclasses import dataclass

from Database import User, Lab
from Keyboards import *
from Pictures import admin, motivation, error_pictures
from Callbacks import start_callback

phrases = ['Если вы можете мечтать об этом, вы можете это сделать. | Уолт Дисней',
           'Успех - это идти от неудачи к неудаче, не теряя энтузиазма. | Уинстон Черчилль',
           'Не считай дни, извлекай из них пользу. | Мухаммед Али',
           'Не ждите. Время никогда не будет подходящим. | Наполеон Хилл',
           'Неисследованная жизнь не стоит того, чтобы ее жить. | Сократ',
           'Я не потерпел неудачу. Я просто нашел 10 000 способов, которые не работают. | Томас Эдисон',
           'Мотивация - это то, что заставляет вас начать. Привычка - это то, что заставляет вас продолжать. | Джим Рюн',
           'Вы должны выучить правила игры. А затем вы должны играть лучше, чем кто-либо другой. | Альберт Эйнштейн',
           'Если вы потратите свою жизнь на то, чтобы быть лучшим во всем, вы никогда не станете великим ни в чем. | Том Рат',
           'Сначала они не замечают тебя, затем смеются над тобой, потом борются с тобой, а потом ты побеждаешь. | Махатма Ганди',
           'Мечтатели - это спасители мира. | Джеймс Аллен',
           'Лучшая месть - это огромный успех. | Фрэнк Синатра',
           'Измени свои мысли и ты изменишь мир. | Норман Винсент Пил',
           'Упорный труд побеждает талант, когда талант не трудится.',
           'По моему опыту, существует только одна мотивация, и это - желание. Никакие причины или принципы не могут его сдержать и или противостоять ему. | Джейн Смайли',
           'Мужество - первое из человеческих качеств, потому что это качество, которое гарантирует все остальные. | Уинстон '
           'Черчилль',
           'Победа - это еще не все, главное это постоянное желание побеждать. | Винс Ломбарди',
           'Чтобы справиться с собой, используйте голову; чтобы справиться с другими, используйте свое сердце. | Элеонора Рузвельт',
           'Неудача никогда не одолеет меня, если моя решимость добиться успеха достаточно сильна. | Ог Мандино'
           'Я всегда выберу ленивого человека для выполнения сложной работы, потому что он найдет легкий путь ее выполнения. | '
           'Билл Гейтс']


async def admin_panel(user: User, bot: Bot, callback: CallbackQuery = None, message: Message = None):
    # Тут происходит что-то страшное. Пытаемся обработать одной функцией и callback, и сообщения входящие
    # Если приходит callback, меняем сообщение. Если приходит сообщение, отправляем ответное
    if callback:
        if 'back' in callback.data:
            await bot.delete_message(chat_id=user.id, message_id=callback.message.message_id)
            if user.nickname == 'Nikatkavr':
                await bot.send_photo(chat_id=user.id,
                                     photo=admin,
                                     caption='Возвращаю тебя в главное меню, моя госпожа',
                                     reply_markup=admin_keyboard(user).as_markup())
            else:
                await bot.send_photo(chat_id=user.id,
                                     photo=admin,
                                     caption='Возвращаю тебя в главное меню, мой господин',
                                     reply_markup=admin_keyboard(user).as_markup())
            user.action = 'admin->start'
        else:
            if 'admin' in callback.data or 'start' in callback.data:
                user.action = callback.data

            if user.action == 'start':
                await start_callback(user, callback)
            elif 'start' in user.action.split('->')[1]:
                if user.nickname == 'Nikatkavr':
                    await callback.message.edit_media(
                        InputMediaPhoto(media=admin,
                                        caption='Привет, моя госпожа'),
                        reply_markup=admin_keyboard(user).as_markup())
                else:
                    await callback.message.edit_media(
                        InputMediaPhoto(media=admin,
                                        caption='Привет, мой господин'),
                        reply_markup=admin_keyboard(user).as_markup())

            elif 'joke' in user.action:
                await callback.message.edit_media(
                    InputMediaPhoto(media=motivation,
                                    caption=phrases[randint(0, len(phrases))]),
                    reply_markup=back_keyboard(user).as_markup())

            elif 'add_science_group' in user.action:
                await add_science_group(user, callback=callback, bot=bot)

            elif 'edit_science_group' in user.action:
                await edit_field(user, callback=callback, bot=bot)

            elif 'delete_science_group' in user.action:
                await delete_science_group(user, callback=callback, bot=bot)

            else:
                await callback.message.edit_media(InputMediaPhoto(media=error_pictures,
                                                                  caption='Упс, кажется, тут пусто'),
                                                  reply_markup=back_keyboard(user).as_markup())

    else:
        if 'add_science_group' in user.action:
            await add_science_group(user, message=message, bot=bot)

        elif 'edit_science_group' in user.action:
            await edit_field(user, message=message, bot=bot)

        elif 'delete_science_group' in user.action:
            await delete_science_group(user, message=message, bot=bot)

    user.update()


async def add_science_group(user: User, bot: Bot, message: Message = None, callback: CallbackQuery = None):
    if 'start' in user.action:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await bot.send_message(chat_id=user.id,
                               text='Напиши полное официальное название научной группы',
                               reply_markup=back_keyboard_without_callback(user).as_markup())
        user.action = 'admin->add_science_group->add_full_name'

    elif 'add_full_name' in user.action:
        result, lab = edit_full_name(user, message)

        if result.success:
            await bot.send_message(chat_id=user.id,
                                   text=f'Редактируем научную группу: {message.text}.\n\n'
                                        f'Введи короткое название научной группы, которое будет отображаться на '
                                        f'кнопках. Помни, что оно не должно превышать 64 символа, однако лучше '
                                        f'сделать его короче',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

            user.action = f'admin->add_science_group->add_short_name_id={lab.id}'

        else:
            if result.error == 'group already exist':
                await bot.send_message(chat_id=user.id,
                                       text='Эта научная группа уже добавлена',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

            else:
                await database_error_message(user, bot)

    elif 'add_short_name' in user.action:
        result, lab = edit_short_name(user, message)

        if result.success:
            await bot.send_message(chat_id=user.id,
                                   text=f'Супер! Напиши callback-название, которое будет использоваться для '
                                        f'внутренней работы бота на английском языке по следующему образцу:\n\n'
                                        f'this_is_just_an_example\n\n'
                                        f'Название не должно превышать 40 символов и должно быть напрямую связано с '
                                        f'названием научное группы',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

            user.action = f'admin->add_science_group->add_callback_name_id={lab.id}'

        elif result.error == 'short name already exist':
            await bot.send_message(chat_id=user.id,
                                   text='Такое короткое имя уже существует. Выбери другое',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        elif result.error == 'too long':
            await bot.send_message(chat_id=user.id,
                                   text=f'В названии количество символов равно {len(message.text)}, а нужно не больше '
                                        f'64. Сократи, пожалуйста, название',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        else:
            await database_error_message(user, bot)

    elif 'add_callback_name' in user.action:
        result, lab = edit_callback_name(user, message)

        if result.success:
            await bot.send_message(chat_id=user.id,
                                   text='Отлично! Пришли мне картинку, которая будет отображаться на главной '
                                        'странице научной группы',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())
            user.action = f'admin->add_science_group->add_main_picture_id={lab.id}'

        elif result.error == 'too long':
            await bot.send_message(chat_id=user.id,
                                   text=f'В названии количество символов равно {len(message.text)}, а нужно не больше '
                                        f'40. Сократи, пожалуйста, название',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        elif result.error == 'callback already exist':
            await bot.send_message(chat_id=user.id,
                                   text='Такое callback имя уже существует. Выбери другое',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        else:
            await database_error_message(user, bot)

    elif 'add_main_picture' in user.action:
        result, lab = edit_main_pictures(user, message)

        if result.success:
            await bot.send_message(chat_id=user.id,
                                   text='Так, картинку сохранил. Теперь напиши описание научной группы. '
                                        'Пожалуйста, помни, что длинный текст большая часть пользователей читать '
                                        'не будет',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

            user.action = f'admin->add_science_group->add_about_id={lab.id}'

        elif result.error == 'document is given':
            await bot.send_message(chat_id=user.id,
                                   text='Пришли изображение как картинку (со сжатием), а не как документ',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        elif result.error == 'no picture':
            await bot.send_message(chat_id=user.id,
                                   text='Картинка не прикрепилась 🥺',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        else:
            await database_error_message(user, bot)

    elif 'add_about' in user.action:
        result, lab = edit_about_group(user, message)

        if result.success:
            await bot.send_message(chat_id=user.id,
                                   text='Описание добавил\. Перейдём к научным направлениям\. Отправляй мне информацию '
                                        'по следующему образцу:\n\n'
                                        ''
                                        '*Название:* \n\n\n'
                                        ''
                                        '*Описание:* \n\n\n'
                                        ''
                                        '*Контакты:* \(потенциального научного руководителя\)\n\n\n'
                                        '*Подробнее:* только одна ссылка на более подробное описание без '
                                        'дополнительного текста \(по желанию\)\n\n'
                                        ''
                                        'Важно\! Не забудь прикрепить картинку к сообщению, оставить слова\n'
                                        '"*Название:* "\n'
                                        '"*Описание:* "\n'
                                        '"*Контакты:* "\n'
                                        '"*Подробнее:* "\n\n'
                                        'По ним я пойму, если чего\-то не хватает\. Между пунктами оставляй *__две '
                                        'пустые строки__*, а между своими абзацами *__одну__*\.'
                                        '\n\n'
                                        'Если считаешь, что все направления указаны, то жми на кнопку "Далее"',
                                   reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                   parse_mode="MarkdownV2")

            user.action = f'admin->add_science_group->add_areas_id={lab.id}'

        elif result.error == 'too long':
            await bot.send_message(chat_id=user.id,
                                   text=f'Описание получилось слишком длинным. Количество символов '
                                        f'{len(message.text)}, а должно быть меньше 1024. Сократи описание',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        else:
            print()
            await database_error_message(user, bot)

    elif 'add_areas' in user.action:
        if callback:
            lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

            if callback.data == 'Далее':
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
                await bot.send_message(chat_id=user.id,
                                       text=f'Напиши мне контакты, по которым можно связаться с научной группой в '
                                            f'следующем формате:\n\n'
                                            f''
                                            f'*Должность ФИО*\n'
                                            f'*Кабинет*\n'
                                            f'*Электронная почта*\n\n'
                                            f''
                                            f'На этот раз можно не вставлять кодовых слов, а просто писать текстом по '
                                            f'образцу\. Если хочешь добавить несколько контактов, оставляй между '
                                            f'людьми *__одну__* пустую строку',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='MarkdownV2')

            user.action = f'admin->add_science_group->add_contacts_id={lab.id}'

        else:
            result, lab = edit_areas(user, message)

            if result.success:
                await bot.send_message(chat_id=user.id,
                                       text=f'Записал\. Теперь прикрепи фотографии *__по одной__*, сопровождая их '
                                            f'описанием',
                                       reply_markup=back_keyboard_without_callback(user,
                                                                                   button='Следующее '
                                                                                          'направление').as_markup(),
                                       parse_mode='MarkdownV2')
                user.action = f'admin->add_science_group->add_picture_to_area_id={lab.id}'

            elif result.error == 'no title':
                await bot.send_message(chat_id=user.id,
                                       text='Не могу понять, где название. Не забывай оставлять кодовое слово перед '
                                            'названием:\n\n'
                                            '*Название:*',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='Markdown')

            elif result.error == 'no about':
                await bot.send_message(chat_id=user.id,
                                       text='Не могу понять, где описание. Не забывай оставлять кодовое слово перед '
                                            'описанием:\n\n'
                                            '*Описание:*',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='Markdown')

            elif result.error == 'no contacts':
                await bot.send_message(chat_id=user.id,
                                       text='Не могу понять, где контакты. Не забывай оставлять кодовое слово перед '
                                            'контактами:\n\n'
                                            '*Контакты:*',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='Markdown')

            elif result.error == 'no indents':
                await bot.send_message(chat_id=user.id,
                                       text='Для меня очень важно, чтобы между пунктами было *__2 пустые__* строки\. '
                                            'Исправь, пожалуйста',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='MarkdownV2')

            else:
                await database_error_message(user, bot)

    elif 'add_picture_to_area' in user.action:
        lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

        if callback:
            lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

            if 'Следующее направление' in callback.data:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
                await bot.send_message(chat_id=user.id,
                                       text='Картинку добавил\. Можешь отправить следующее научное направление по '
                                            'тому же образцу:\n\n'
                                            ''
                                            '*Название:* \n\n\n'
                                            ''
                                            '*Описание:* \n\n\n'
                                            ''
                                            '*Контакты:* \(потенциального научного руководителя\)\n\n\n'
                                            '*Подробнее:* *__только одна__* ссылка на более подробное описание без '
                                            'дополнительного текста \(по желанию\)\n\n\n'
                                            ''
                                            'Важно\! Не забудь прикрепить картинку к сообщению, оставить слова\n'
                                            '"*Название:* "\n'
                                            '"*Описание:* "\n'
                                            '"*Контакты:* "\n'
                                            '"*Подробнее:* "\n\n'
                                            'По ним я пойму, если чего\-то не хватает\. Между пунктами оставляй *__две '
                                            'пустые строки__*, а между своими абзацами *__одну__*'
                                            '\n\n'
                                            'Если считаешь, что все направления указаны, то жми на кнопку "Далее"',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode="MarkdownV2")

                user.action = f'admin->add_science_group->add_areas_id={lab.id}'

        else:
            result, lab = edit_area_pictures(user, message)

            if result.success:
                await bot.send_message(chat_id=user.id,
                                       text='Записал. Можешь отправить ещё картинки или перейти к следующему '
                                            'направлению',
                                       reply_markup=back_keyboard_without_callback(user,
                                                                                   button='Следующее направление').as_markup())

            elif result.error == 'document is given':
                await bot.send_message(chat_id=user.id,
                                       text='Прикрепляй изображение *__как картинку__* (со сжатием), а не как документ',
                                       reply_markup=back_keyboard_without_callback(user).as_markup(),
                                       parse_mode="MarkdownV2")

            elif result.error == 'no picture':
                await bot.send_message(chat_id=user.id,
                                       text='Не вижу картинки. Ты не забыл её прикрепить?',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

            else:
                await database_error_message(user, bot)

    elif 'add_contacts' in user.action:
        # Своего рода костыль. Чтобы не переходить к следующему этапу, если пользователь прислал неправильно оформленный
        # текст
        success = False

        if callback:
            lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

            if 'Далее' in callback.data:
                await bot.send_message(chat_id=user.id,
                                       text='И последний этап\. Добавь темы курсовых работ, которыми могут заниматься '
                                            'студенты\. Если будешь добавлять по одной работе, то отправляй сообщения '
                                            'по следующему образцу:\n\n'
                                            ''
                                            '*Название*\n'
                                            '*Научный руководитель*\n'
                                            '*Контакт научного руководителя*\n\n'
                                            ''
                                            'Я могу обрабатывать и по несколько курсовых за раз\. Отправляй сообщения '
                                            'по тому же образцу, но оставляй пустую строку между информацией:\n\n'
                                            ''
                                            '*Название*\n'
                                            '*Научный руководитель*\n'
                                            '*Контакт научного руководителя*\n\n'
                                            ''
                                            '*Название*\n'
                                            '*Научный руководитель*\n'
                                            '*Контакт научного руководителя*\n\n'
                                            ''
                                            'Кодовые слова в этот раз тоже не обязательны',
                                       reply_markup=back_keyboard_without_callback(user,
                                                                                   button='Завершить').as_markup())

                user.action = f'admin->add_science_group->add_courseworks_id={lab.id}'

        else:
            result, lab = edit_contacts(user, message)

            if result.success:
                await bot.send_message(chat_id=user.id,
                                       text='И последний этап. Добавь темы курсовых работ, которыми могут заниматься '
                                            'студенты. Если будешь добавлять по одной работе, то отправляй сообщений '
                                            'по следующему образцу:\n\n'
                                            ''
                                            '*Название*\n'
                                            '*Научный руководитель*\n'
                                            '*Контакт научного руководителя*\n\n'
                                            ''
                                            'Я могу обрабатывать и по несколько курсовых за раз. Отправляй сообщения '
                                            'по тому же образцу, но оставляй пустую строку между информацией:\n\n'
                                            ''
                                            '*Название*\n'
                                            '*Научный руководитель*\n'
                                            '*Контакт научного руководителя*\n\n'
                                            ''
                                            '*Название*\n'
                                            '*Научный руководитель*\n'
                                            '*Контакт научного руководителя*\n\n'
                                            ''
                                            'Оставлять кодовые слова необязательно',
                                       reply_markup=back_keyboard_without_callback(user,
                                                                                   button='Завершить').as_markup(),
                                       parse_mode='Markdown')

                user.action = f'admin->add_science_group->add_courseworks_id={lab.id}'

            elif result.error == 'not enough information':
                await bot.send_message(chat_id=user.id,
                                       text=f'Об одном или нескольких сотрудниках дана неполная информация\. О каждом '
                                            f'человеке информация должна быть заполнена по образцу:\n\n'
                                            ''
                                            '*к\.ф\.\-м\.н\. Иванов Иван Иванович*\n'
                                            '*7\-05\, КНО*\n'
                                            '*any_email_adress@any_server\.any_domen*\n\n',
                                       reply_markup=back_keyboard_without_callback(user).as_markup(),
                                       parse_mode='MarkdownV2')

            else:
                await database_error_message(user, bot)

    elif 'add_courseworks' in user.action:
        if callback:
            if 'Завершить' in callback.data:
                if user.nickname == 'Nikatkavr':
                    await bot.send_photo(chat_id=message.chat.id,
                                         photo=admin,
                                         caption='Редактирование научного направления завершено, моя госпожа',
                                         reply_markup=admin_keyboard(user).as_markup())
                else:
                    await bot.send_photo(chat_id=user.id,
                                         photo=admin,
                                         caption='Редактирование научного направления завершено, мой господин',
                                         reply_markup=admin_keyboard(user).as_markup())

                user.action = 'admin->start'

        else:
            result, lab = edit_area_pictures(user, message)

            if result.success:
                await bot.send_message(chat_id=message.chat.id,
                                       text=f'Записал. Можешь прислать ещё или нажать кнопку "Завершить"',
                                       reply_markup=back_keyboard_without_callback(user,
                                                                                   button='Завершить').as_markup(),
                                       parse_mode='Markdown')

            elif result.error == 'not enough information':
                await bot.send_message(chat_id=message.chat.id,
                                       text='У одной или нескольких курсовых работ информация неполная. Я не могу '
                                            'такое записать. Нужно исправить',
                                       reply_markup=back_keyboard_without_callback(user,
                                                                                   button='Завершить').as_markup(),
                                       parse_mode='Markdown')

            else:
                await database_error_message(user, bot)

    user.update()


# TODO: добавить общие методы для добавления научной группы и редактирования

async def edit_field(user: User, bot: Bot, message: Message = None, callback: CallbackQuery = None):
    if 'start' in user.action:
        labs = AllLabs()
        if len(labs.labs) == 0:
            if user.nickname == 'Nikatkavr':
                await callback.message.edit_media(
                    InputMediaPhoto(media=admin,
                                    caption='Нечего редактировать, моя госпожа'),
                    reply_markup=admin_keyboard(user).as_markup())
            else:
                await callback.message.edit_media(
                    InputMediaPhoto(media=admin,
                                    caption='Нечего редактировать, мой господин'),
                    reply_markup=admin_keyboard(user).as_markup())
        else:
            list_labs = ''
            for lab in labs.labs:
                list_labs += f'\n{lab[0]}. {lab[2]}'

            if callback:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await bot.send_message(chat_id=user.id,
                                   text=f'Напиши номер научной группы, которую хочешь отредактировать:\n{list_labs}',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

            user.action = 'admin->edit_science_group->get_id'

    elif 'get_id' in user.action:
        try:
            labs = AllLabs()
            group_id = int(message.text)

            if group_id >= len(labs.labs) or group_id < 0:
                await bot.send_message(chat_id=user.id,
                                       text='Кажется, число введено неправильно. Проверь номер группы и попробуй ещё '
                                            'раз',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())
            else:
                lab = Lab(id=group_id)
                await bot.send_message(chat_id=user.id,
                                       text=f'Выбрано: {lab.short_name}. Теперь нужно решить, какое поле будем менять',
                                       reply_markup=fields_to_edit().as_markup())

                user.action = f'admin->edit_science_group->selecting_field_id={group_id}'

        except ValueError:
            await bot.send_message(chat_id=user.id,
                                   text='Ты точно правильно ввёл число? Оно должно соответствовать номеру научной '
                                        'группы',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

    if callback:
        if 'full_name' in callback.data:
            lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))


@dataclass
class EditingResult:
    success: bool
    error: str = None


def edit_full_name(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    labs = AllLabs(user)
    lab = Lab(full_name=message.text)

    if len(labs.labs) == 0:
        if lab.add_new_lab():
            return EditingResult(success=True), lab

        else:
            return EditingResult(success=False, error='database error'), lab

    elif message.text in [x[1] for x in labs.labs]:
        return EditingResult(success=False, error='group already exist'), lab

    else:
        if lab.add_new_lab():
            return EditingResult(success=True), lab

        else:
            return EditingResult(success=False, error='database error'), lab


def edit_short_name(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))
    labs = AllLabs()

    if message.text in [x[2] for x in labs.labs]:
        return EditingResult(success=False, error='short name already exist'), lab

    elif len(message.text) > 64:
        return EditingResult(success=False, error='too long'), lab

    else:
        lab.short_name = message.text
        if lab.update():
            return EditingResult(success=True), lab

        else:
            return EditingResult(success=False, error='database error'), lab


def edit_callback_name(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))
    labs = AllLabs()

    if message.text in [x[3] for x in labs.labs]:
        if message.text in [x[2] for x in labs.labs]:
            return EditingResult(success=False, error='callback already exist'), lab

    elif len(message.text) > 40:
        return EditingResult(success=False, error='too long'), lab

    else:
        lab.callback_name = message.text
        if lab.update():
            return EditingResult(success=True), lab

        else:
            return EditingResult(success=False, error='database error'), lab


def edit_main_pictures(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

    if message.photo is None:
        if message.document is not None:
            return EditingResult(success=False, error='document is given'), lab
        else:
            return EditingResult(success=False, error='no picture'), lab

    else:
        lab.main_picture = message.photo[-1].file_id
        if lab.update():
            return EditingResult(success=True), lab

        else:
            return EditingResult(success=False, error='database error'), lab


def edit_about_group(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))
    lab.about = message.text

    if len(message.text) > 1024:
        return EditingResult(success=False, error='too long'), lab

    elif lab.update():
        return EditingResult(success=True), lab

    else:
        return EditingResult(success=False, error='database error'), lab


def edit_areas(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))
    num = False

    if 'Название:' not in message.text:
        return EditingResult(success=False, error='no title'), lab

    elif 'Описание:' not in message.text:
        return EditingResult(success=False, error='no about'), lab

    elif 'Контакты:' not in message.text:
        return EditingResult(success=False, error='no contacts'), lab

    elif '\n\n\n' not in message.text or len(message.text.split('\n\n\n')) < 3:
        return EditingResult(success=False, error='no indents'), lab

    else:
        _ = message.text.split('\n\n\n')
        data_to_paste = {'title': _[0].replace('Название:', ''),
                         'about': _[1].replace('Описание:', ''),
                         'contacts': _[2].replace('Контакты:', '')}
        if len(_) == 4:
            data_to_paste['more'] = _[3].replace('Подробнее:', '')

        if type(lab.areas) is list:
            if num:
                lab.areas[num] = data_to_paste
            else:
                lab.areas.append(data_to_paste)
        else:
            lab.areas = [data_to_paste]

        if lab.update():
            return EditingResult(success=True), lab

        else:
            return EditingResult(success=False, error='database error'), lab


def edit_area_pictures(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))
    # Здесь будет номер научного направления
    num = False

    if message.photo is None:
        if message.document is not None:
            return EditingResult(success=False, error='document is given'), lab

        else:
            return EditingResult(success=False, error='no picture'), lab

    else:
        if num:
            lab.areas[-1]['pictures'] = {'picture': message.photo[-1].file_id,
                                         'desc': message.caption}
        else:
            if 'pictures' in lab.areas[-1].keys():
                lab.areas[-1]['pictures'].append({'picture': message.photo[-1].file_id,
                                                  'desc': message.caption})
            else:
                lab.areas[-1]['pictures'] = [{'picture': message.photo[-1].file_id,
                                              'desc': message.caption}]

        if lab.update():
            return EditingResult(success=True), lab

        else:
            return EditingResult(success=False, error='database error'), lab


def edit_contacts(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

    if '\n\n' in message.text:
        for human in message.text.split('\n\n'):
            if len(human.split('\n')) != 3:
                return EditingResult(success=False, error='not enough information'), lab

            else:
                _ = human.split('\n')
                data_to_paste = {'person': _[0],
                                 'room': _[1],
                                 'email': _[2]}
                print(data_to_paste)
                if lab.contacts is None:
                    lab.contacts = [data_to_paste]
                else:
                    lab.contacts.append(data_to_paste)

                print(lab.contacts)

    else:
        if len(message.text.split('\n')) != 3:
            return EditingResult(success=False, error='not enough information'), lab

        else:
            _ = message.text.split('\n')
            data_to_paste = {'person': _[0],
                             'room': _[1],
                             'email': _[2]}
            if lab.contacts is None:
                lab.contacts = [data_to_paste]
            else:
                lab.contacts.append(data_to_paste)

    if lab.update():
        return EditingResult(success=True), lab

    else:
        return EditingResult(success=False, error='database error'), lab


def edit_courseworks(user: User, message: Message = None) -> tuple[EditingResult, Lab]:
    lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

    if '\n\n' in message.text:
        for coursework in message.text.split('\n\n'):
            _ = coursework.split('\n')
            if len(_) < 3:
                return EditingResult(success=False, error='not enough information'), lab

            else:
                _ = {'title': _[0],
                     'teacher': _[1],
                     'contact': _[2]}

                lab.courseworks = [_] if lab.courseworks is None else lab.courseworks.apend(_)

    else:
        _ = message.text.split('\n')
        if len(_) < 3:
            return EditingResult(success=False, error='not enough information'), lab

        else:
            _ = {'title': _[0],
                 'teacher': _[1],
                 'contact': _[2]}

            lab.courseworks = [_] if lab.courseworks is None else lab.courseworks.apend(_)

    if lab.update():
        return EditingResult(success=True), lab

    else:
        return EditingResult(success=False, error='database error'), lab


async def delete_science_group(user: User, bot: Bot, message: Message = None, callback: CallbackQuery = None):
    labs = AllLabs(user=user)

    if 'start' in user.action:
        if len(labs.labs) > 0:
            if callback:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            list_labs = 'Напиши номер группы, которую хочешь удалить:\n'
            for lab in labs.labs:
                list_labs += f'\n{lab[0] + 1}. {lab[2]}'

            await bot.send_message(chat_id=user.id,
                                   text=list_labs,
                                   reply_markup=back_keyboard_without_callback(user).as_markup())
            user.action = 'admin->delete_science_group->get_id'
        else:
            if user.nickname == 'Nikatkavr':
                await callback.message.edit_media(
                    InputMediaPhoto(media=admin,
                                    caption='Нечего удалять, моя госпожа'),
                    reply_markup=admin_keyboard(user).as_markup())
            else:
                await callback.message.edit_media(
                    InputMediaPhoto(media=admin,
                                    caption='Нечего удалять, мой господин'),
                    reply_markup=admin_keyboard(user).as_markup())

    elif 'get_id' in user.action:
        try:
            group_id = int(message.text)

            if group_id not in [x[0] for x in labs.labs]:
                await bot.send_message(chat_id=user.id,
                                       text='Не вижу такого номера группы. Проверь ещё раз',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

            else:
                lab = Lab(id=group_id)
                if lab.delete_lab():
                    await bot.send_message(chat_id=user.id,
                                           text=f'Группа {lab.short_name} успешно удалена',
                                           reply_markup=back_keyboard_without_callback(user).as_markup())
                else:
                    await bot.send_message(chat_id=user.id,
                                           text='Что-то пошло не так',
                                           reply_markup=back_keyboard_without_callback(user).as_markup())
        except ValueError:
            await bot.send_message(chat_id=user.id,
                                   text=f'Не могу распознать число в твоём сообщении :(',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())


async def database_error_message(user: User, bot: Bot):
    await bot.send_message(chat_id=user.id,
                           text='Что-то не так с базой данных, не могу записать информацию. Попробуй ещё '
                                'раз или напиши @DelNick99',
                           reply_markup=back_keyboard_without_callback(user).as_markup())
