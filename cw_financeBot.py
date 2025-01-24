import asyncio

# Bot отвечает за взаимодействие с Telegram bot API,
# а Dispatcher управляет обработкой входящих сообщений и команд
from aiogram import Bot, Dispatcher, F

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

# импортируем библиотеку логирования - ведение журнала событий для записи сообщений, событий или информации о работе программы
import logging
import requests
import random

from keyboards import keyboard
from config import TOKEN_CW

bot = Bot(token=TOKEN_CW)
dp = Dispatcher()

# настроим логирование - в скобках уровня логирования. Уровень info просто дает информацию о ходе выполнения работы программы.
# Есть другие уровни логирования, такие как debug, error, critical.
logging.basicConfig(level=logging.INFO)

# Создаем БД. id проставляется автоматически.
# в тройных кавычках пропишем действие с помощью запроса CREATE TABLE
conn = sqlite3.connect('user.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL)
''')
conn.commit()


# Чтобы запрашивать информацию и ждать ответа, нужно использовать состояния.
# Создаём класс, в котором будут прописаны эти состояния для каждой категории и каждого значения категории
class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я ваш личный финансовый помощник. Выберите одну из опций в меню!",
                         reply_markup=keyboard)


@dp.message(F.text == 'Регистрация в ТГ-боте')
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name

    cur.execute('''
    SELECT * FROM users WHERE telegram_id =?''', (telegram_id,))
    user = cur.fetchone()

    if user:
        await message.answer('Вы уже зарегистрированы!')
    else:
        cur.execute('''
        INSERT INTO users (telegram_id, name) VALUES (?,?)''', (telegram_id, name))
        conn.commit()
        await message.answer('Вы успешно зарегистрированы!')


# https://www.exchangerate-api.com/docs/overview
@dp.message(F.text == 'Курс валют')
async def exchange_rates(message: Message):
    url = 'https://v6.exchangerate-api.com/v6/d28c999c5a8bca892eefcbaa/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer('Не удалось получить данные о курсе валют!')
            return

        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']
        eur_to_rub = eur_to_usd * usd_to_rub

        await message.answer(f'1 USD - {usd_to_rub: .2f} RUB\n'
                             f'1 EUR - {eur_to_rub: .2f} RUB\n')

    except:
        await message.answer('Произошла ошибка!')


@dp.message(F.text == 'Советы по экономии')
async def send_tips(message: Message):
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам."
    ]
    tip = random.choice(tips)
    await message.answer(tip)


@dp.message(F.text == 'Личные финансы')
async def finances(message: Message):
    


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
