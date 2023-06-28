from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_btn = [
    KeyboardButton("let's go"),
    KeyboardButton("No")
]

start_kbd = ReplyKeyboardMarkup(resize_keyboard=True).row(*start_btn)

main_btns = [
    KeyboardButton("Consumption"),
    KeyboardButton("Income"),
    KeyboardButton("Show consumptions"),
    KeyboardButton("Show incomes"),
    KeyboardButton("Show capital"),
]

main_kbd = ReplyKeyboardMarkup(resize_keyboard=True).row(*main_btns)