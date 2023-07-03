from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy import func
from models import Users, Incomes, Consumptions
from states import Form
from db_map import Session
from keyboards import main_kbd, start_kbd
from utils import check_if_integer, check_user_exists


async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await check_user_exists(user_id):
        await message.answer("You're already registered", reply_markup=main_kbd)
        await state.reset_state()
    else:
        await state.update_data(ID=user_id)
        await state.set_state(Form.ID)
        print(f"[ log ] {user_id}, started registration")
        await message.answer("Enter your capital: ")

async def set_capital(message: types.Message, state: FSMContext):
    await check_if_integer(message, state, "capital")
    data = await state.get_data()
    ID = data.get('ID')
    new_user = Users(UId=ID, capital=data['capital'])
    with Session() as session:
        session.add(new_user)
        session.commit()
    await state.reset_data()
    await state.reset_state()
    print(f"[ log ] Successfully created data {ID}, with capital {data['capital']}")
    await message.answer("Successful!", reply_markup=main_kbd)


async def income_handler(message: types.Message, state: FSMContext):
    await message.answer("Enter your income:", reply_markup=types.ReplyKeyboardRemove(True))
    await state.set_state(Form.Income)


async def reason_handler1(message: types.Message, state: FSMContext):
    try:
        Income = int(message.text)
    except ValueError:
        await message.answer("Income must be an integer. Please try again:")
        return
    await state.update_data(Income=Income)
    with Session() as session:
        user = session.query(Users).filter_by(UId=message.from_user.id).first()
        user.capital += Income
        print(f"[ log ] Successfully updated {message.from_user.id}'s capital and income")
        await message.answer(f"Your new Income: {Income}\nYour new capital: {user.capital}", reply_markup=main_kbd)
        session.add(Incomes(sum=Income, UId=message.from_user.id))
        session.commit()
    await state.reset_data()
    await state.reset_state()


async def consumption_handler(message: types.Message, state: FSMContext):
    await message.answer("Enter your consumption:", reply_markup=types.ReplyKeyboardRemove(True))
    await state.set_state(Form.Consumption)


async def reason_handler(message: types.Message, state: FSMContext):
    try:
        consumption = int(message.text)
    except ValueError:
        await message.answer("Consumption must be an integer. Please try again:")
        return
    await state.update_data(Consumption=consumption)
    await message.answer("What's the reason for this consumption?")
    await Form.Reason.set()


async def reason_handler2(message: types.Message, state: FSMContext):
    reason = message.text
    data = await state.get_data()
    consumption = data.get('Consumption')
    with Session() as session:
        user = session.query(Users).filter_by(UId=message.from_user.id).first()
        print(user.capital)
        print(consumption)
        if user.capital is None:
            user.capital = 0
        if int(user.capital) < consumption:
            await message.answer("You don't have enough money for this consumption", reply_markup=main_kbd)
        else:
            user.capital -= consumption
            session.add(Consumptions(sum=consumption, reason=reason, UId=message.from_user.id))
            session.commit()
            print(f"[ log ] {user.UId} have spent {consumption}, updated {user.capital} and reason is {reason}")
            await message.answer(f"You have spent {consumption}. Your new capital is {user.capital}", reply_markup=main_kbd)
    await state.reset_data()
    await state.reset_state()


async def show_consumptions(message: types.Message):
    user_id = message.from_user.id
    with Session() as session:

        consumption_query = session.query(
            func.date(Consumptions.data).label("day"),
            func.sum(Consumptions.sum).label("total"),
            func.avg(Consumptions.sum).label("average")
        ).filter_by(UId=user_id).group_by("day").all()

        if not consumption_query:
            await message.answer("You don't have any consumptions yet", reply_markup=main_kbd)
            return

        total_consumption = sum(row.total for row in consumption_query)
        consumption_count = len(consumption_query)

        response = "Your consumptions:\n"
        for consumption in consumption_query:
            response += f"Date: {consumption.day}, Total: {consumption.total}, Average: {consumption.average}\n"

        average_consumption = total_consumption / consumption_count

        response += f"\nTotal consumption: {total_consumption}\nAverage consumption: {average_consumption}"

        await message.answer(response, reply_markup=main_kbd)


async def show_incomes(message: types.Message):
    user_id = message.from_user.id
    with Session() as session:
        income_query = session.query(
            func.date(Incomes.data).label("day"),
            func.sum(Incomes.sum).label("total"),
            func.avg(Incomes.sum).label("average")
        ).filter_by(UId=user_id).group_by("day").all()

        if not income_query:
            await message.answer("You don't have any incomes yet", reply_markup=main_kbd)
            return

        response = "Your incomes:\n"
        for income in income_query:
            response += f"Date: {income.day}, Total: {income.total}, Average: {income.average}\n"

        await message.answer(response, reply_markup=main_kbd)

async def show_capital(message: types.Message):
    user_id = message.from_user.id
    with Session() as session:
        capital = session.query(Users.capital).filter_by(UId=user_id).first()[0]
        if not capital:
            await message.answer("Your capital is 0")
            return
        await message.answer(f"your capital is: {capital}")