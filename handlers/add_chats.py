from main import dp, bot, message_id, logger, db
from aiogram import types
from keyboards.keyboards import wellcome_kb, back
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddChat(StatesGroup):
    add_chat_link = State()


@dp.callback_query_handler(lambda call: call.data == "add chat")
async def add_chat(callback: types.CallbackQuery):
    logger.debug(f"{callback.from_user}добавить чат")
    language = callback.message.from_user.language_code
    await AddChat.add_chat_link.set()
    try:
        chats = "Список чатов:\n" + \
            "\n".join(db.all_chats(callback.from_user.id))
    except:
        chats = ""
    await callback.message.edit_text('Введите ссылку на чат \nФормат "t.me/linkonyourchat"'+f"\n{chats}", reply_markup=back(language), disable_web_page_preview=True)
    message_id[callback.from_user.id] = {
        'message_id': callback.message.message_id, 'chat_id': callback.message.chat.id, "chats": []}


@dp.callback_query_handler(lambda call: call.data == "back", state=AddChat.add_chat_link)
async def add_chat_back(callback: types.CallbackQuery, state: State):
    await state.finish()
    logger.debug(f"{callback.from_user}Назад из добавить чат")
    language = callback.message.from_user.language_code
    if language == "ru":
        wellcome_text = "Добро пожаловать!"
        await callback.message.edit_text(wellcome_text, reply_markup=wellcome_kb(language=language))
    else:
        wellcome_text = "Wellcome"
        await callback.message.edit_text(wellcome_text, reply_markup=wellcome_kb(language=language))


@ dp.message_handler(state=AddChat.add_chat_link)
async def chat_link(message: types.Message):
    from aiogram.utils.exceptions import MessageNotModified
    try:
        language = message.from_user.language_code
        l = "@" + message.text.replace("https://t.me/", "")
        chat_info = await bot.get_chat(l)
        chat_subs = await bot.get_chat_members_count(l)
        chat_id = chat_info.id
        chat_title = chat_info.title
        chat_username = chat_info.username
        telegram_id = message.from_user.id
        if "t.me/" in message.text:
            db.add_chat(telegram_id=telegram_id,
                        chat_link=message.text,
                        chat_num=chat_id,
                        chat_name=chat_title,
                        chat_subs_amount=chat_subs
                        )
            chats = "Список чатов:\n" + \
                "\n".join(db.all_chats(telegram_id))
            await message.delete()
            await bot.edit_message_text(message_id=message_id[message.from_user.id]['message_id'],
                                        chat_id=message_id[message.from_user.id]['chat_id'],
                                        text=chats,
                                        reply_markup=back(language),
                                        disable_web_page_preview=True)
            logger.debug(f"{message.from_user} Добавлен чат {message.text}")
        else:
            try:
                chats = message_id[message.from_user.id]["chats"]
                chats = "Список чатов:\n" + "\n".join(chats)
            except:
                chats = ""
            logger.debug(f"{message.from_user} Плохая ссылка! {message.text}")
        # await message.delete()
        await bot.edit_message_text(message_id=message_id[message.from_user.id]['message_id'],
                                    chat_id=message_id[message.from_user.id]['chat_id'],
                                    text='Введите ссылку на чат\nФормат "t.me/linkonyourchat"' +
                                    f"\nВаши чаты:\n{chats}",
                                    reply_markup=back(language),
                                    disable_web_page_preview=True)
    except MessageNotModified:
        # await message.delete()
        pass
