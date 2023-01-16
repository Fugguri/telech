from main import dp, db
from aiogram import types
from utils.visualizer import create
dataset = {'period': ["Пн.", "Вт.", "Ср.", "Чт.", "Пт.", "Сб.", "Вс."],
           'team_B': [1, 3, 1, 0, 0, 1, 3],
           'team_C': [-1, -2, -0, -5, -1, 0, 0],
           }


@dp.message_handler(commands=["a"])
async def day_report(message: types.Message):
    events = db.user_event(message.from_id)
    for key in events:
        if events[key] == ():
            await message.answer(f"Non event in {key}")
        else:
            for event in events[key]:
                if event[6] != "2023-01-06":
                    # print(datetime.date.strptim(
                    #     str(event[6]), "YYYY-mm-dd"))
                    await message.answer(f"{key} event {event}")
                else:
                    return
    a = create(dataset)
    with open("out.png", "rb") as a:
        await message.answer_photo(photo=a)
