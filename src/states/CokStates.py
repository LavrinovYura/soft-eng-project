from aiogram.dispatcher.filters.state import State, StatesGroup


class CokStates(StatesGroup):
    waiting_for_fio = State()
    waiting_for_mail = State()
    waiting_for_question = State()
    confirm_sending = State()
