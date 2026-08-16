import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8906543011:AAE1MwSygdmOHXmPj3ELpUd502-m68ZB92M"

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Assalomu alaykum! Aiogram boti ishlayapti.")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
