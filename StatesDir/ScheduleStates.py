from aiogram.dispatcher.filters.state import State, StatesGroup

class ScheduleStates(StatesGroup):
    wait_for_week_or_day = State()
