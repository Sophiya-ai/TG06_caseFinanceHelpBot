#для создания клавиатур библиотеки
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

button_registr = KeyboardButton(text='Регистрация в ТГ-боте')
button_exchage_rates = KeyboardButton(text='Курс валют')
button_tips = KeyboardButton(text='Советы по экономии')
button_finances = KeyboardButton(text='Личные финансы')
keyboard = ReplyKeyboardMarkup([
            [button_registr, button_exchage_rates],
            [button_tips, button_finances]
            ], resize_keyboard=True)