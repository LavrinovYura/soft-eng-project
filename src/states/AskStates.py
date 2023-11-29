from aiogram.dispatcher.filters.state import State, StatesGroup


class AskStates(StatesGroup):
    waiting_for_question = State()
    did_you_get_the_right_answer = State()
    did_you_get_the_right_answer_after_top = State()
