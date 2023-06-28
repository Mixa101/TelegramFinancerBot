from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from db_map import Session
from models import Users

async def check_if_integer(message: types.Message, state: FSMContext, data_key: str):
    try:
        data = int(message.text)
    except:
        await message.answer(f"{data_key.capitalize()} must be integer, try again", reply_markup=ReplyKeyboardRemove(True))
        return
    await state.update_data({data_key: data})

async def check_user_exists(user_id: int) -> bool:
    session = Session()
    user = session.query(Users).filter_by(UId = user_id).first()
    session.close()
    return bool(user)
