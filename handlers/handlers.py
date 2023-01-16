from main import dp, message_id, logger, db
from aiogram import types
from keyboards.keyboards import wellcome_kb, back


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    language = message.from_user.language_code.strip()
    message_id[message.from_user.id] = message.message_id
    logger.debug(
        f"{message.from_user}Нажал старт, пользователь занесен в базу данных")
    telegram_id = message.from_id
    username = message.from_user.username
    full_name = message.from_user.full_name
    db.create_user(telegram_id, full_name, username)
    await message.delete()
    if language == "ru":
        wellcome_text = "Добро пожаловать!"
    else:
        wellcome_text = "Wellcome"
    await message.answer(wellcome_text, reply_markup=wellcome_kb(language=language))


@dp.callback_query_handler(lambda call: call.data == "help")
async def help(callback: types.CallbackQuery):
    language = callback.message.from_user.language_code
    await callback.message.edit_text("Тут будет хелп", reply_markup=back(language))


@dp.callback_query_handler(lambda call: call.data == "about")
async def about(callback: types.CallbackQuery):
    logger.debug(f"{callback.from_user}Кнопка about")
    language = callback.message.from_user.language_code
    await callback.message.edit_text("Тут будет о проекте", reply_markup=back(language))


@dp.callback_query_handler(lambda call: call.data == "back")
async def add_chat_back(callback: types.CallbackQuery):
    logger.debug(f"{callback.from_user}Кнопка назад из основного меню")
    language = callback.message.from_user.language_code
    if language == "ru":
        wellcome_text = "Добро пожаловать!"
        await callback.message.edit_text(wellcome_text, reply_markup=wellcome_kb(language=language))
    else:
        wellcome_text = "Wellcome"
        await callback.message.edit_text(wellcome_text, reply_markup=wellcome_kb(language=language))


@dp.message_handler(commands=["logs"])
async def start(message: types.Message):
    logger.debug(f"{message.from_user}Получить логи")
    with open("logs/main.log", "r") as logs:
        try:
            await message.answer("Ваши логи,хозяин")
            await message.answer_document(document=logs)
        except:
            await message.answer("Логи пусты")
