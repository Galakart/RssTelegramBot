from aiogram.fsm.state import State, StatesGroup


class NewFeedState(StatesGroup):
    ask_newfeed_link = State()
    ask_newfeed_customtitle = State()
