from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from loader import dp, bot
from data.messages import answers
from states.states import SubmitRequest
from data.config import ADMIN


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.callback_query_handler(text='read_rules', state=SubmitRequest.read_rules)
async def get_rules_read(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Принять правила', 'accept_rules'))
    await call.message.edit_text(answers.rules, reply_markup=keyboard)
    await call.answer()
    await SubmitRequest.accept_rules


@dp.callback_query_handler(text='accept_rules', state=SubmitRequest.accept_rules)
async def get_rules_accepted(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Подать заявку', 'submit_request'))

    await call.message.edit_text(answers.give_request, reply_markup=keyboard)
    await call.answer()
    await SubmitRequest.submit_request.set()


@dp.callback_query_handler(text='submit_request', state=SubmitRequest.submit_request)
async def get_request_submitted(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Друзья', 'from_friends'))
    keyboard.add(InlineKeyboardButton('Реклама', 'from_adv'))
    keyboard.add(InlineKeyboardButton('LOLZTEAM', 'from_lolz'))

    await call.message.edit_text(answers.where_was_found_out, reply_markup=keyboard)
    await call.answer()
    await SubmitRequest.from_where.set()


@dp.callback_query_handler(text=['from_friends', 'from_adv', 'from_lolz'], state=SubmitRequest.from_where)
async def get_from_where(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['where_was_it_found_out'] = call.data
    await call.message.edit_text(answers.profile_link)
    await call.answer()
    await SubmitRequest.profile_link.set()


@dp.message_handler(state=SubmitRequest.profile_link)
async def get_profile_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['profile_link'] = message.text

    await message.answer(answers.work_hours)
    await SubmitRequest.work_hours.set()


@dp.message_handler(state=SubmitRequest.work_hours)
async def get_work_hours(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['work_hours'] = message.text

    await message.answer(answers.scam_experience)
    await SubmitRequest.scam_experience.set()


@dp.message_handler(state=SubmitRequest.scam_experience)
async def get_scam_experience(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['scam_exp'] = message.text

    data = await state.get_data()

    keyboard = InlineKeyboardMarkup()
    keyboard.insert(InlineKeyboardButton('Отправить заявку', 'send_request'))
    keyboard.insert(InlineKeyboardButton('Заполнить заново', 'fill_in_again'))
    await message.answer(answers.request_info.format(from_where=data['where_was_it_found_out'],
                                                     profile_link=data['profile_link'],
                                                     work_hours=data['work_hours'],
                                                     experience=data['scam_exp']), reply_markup=keyboard)
    await SubmitRequest.confirm_request.set()


@dp.callback_query_handler(text='fill_in_again', state=SubmitRequest.confirm_request)
async def fill_request_in_again(call: CallbackQuery, state: FSMContext):
    await state.reset_data()
    await SubmitRequest.submit_request.set()
    await get_request_submitted(call, state)


@dp.callback_query_handler(text='send_request', state=SubmitRequest.confirm_request)
async def send_request(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    keyboard = InlineKeyboardMarkup()
    keyboard.insert(InlineKeyboardButton('Принять', 'admin:accept_request:' + user_id))
    keyboard.insert(InlineKeyboardButton('Отклонить', 'admin:reject_request:' + user_id))
    await bot.send_message(ADMIN,
                           answers.new_request.format(user_id) + answers.request_info.format(
                               from_where=data['where_was_it_found_out'],
                               profile_link=data['profile_link'],
                               work_hours=data['work_hours'],
                               experience=data['scam_exp']),
                           reply_markup=keyboard)

    await call.message.edit_text(answers.request_was_sent)
    await call.answer()
    await state.reset_state(with_data=True)

    async with state.proxy() as data:
        data['request_was_sent'] = True


@dp.callback_query_handler(text_contains='admin:accept_request')
async def admin_accept_request(call: CallbackQuery):
    user_id = int(call.data.split(':')[-1])

    await call.message.edit_text(answers.admin_request_accepted.format(user_id))
    await bot.send_message(user_id, answers.request_accepted)
    await call.answer()


@dp.callback_query_handler(text_contains='admin:reject_request')
async def admin_request_rejected(call: CallbackQuery):
    user_id = int(call.data.split(':')[-1])

    await call.message.edit_text(answers.admin_request_rejected.format(user_id))
    await bot.send_message(user_id, answers.request_rejected)
    user_state = dp.current_state(user=user_id)

    async with user_state.proxy() as data:
        data['request_was_confirmed'] = True

    await call.answer()
