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
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.reply("Введите первую категорию расходов:")


@dp.message(FinancesForm.category1)
async def cat1(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.reply(f"Введите расходы для категории <{message.text}>:")


@dp.message(FinancesForm.expenses1)
async def exp1(message: Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.reply(f"Введите вторую категорию расходов:")


@dp.message(FinancesForm.category2)
async def cat2(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.reply(f"Введите расходы для категории <{message.text}>:")


@dp.message(FinancesForm.expenses2)
async def exp2(message: Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.reply(f"Введите третью категорию расходов:")


@dp.message(FinancesForm.category3)
async def cat3(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.reply(f"Введите расходы для категории <{message.text}>:")


@dp.message(FinancesForm.expenses3)
async def exp3(message: Message, state: FSMContext):
    await state.update_data(expenses3=float(message.text))
    data = await state.get_data()
    telegram_id = message.from_user.id
    cur.execute('''
    UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, category3 = ?, expenses3 = ? 
     WHERE telegram_id = ?''',
                (data['category1'], data['expenses1'], data['category2'], data['expenses2'],
                 data['category3'], data['expenses3'], telegram_id)
                )
    conn.commit()
    await state.clear()

    await message.answer('Категории и расходы по ним сохранены')


@dp.message(F.text == 'Отображение всей базы данных')
async def db(message: Message):
    cur.execute('''SELECT * FROM users''')
    users = cur.fetchall()
    if users:
        # создаем строку `response`, которая будет содержать текст "Студенты в группе 'название_группы':\n".
        # Метод `.format()` – это метод строк, используется для форматирования строк и позволяет вставлять
        # значения в строку в обозначенные места
        response = "Содержимое БД:\n\n"
        # Далее для каждого студента мы добавляем строку в `response`, содержащую его имя и возраст
        for user in users:
            response += (f"Имя: {user[2]}\n"
                         f"Категория 1: {user[3]} (расходы - {user[6]})\n"
                         f"Категория 2: {user[4]} (расходы - {user[7]})\n"
                         f"Категория 3: {user[5]} (расходы - {user[8]})\n")
    else:
        response = "В БД нет записей"

        # Отправляем ответное сообщение
    await message.answer(response)


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
