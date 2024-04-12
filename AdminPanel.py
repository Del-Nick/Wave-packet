import re

from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.enums import ParseMode
from aiogram import Bot
from Database import User, Lab
from numpy.random import randint
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
        # if 'Назад' in message.text:
        #     await bot.delete_message(chat_id=user.id, message_id=message.message_id)
        #     if user.nickname == 'Nikatkavr':
        #         await bot.send_photo(chat_id=user.id,
        #                              photo=admin,
        #                              caption='Возвращаю тебя в главное меню, моя госпожа',
        #                              reply_markup=admin_keyboard(user).as_markup())
        #     else:
        #         await bot.send_photo(chat_id=user.id,
        #                              photo=admin,
        #                              caption='Возвращаю тебя в главное меню, мой господин',
        #                              reply_markup=admin_keyboard(user).as_markup())
        #     user.action = 'admin->start'

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
        labs = AllLabs(user)
        if len(labs.labs) == 0:
            lab = Lab(full_name=message.text)
            if lab.add_new_lab():
                await bot.send_message(chat_id=user.id,
                                       text=f'Редактируем научную группу: {message.text}.\n\n'
                                            f'Введи короткое название научной группы, которое будет отображаться на '
                                            f'кнопках. Помни, что оно не должно превышать 64 символа, однако лучше '
                                            f'сделать его короче',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

                user.action = f'admin->add_science_group->add_short_name_id={lab.id}'

            else:
                await database_error_message(user, bot)

        elif message.text in [x[1] for x in labs.labs]:
            await bot.send_message(chat_id=user.id,
                                   text='Эта научная группа уже добавлена',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        else:
            lab = Lab(full_name=message.text)
            if lab.add_new_lab():
                await bot.send_message(chat_id=user.id,
                                       text=f'Редактируем научную группу: {message.text}.\n\n'
                                            f'Введи короткое название научной группы, которое будет отображаться на '
                                            f'кнопках. Помни, что оно не должно превышать 64 символа, однако лучше '
                                            f'сделать его короче',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

                user.action = f'admin->add_science_group->add_short_name_id={lab.id}'

            else:
                await database_error_message(user, bot)

    elif 'add_short_name' in user.action:
        # Названия в callback не запихать, слишком длинные. Ищем лабу по id
        lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))
        labs = AllLabs()

        if message.text in [x[2] for x in labs.labs]:
            await bot.send_message(chat_id=user.id,
                                   text='Такое короткое имя уже существует. Выбери другое',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())
        elif len(message.text) > 64:
            await bot.send_message(chat_id=user.id,
                                   text=f'В названии количество символов равно {len(message.text)}, а нужно не больше '
                                        f'64. Сократи, пожалуйста, название',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())
        else:
            lab.short_name = message.text
            if lab.update_lab():
                await bot.send_message(chat_id=user.id,
                                       text=f'Супер! Напиши callback-название, которое будет использоваться для '
                                            f'внутренней работы бота на английском языке по следующему образцу:\n\n'
                                            f'this_is_just_an_example\n\n'
                                            f'Название не должно превышать 40 символов и должно быть напрямую связано с '
                                            f'названием научное группы',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

                user.action = f'admin->add_science_group->add_callback_name_id={lab.id}'
            else:
                await database_error_message(user, bot)

    elif 'add_callback_name' in user.action:
        lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))
        labs = AllLabs()

        if message.text in [x[3] for x in labs.labs]:
            await bot.send_message(chat_id=user.id,
                                   text='Такое callback имя уже существует. Выбери другое',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        elif len(message.text) > 40:
            await bot.send_message(chat_id=user.id,
                                   text=f'В названии количество символов равно {len(message.text)}, а нужно не больше '
                                        f'40. Сократи, пожалуйста, название',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())

        else:
            lab.callback_name = message.text
            if lab.update_lab():
                await bot.send_message(chat_id=user.id,
                                       text='Отлично! Пришли мне картинку, которая будет отображаться на главной '
                                            'странице научной группы',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

                user.action = f'admin->add_science_group->add_main_picture_id={lab.id}'
            else:
                await database_error_message(user, bot)

    elif 'add_main_picture' in user.action:
        lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

        if message.photo is None:
            await bot.send_message(chat_id=user.id,
                                   text='Это точно картинка? Не могу её прочитать',
                                   reply_markup=back_keyboard_without_callback(user).as_markup())
        else:
            lab.main_picture = message.photo[-1].file_id
            if lab.update_lab():
                await bot.send_message(chat_id=user.id,
                                       text='Так, картинку сохранил. Теперь напиши описание научной группы. '
                                            'Пожалуйста, помни, что длинный текст большая часть пользователей читать '
                                            'не будет',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

                user.action = f'admin->add_science_group->add_about_id={lab.id}'

            else:
                await database_error_message(user, bot)

    elif 'add_about' in user.action:
        lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

        lab.about = message.text

        if lab.update_lab():
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

        else:
            await database_error_message(user, bot)

    elif 'add_areas' in user.action:
        lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))
        if callback:
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
            if 'Название:' not in message.text:
                await bot.send_message(chat_id=user.id,
                                       text='Не могу понять, где название. Не забывай оставлять кодовое слово перед '
                                            'названием:\n\n'
                                            '*Название:*',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='Markdown')

            elif 'Описание:' not in message.text:
                await bot.send_message(chat_id=user.id,
                                       text='Не могу понять, где описание. Не забывай оставлять кодовое слово перед '
                                            'описанием:\n\n'
                                            '*Описание:*',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='Markdown')

            elif 'Контакты:' not in message.text:
                await bot.send_message(chat_id=user.id,
                                       text='Не могу понять, где контакты. Не забывай оставлять кодовое слово перед '
                                            'контактами:\n\n'
                                            '*Контакты:*',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='Markdown')

            elif '\n\n\n' not in message.text or len(message.text.split('\n\n\n')) < 3:
                await bot.send_message(chat_id=user.id,
                                       text='Для меня очень важно, чтобы между пунктами было *__2 пустые__* строки\. '
                                            'Исправь, пожалуйста',
                                       reply_markup=back_keyboard_without_callback(user, button='Далее').as_markup(),
                                       parse_mode='MarkdownV2')

            else:
                _ = message.text.split('\n\n\n')
                data_to_paste = {'title': _[0].replace('Название:', ''),
                                 'about': _[1].replace('Описание:', ''),
                                 'contacts': _[2].replace('Контакты:', '')}
                if len(_) == 4:
                    data_to_paste['more'] = _[3].replace('Подробнее:', '')

                if type(lab.areas) is list:
                    lab.areas.append(data_to_paste)
                else:
                    lab.areas = [data_to_paste]

                if lab.update_lab():
                    await bot.send_message(chat_id=user.id,
                                           text=f'Записал. Теперь прикрепи фотографии *__по одной__*, сопровождая их '
                                                f'описанием',
                                           reply_markup=back_keyboard_without_callback(user,
                                                                                       button='Следующее '
                                                                                              'направление').as_markup(),
                                           parse_mode='MarkdownV2')
                    user.action = f'admin->add_science_group->add_picture_to_area_id={lab.id}'
                else:
                    await database_error_message(user, bot)

    elif 'add_picture_to_area' in user.action:
        lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

        if callback:
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
            if message.document is not None:
                await bot.send_message(chat_id=user.id,
                                       text='Прикрепляй изображение *__как картинку__* (со сжатием), а не как документ',
                                       reply_markup=back_keyboard_without_callback(user).as_markup(),
                                       parse_mode="MarkdownV2")

            elif message.photo is None:
                await bot.send_message(chat_id=user.id,
                                       text='Не вижу картинки. Ты не забыл её прикрепить?',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

            elif message.caption is None:
                await bot.send_message(chat_id=user.id,
                                       text='Прикрепи описание, чтобы было понятно, что изображено на картинке',
                                       reply_markup=back_keyboard_without_callback(user).as_markup())

            else:
                if 'pictures' in lab.areas[-1].keys():
                    lab.areas[-1]['pictures'].append({'picture': message.photo[-1].file_id,
                                                      'desc': message.caption})
                else:
                    lab.areas[-1]['pictures'] = [{'picture': message.photo[-1].file_id,
                                                  'desc': message.caption}]
                if lab.update_lab():
                    await bot.send_message(chat_id=user.id,
                                           text='Записал. Можешь отправить ещё картинки или перейти к следующему '
                                                'направлению',
                                           reply_markup=back_keyboard_without_callback(user,
                                                                                       button='Следующее направление').as_markup())
                else:
                    await database_error_message(user, bot)

    elif 'add_contacts' in user.action:
        lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

        # Своего рода костыль. Чтобы не переходить к следующему этапу, если пользователь прислал неправильно оформленный
        # текст
        success = False

        if callback:
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
            if '\n\n' in message.text:
                for human in message.text.split('\n\n'):
                    if len(human.split('\n')) != 3:
                        await bot.send_message(chat_id=user.id,
                                               text=f'Возникла проблема с этим человеком:\n {human}\. Проверь, все ли '
                                                    f'правила соблюдены\n\n'
                                                    ''
                                                    '*Название*\n'
                                                    '*Научный руководитель*\n'
                                                    '*Контакт научного руководителя*\n\n',
                                               reply_markup=back_keyboard_without_callback(user).as_markup(),
                                               parse_mode='MarkdownV2')
                        break
                    else:
                        _ = human.split('\n')
                        data_to_paste = {'title': _[0],
                                         'teacher': _[1],
                                         'contact': _[2]}
                        if lab.contacts is None:
                            lab.contacts = [data_to_paste]
                        else:
                            lab.contacts.append(data_to_paste)

                        success = True
            else:
                if len(message.text.split('\n')) != 3:
                    await bot.send_message(chat_id=user.id,
                                           text=r'Возникла проблема с текстом\. Проверь, все ли '
                                                'правила соблюдены\n\n'
                                                ''
                                                '*Название*\n'
                                                '*Научный руководитель*\n'
                                                '*Контакт научного руководителя*\n\n',
                                           reply_markup=back_keyboard_without_callback(user).as_markup(),
                                           parse_mode='MarkdownV2')
                else:
                    _ = message.text.split('\n')
                    data_to_paste = {'title': _[0],
                                     'teacher': _[1],
                                     'contact': _[2]}
                    if lab.contacts is None:
                        lab.contacts = [data_to_paste]
                    else:
                        lab.contacts.append(data_to_paste)

                    success = True

            if success:
                if lab.update_lab():
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
            lab = Lab(id=int(re.search(r'id=\d{1,2}', user.action).group().replace('id=', '')))

            if '\n\n' in message.text:
                for coursework in message.text.split('\n\n'):
                    _ = coursework.split('\n')
                    if len(_) < 3:
                        _ = '\n'.join(_)
                        await bot.send_message(chat_id=message.chat.id,
                                               text=f'Непорядок с этими строчками:\n\n'
                                                    f'{_}\n\n'
                                                    f'Их и всё, что ниже, я вставить не могу. Исправь и пришли заново. '
                                                    f'Напоминаю о шаблоне:\n\n'
                                                    f'*Название*\n'
                                                    f'*Научный руководитель*\n'
                                                    f'*Контакты*',
                                               reply_markup=back_keyboard_without_callback(user,
                                                                                           button='Завершить').as_markup(),
                                               parse_mode='Markdown')
                        break

                    else:
                        _ = {'title': _[0],
                             'teacher': _[1],
                             'contact': _[2]}

                        lab.courseworks = [_] if lab.courseworks is None else lab.courseworks.apend(_)

                        if lab.update_lab():
                            await bot.send_message(chat_id=message.chat.id,
                                                   text=f'Добавил курсовую:\n\n'
                                                        f'*Название:*    {_["title"]}\n\n'
                                                        f'*Научный руководитель:*    {_["teacher"]}\n\n'
                                                        f'*Контакты:*   {_["contact"]}',
                                                   reply_markup=back_keyboard_without_callback(user,
                                                                                               button='Завершить').as_markup())
                        else:
                            await database_error_message(user, bot)

            else:
                _ = message.text.split('\n')
                if len(_) < 3:
                    _ = '\n'.join(_)
                    await bot.send_message(chat_id=message.chat.id,
                                           text=f'Непорядок с этими строчками:\n\n'
                                                f'{_}\n\n'
                                                f'Их и всё, что ниже я вставить не могу. Исправь и пришли заново. '
                                                f'Напоминаю о шаблоне:\n\n'
                                                f'*Название*\n'
                                                f'*Научный руководитель*\n'
                                                f'*Контакты*',
                                           reply_markup=back_keyboard_without_callback(user,
                                                                                       button='Завершить').as_markup(),
                                           parse_mode='Markdown')
                else:
                    _ = {'title': _[0],
                         'teacher': _[1],
                         'contact': _[2]}

                    lab.courseworks = [_] if lab.courseworks is None else lab.courseworks.apend(_)

                    if lab.update_lab():
                        await bot.send_message(chat_id=message.chat.id,
                                               text=f'Добавил курсовую:\n\n'
                                                    f'*Название:*    {_["title"]}\n\n'
                                                    f'*Научный руководитель:*    {_["teacher"]}\n\n'
                                                    f'*Контакты:*   {_["contact"]}',
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
