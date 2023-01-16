import logging
from aiogram import Bot, Dispatcher, executor
from config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db.DB_connector import Database


storage = MemoryStorage()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
py_handler = logging.FileHandler(f"logs/{__name__}.log", mode='w')
logger.addHandler(py_handler)
bot = Bot(TOKEN_API, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage,)
db = Database("TeleChurn")
message_id = {}


async def on_startup(_):
    print("Бот запущен")
    db.create_tables()


async def on_shutdown(_):
    print("Бот остановлен")


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        allowed_updates=["message", "callback_query", "chat_member"],
    )
