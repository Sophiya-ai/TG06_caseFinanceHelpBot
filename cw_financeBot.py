import asyncio

# Bot отвечает за взаимодействие с Telegram bot API,
# а Dispatcher управляет обработкой входящих сообщений и команд
from aiogram import Bot, Dispatcher

# импорт для отслеживания каких-либо команд в Telegram-боте. Обычно первая команда — это start.
# Чтобы отслеживать команды, нужно импортировать фильтры и типы сообщений
# FSInputFile необходим для обработки файлов и их отправки в aiogram
from aiogram.filters import CommandStart
from aiogram.types import Message

# работа с базами данных
import sqlite3

# для сохранения контекста между сообщениями, чтобы сохранять информацию между запросами и использовать ее,
# например, в базе данных.
from aiogram.fsm.context import FSMContext

# импортируем библиотеку для работы с состояниями (для работы с информацией, передаваемой пользователем).
# класс State для работы с отдельными состояниями пользователей
# и StatesGroup для группировки состояний
from aiogram.fsm.state import State, StatesGroup

# импортируем библиотеку для сохранения состояния в оперативной памяти
from aiogram.fsm.storage.memory import MemoryStorage

# библиотека — IOHTTP для выполнения асинхронных HTTP-запросов.
# бот будет подключаться к API прогнозов погоды и выдавать прогноз для конкретного пользователя, город которого будет записан в БД
import aiohttp

# импортируем библиотеку логирования - ведение журнала событий для записи сообщений, событий или информации о работе программы
import logging

#для создания клавиатур библиотеки
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import TOKEN_CW, API_KEY

bot = Bot(token=TOKEN_CW)
dp = Dispatcher()

# настроим логирование - в скобках уровня логирования. Уровень info просто дает информацию о ходе выполнения работы программы.
# Есть другие уровни логирования, такие как debug, error, critical.
logging.basicConfig(level=logging.INFO)





# асинхронная функция main, которая будет запускаться и работать одновременно со всем остальным.
# await здесь — это действие, которое происходит с Telegram-ботом, и
# будет запускаться действие dp.start_polling: в этом случае программа будет отправлять запрос в Telegram,
# проверяя, есть ли входящие сообщения и произошедшие события.
# Если события есть, программа их “отлавливает”.
# В отсутствие событий функция продолжает отправлять запросы и ждет, когда событие произойдет,
# чтобы с этим можно было начать работать
async def main():
    await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(main())
asyncio.run(main())
# пишем здесь не просто run(main), потому что функция здесь асинхронная,
# ее нужно запускать определенным образом, указывая при этом,
# какую именно функцию мы хотим запустить