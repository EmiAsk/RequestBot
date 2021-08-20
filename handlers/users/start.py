from aiogram import types

from loader import dp
from data.messages import answers
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

from states.states import SubmitRequest


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    data = await state.get_data()
    if data.get('request_was_sent'):
        return
    keyboard.add(InlineKeyboardButton(text='Прочесть правила', callback_data='read_rules'))
    await message.answer(answers.read_rules.format(message.from_user.full_name),
                         reply_markup=keyboard)
    await SubmitRequest.first()