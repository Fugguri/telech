import datetime

"""Rebuild CLASS-BASED serializer"""

"""Количетсво подписчиков для отсчета жизненного цикла
    Берем первую дату, собития в канале, или дату присоединения пользователя.  И если пользователь вышел - вызываем.
    Вынести в отдельную функцию!!!"""
subs_amount_for_life_cycle = int()
date_for_life_cycle = ""


async def serializer(chat_title: str, events: list):
    """stray_list для дальнейшей обработки количества залетных пользователей.
       Они пришли, значи заинтересованы, но что-то в этот раз их оттолкнуло и при следующей рекламе весьма вероятно их зацепить."""
    today = datetime.date.today()
    result = dict()
    result["period"] = [datetime.date.strftime(
        today - datetime.timedelta(days=i), "%m.%d") for i in range(6, -1, -1)]
    result["left"] = [0, 0, 0, 0, 0, 0, 0]
    result["join"] = [0, 0, 0, 0, 0, 0, 0]
    week_end = datetime.date.today() - datetime.timedelta(days=6)
    # Users lists
    departed_list = list()
    remained_list = list()
    stray_list = list()  # Дописать обработку залетных
    # User events counters
    remained_count = int()
    departed_count = int()
    stray_count = int()
    """Работа функции будет настроена на опеределенный день?
       Если на определенный день, то рассылка будет считать с начала недели и собирать данные.
       (предусмотрен ли запрос в течении недели, с отрисовкой графика???) """
    if events == ():
        return f"No events for {chat_title}"
    else:
        for event in events:
            username = event[2]
            full_name = event[3]
            status = event[4]
            date = event[5]
            str_date = datetime.date.strftime(date, "%m.%d")
            subs_amount = event[6]
            user_data = [username, full_name, date]
            day_index = result["period"].index(str_date)
            if week_end < date:  # проверка даты события
                if status == "member":
                    if user_data not in departed_list:
                        remained_list.append(user_data)
                        result["join"][day_index] += 1
                    else:
                        stray_list.append(user_data)
                        stray_count += 1
                        departed_list.remove(user_data)
                        result["left"][day_index] -= 1
                if status == "left":
                    if user_data not in remained_list:
                        departed_list.append(user_data)
                        result["left"][day_index] -= 1
                    else:
                        stray_list.append(user_data)
                        stray_count += 1
                        remained_list.remove(user_data)
                        result["join"][day_index] -= 1
            else:
                break
            """ Не хватает всех вариантов нахождения в списках
                Если пользователь в списке залетных, но присоединился и не вышел, добавляем в список присоединившихся"""
    return [result, departed_list, remained_list, stray_list]
    # return {"chat_title": chat_title, "departed_count": departed_count, "remained_count": remained_count, "stray_count": stray_count}
