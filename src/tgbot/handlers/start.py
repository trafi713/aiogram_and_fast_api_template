from aiogram import types, Dispatcher


async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}")


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
