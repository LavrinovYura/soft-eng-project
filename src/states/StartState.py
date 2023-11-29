from aiogram.dispatcher.filters.state import State, StatesGroup


class StartState(StatesGroup):
    waiting_for_group_id = State()
