from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from models import Base
from db_map import engine
from handlers import (
    start_handler,
    set_capital,
    income_handler,
    reason_handler,
    reason_handler1,
    reason_handler2,
    consumption_handler,
    show_consumptions,
    show_incomes,
    show_capital,
)
from config import TOKEN, DB_FILENAME
from keyboards import start_kbd
from states import Form
import os

# Инициализация Telegram Bot
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


if not os.path.isfile(f"./{DB_FILENAME}"):
    Base.metadata.create_all(engine)

# Регистрация хэндлеров
dp.register_message_handler(start_handler, commands=['start'])
dp.register_message_handler(set_capital, state=Form.ID)
dp.register_message_handler(income_handler, Text(equals="Income"))
dp.register_message_handler(reason_handler1, state=Form.Income)
dp.register_message_handler(consumption_handler, Text(equals="Consumption"))
dp.register_message_handler(reason_handler, state=Form.Consumption)
dp.register_message_handler(reason_handler2, state=Form.Reason)
dp.register_message_handler(show_consumptions, Text(equals="Show consumptions"))
dp.register_message_handler(show_incomes, Text(equals="Show incomes"))
dp.register_message_handler(show_capital, Text(equals="Show capital"))

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
