from main import dp, db
from aiogram import types
from utils.visualizer import create_plot_png
from utils.serializer import serializer

# dataset = {'period': [1, 2, 3, 4, 5, 6, 7],
#            'join': [1, 3, 1, 0, 0, 1, 3],
#            'left': [-1, -2, -0, -5, -1, 0, 0],
#            }


@dp.message_handler(commands=["a"])
async def day_report(message: types.Message):

    users_chat_or_channel_events = db.user_events(message.from_id)
    """ Временная функция для рассылки данных из обработчика """
    for chat_title in users_chat_or_channel_events:
        events = users_chat_or_channel_events[chat_title]
        dataset = await serializer(chat_title, events)
        """ ассанхронный mathplotlib???"""
        if "No events" not in dataset:
            create_plot_png(dataset[0])
            """Отправлять файл бинарником без сохранения?"""
            join = [i[1]for i in dataset[1]]
            left = [i[1]for i in dataset[2]]
            stray = [i[1]for i in dataset[3]]
           # вывод списка пользователей - настроить
            with open("out.png", "rb") as a:
                await message.answer_photo(photo=a, caption="""Отчет для: {}
                                           \nУшли: {}
                                           \nПрисоединились: {}
                                           \nНе остались: {}
                                           """.format(chat_title, join, left, stray))

        else:
            await message.answer("Нет событий для {}".format(chat_title))
