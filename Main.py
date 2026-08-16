import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Tokeningizni qo'shtirnoq ichiga yozasiz
TOKEN = "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"

dp = Dispatcher()

# Asosiy menyu tugmalari
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👗 Ko'ylak zakaz berish", callback_data="dress")],
    [InlineKeyboardButton(text="🚚 Yetkazib berish", callback_data="delivery")],
    [InlineKeyboardButton(text="⏰ Ish vaqti", callback_data="work_time")]
])

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n"
        "Alex Home & Wear botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )

@dp.callback_query(F.data == "dress")
async def dress_handler(callback: CallbackQuery):
    text = (
        "<b>👗 Ko'ylak zakaz berish:</b>\n"
        "Siz istagan modeldagi kiyim-kechaklarni shaxsiy o'lchamlaringiz "
        "asosida professional tarzda tikib beramiz.\n\n"
        "Buyurtma uchun: @Ali_tex1"
    )
    await callback.message.answer(text, parse_mode=ParseMode.HTML, reply_markup=main_menu)
    await callback.answer()

@dp.callback_query(F.data == "delivery")
async def delivery_handler(callback: CallbackQuery):
    text = (
        "<b>🚚 Yetkazib berish shartlari:</b>\n"
        "<b>• Pardalar:</b> Qo'qon shahar va atrofdagi tumanlar bo'ylab o'lcham "
        "olish va o'rnatib berish xizmatlari bilan.\n"
        "<b>• Kiyim-kechaklar:</b> O'zbekiston Respublikasi bo'ylab barcha "
        "viloyatlarga pochta orqali yetkazib beriladi."
    )
    await callback.message.answer(text, parse_mode=ParseMode.HTML, reply_markup=main_menu)
    await callback.answer()

@dp.callback_query(F.data == "work_time")
async def work_time_handler(callback: CallbackQuery):
    text = (
        "<b>⏰ Ish vaqti:</b>\n"
        "<b>• Telegram bot:</b> 24/7 (Kechayu kunduz avtomat ishlaydi)\n"
        "<b>• Menejer va guruhlar:</b> Har kuni 09:00 dan 20:00 gacha buyurtmalar qabul qilinadi."
    )
    await callback.message.answer(text, parse_mode=ParseMode.HTML, reply_markup=main_menu)
    await callback.answer()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if name == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
