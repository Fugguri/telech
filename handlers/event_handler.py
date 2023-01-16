from main import dp, bot, logger, db
from aiogram import types
import datetime


@dp.chat_member_handler()
async def some_handler(chat_member: types.ChatMemberUpdated):
    chat_id = chat_member.chat.id
    subs_amount = await bot.get_chat_member_count(chat_id)
    user_id = chat_member.from_user.id
    username = chat_member.from_user.username
    full_name = chat_member.from_user.full_name
    status = chat_member.new_chat_member.status
    date = str(datetime.date.today())
    db.add_event(chat_id, user_id, username,
                 full_name, status, date, subs_amount)
