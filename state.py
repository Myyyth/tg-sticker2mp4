from aiogram.dispatcher.filters.state import StatesGroup, State


class StickerUpload(StatesGroup):
    color = State()
