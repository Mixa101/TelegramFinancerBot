from aiogram.dispatcher.filters.state import StatesGroup, State

class Form(StatesGroup):
    ID = State()
    capital = State()
    Income = State()
    Consumption = State()
    Reason = State()