import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8906543011:AAH8e..."

dp = Dispatcher()

# Asosiy menyu tugmalari (barcha tugmalar kiritilgan)
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛍 Mahsulotlar katalogi", callback_data="catalog"
            )
        ],
        [
            InlineKeyboardButton(
                text="❓ Savol-javoblar", callback_data="faq"
            ),
            InlineKeyboardButton(
                text="📞 Biz bilan aloqa", callback_data="contact"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🪟 Parda zakaz berish", callback_data="curtain"
            ),
            InlineKeyboardButton(
                text="👗 Ko'ylak zakaz berish", callback_data="dress"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🚚 Yetkazib berish shartlari", callback_data="delivery"
            )
        ],
        [
            InlineKeyboardButton(
                text="⏰ Ish vaqti", callback_data="work_time"
            ),
            InlineKeyboardButton(
                text="💳 To'lov (Karta raqami)", callback_data="payment"
            ),
        ],
    ]
)


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
  await message.answer(
      "<b>Xush kelibsiz! Alex Home & Wear rasmiy botiga marhamat.</b>\n\nQuyidagi"
      " tugmalardan birini tanlang:",
      parse_mode=ParseMode.HTML,
      reply_markup=main_menu,
  )


@dp.callback_query(F.data == "catalog")
async def catalog_handler(callback: CallbackQuery):
  product_text = (
      "<b>🌿 Yashil rangdagi libos va kardi-to'plami</b>\n"
      "<b>Matosi:</b> Yuqori sifatli shifon va trikotaj\n"
      "<b>Narxi:</b> 250,000 so'm\n\n"
      "<b>✨ Individual buyurtma:</b> Siz xohlagan mato va"
      " sizingizning shaxsiy o'lchamlaringiz bo'yicha tikib beramiz!\n"
      "<i>Buyurtma berish uchun quyidagi tugma orqali bog'laning.</i>"
  )
  await callback.message.answer(
      product_text, parse_mode=ParseMode.HTML, reply_markup=main_menu
  )
  await callback.answer()


@dp.callback_query(F.data == "faq")
async def faq_handler(callback: CallbackQuery):
  faq_text = (
      "<b>❓ Ko'p beriladigan savollar va javoblar:</b>\n\n"
      "<b>1. Buyurtmani qanday beraman?</b>\n"
      "– Tegishli guruhlarga o'tib yoki adminga yozib buyurtma berasiz.\n\n"
      "<b>2. O'lchamni qanday tanlaymiz?</b>\n"
      "– O'lchamlaringizni adminga yuborsangiz, sizga moslab tayyorlab"
      " beramiz."
  )
  await callback.message.answer(
      faq_text, parse_mode=ParseMode.HTML, reply_markup=main_menu
  )
  await callback.answer()


@dp.callback_query(F.data == "contact")
async def contact_handler(callback: CallbackQuery):
  contact_text = (
      "<b>📞 Biz bilan bog'lanish:</b>\n\n"
      "Menejer: @Ali_tex1\n"
      "Telefon raqam: +998 90 587-31-01"
  )
  await callback.message.answer(
      contact_text, parse_mode=ParseMode.HTML, reply_markup=main_menu
  )
  await callback.answer()


@dp.callback_query(F.data == "curtain")
async def curtain_handler(callback: CallbackQuery):
  text = (
      "<b>🪟 Parda zakaz berish:</b>\n\n"
      "Qo'qon shahar va atrofdagi tumanlar bo'ylab o'lcham olish va o'rnatib"
      " berish xizmatlari bilan amalga oshiriladi.\n\n"
      "Menejer bilan bog'lanish: @Ali_tex1"
  )
  await callback.message.answer(
      text, parse_mode=ParseMode.HTML, reply_markup=main_menu
  )
  await callback.answer()


@dp.callback_query(F.data == "dress")
async def dress_handler(callback: CallbackQuery):
  text = (
      "<b>👗 Ko'ylak zakaz berish:</b>\n\n"
      "Siz istagan modeldagi kiyim-kechaklarni shaxsiy o'lchamlaringiz"
      " asosida professional tarzda tikib beramiz.\n\n"
      "Buyurtma uchun: @Ali_tex1"
  )
  await callback.message.
    answer(
      text, parse_mode=ParseMode.HTML, reply_markup=main_menu
  )
  await callback.answer()


@dp.callback_query(F.data == "delivery")
async def delivery_handler(callback: CallbackQuery):
  text = (
      "<b>🚚 Yetkazib berish shartlari:</b>\n\n"
      "<b>Pardalar:</b> Qo'qon shahar va atrofdagi tumanlar bo'ylab o'lcham"
      " olish va o'rnatib berish xizmatlari bilan.\n"
      "<b>Kiyim-kechaklar:</b> O'zbekiston Respublikasi bo'ylab barcha"
      " viloyatlarga pochta orqali yetkazib beriladi."
  )
  await callback.message.answer(
      text, parse_mode=ParseMode.HTML, reply_markup=main_menu
  )
  await callback.answer()


@dp.callback_query(F.data == "work_time")
async def work_time_handler(callback: CallbackQuery):
  text = (
      "<b>⏰ Ish vaqti:</b>\n\n"
      "• <b>Telegram bot:</b> 24/7 (Kechayu kunduz avtomat ishlaydi)\n"
      "• <b>Menejer va guruhlar:</b> Har kuni 09:00 dan 20:00 gacha buyurtmalar"
      " qabul qilinadi."
  )
  await callback.message.answer(
      text, parse_mode=ParseMode.HTML, reply_markup=main_menu
  )
  await callback.answer()


@dp.callback_query(F.data == "payment")
async def payment_handler(callback: CallbackQuery):
  text = (
      "<b>💳 To'lov ma'lumotlari:</b>\n\n"
      "Karta raqami: <code>8600 0000 0000 0000</code>\n"
      "Karta egasi: M Aliyevna\n\n"
      "<i>To'lov qilib, chekni adminga yuborishni unutmang!</i>"
  )
  await callback.message.answer(
      text, parse_mode=ParseMode.HTML, reply_markup=main_menu
  )
  await callback.answer()


async def main() -> None:
  bot = Bot(token=TOKEN, default=BotProperties(parse_mode=ParseMode.HTML))
  await dp.start_polling(bot)


if name == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
