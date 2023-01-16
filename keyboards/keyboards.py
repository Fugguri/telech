from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def back(language):
    if language == "ru":
        back = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Назад", callback_data="back"))
    else:
        back = back = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Back", callback_data="back"))
    return back


def wellcome_kb(language):
    wellcome = InlineKeyboardMarkup(row_width=3)
    if language == "ru":
        wellcome.add(InlineKeyboardButton(
            text="Помощь", callback_data="help")).add(InlineKeyboardButton(
                text="Добавить чат", callback_data="add chat")).add(InlineKeyboardButton(
                    text="О проекте", callback_data="about"))
    else:
        wellcome.add(InlineKeyboardButton(
            text="Help", callback_data="help")).add(InlineKeyboardButton(
                text="Add chat", callback_data="add chat")).add(InlineKeyboardButton(
                    text="About", callback_data="about"))
    return wellcome
