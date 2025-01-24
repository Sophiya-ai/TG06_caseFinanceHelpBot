#для создания клавиатур библиотеки
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

button_registr = KeyboardButton(text='Регистрация в ТГ-боте')
button_exchage_rates = KeyboardButton(text='Курс валют')
button_tips = KeyboardButton(text='Советы по экономии')
button_finances = KeyboardButton(text='Личные финансы')
button_db = KeyboardButton(text='Отображение всей базы данных')
keyboard = ReplyKeyboardMarkup(keyboard=[
            [button_registr, button_exchage_rates],
            [button_tips, button_finances],
            [button_db]
            ], resize_keyboard=True)