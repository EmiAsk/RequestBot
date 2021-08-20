from aiogram.dispatcher.filters.state import StatesGroup, State


class SubmitRequest(StatesGroup):
    read_rules = State()
    accept_rules = State()
    submit_request = State()
    from_where = State()
    profile_link = State()
    work_hours = State()
    scam_experience = State()
    confirm_request = State()