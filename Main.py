import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8906543011:AAE1MwSygdmOHXmPj3ELpUd502-m68ZB92M"

dp = Dispatcher()

# Asosiy menyu tugmalari
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👗 Ko'ylak zakaz berish", callback_data="dress")],
    [InlineKeyboardButton(text="🚚 Yetkazib berish", callback_data="delivery")],
    [InlineKeyboardButton(text="🕒 Ish vaqti", callback_data="work_time")]
])

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n"
        "Alex Home & Wear botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ =="__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
