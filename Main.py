import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

TOKEN = "8906543011:AAH8e... (o'zingizning tokeningiz)" # Tokeningizni o'rniga qo'yasiz

dp = Dispatcher()

# Asosiy menyu tugmalari
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛍 Mahsulotlar katalogi", callback_data="catalog")],
    [InlineKeyboardButton(text="❓ Savol-javoblar", callback_data="faq")],
    [InlineKeyboardButton(text="📞 Biz bilan aloqa", callback_data="contact")]
])

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        "<b>Biz bilan bog'lanish:</b>\n\n"
        "Menejer: @Ali_tex1\n"
        "Telefon raqam: +998 90 587-31-01",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu
    )

@dp.callback_query(F.data == "catalog")
async def catalog_handler(callback: CallbackQuery):
    product_text = (
        "<b>🌿 Yashil rangli libos va kardi-to'plam</b>\n"
        "<b>Matosi:</b> Yuqori sifatli shifon va viskoza aralashmasi\n"
        "<b>Narxi:</b> 250,000 so'm\n\n"
        "<b>✨ Individual buyurtma:</b> Siz xohlagan rang va o'lchamlarda "
        "sizning shaxsiy o'lchamlaringiz bo'yicha maxsus tikib beramiz!\n"
        "Juda yengil va havo o'tkazuvchan\n"
        "Yuvilganda rangi o'zgarmaydi\n\n"
        "<i>Buyurtma berish uchun quyidagi tugmani bosing:</i>"
    )
    await callback.message.answer(product_text, parse_mode=ParseMode.HTML, reply_markup=main_menu)
    await callback.answer()

@dp.callback_query(F.data == "faq")
async def faq_handler(callback: CallbackQuery):
    faq_text = (
        "<b>❓ Ko'p beriladigan savollar va javoblar:</b>\n\n"
        "1. Buyurtmani qanday beraman?\n"
        "– Katalogdan mahsulotni tanlab, admin bilan bog'lanasiz.\n\n"
        "2. Yetkazib berish xizmati bormi?\n"
        "– Ha, O'zbekiston bo'ylab mavjud."
    )
    await callback.message.answer(faq_text, parse_mode=ParseMode.HTML, reply_markup=main_menu)
    await callback.answer()

@dp.callback_query(F.data == "contact")
async def contact_handler(callback: CallbackQuery):
    contact_text = (
        "<b>📞 Biz bilan bog'lanish:</b>\n\n"
        "Menejer: @Ali_tex1\n"
        "Telefon raqam: +998 90 587-31-01"
    )
    await callback.message.answer(contact_text, parse_mode=ParseMode.HTML, reply_markup=main_menu)
    await callback.answer()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
