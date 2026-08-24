import asyncio
import logging
import sqlite3
import sys
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)

TOKEN = "8906543011:AAE1MwSygdmOHXmPj3ELpUd5O2-m68ZB92M"

dp = Dispatcher()

# --- BAZA BILAN ISHLASH (Statistika uchun) ---
def init_db():
  conn = sqlite3.connect("bot_users.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()


def add_user(user_id, full_name, username):
  conn = sqlite3.connect("bot_users.db")
  cursor = conn.cursor()
  cursor.execute(
      "INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES"
      " (?, ?, ?)",
      (user_id, full_name, username),
  )
  conn.commit()
  conn.close()


# Asosiy menyu
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛍 Mahsulotlar katalogi", callback_data="catalog"
            ),
            InlineKeyboardButton(
                text="❓ Savol-javoblar (FAQ)", callback_data="faq"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🪟 Parda zakaz guruhi",
                url="https://t.me/parda_tikamiz_oson_tez",
            ),
            InlineKeyboardButton(
                text="👗 Ko'ylak zakaz guruhi",
                url="https://t.me/zakazga_hamma_narsa_tikamiz",
            ),
        ],
        [
            InlineKeyboardButton(
                text="💬 Mijozlar sharhlari",
                url="https://t.me/parda_tikamiz_oson_tez",
            ),
            InlineKeyboardButton(
                text="📏 O'lcham olish yo'riqnomasi", callback_data="size_guide"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🚚 Yetkazib berish shartlari", callback_data="delivery"
            ),
            InlineKeyboardButton(
                text="⏰ Ish vaqti", callback_data="worktime"
            ),
        ],
        [
            InlineKeyboardButton(
                text="💳 To'lov (Karta raqami)", callback_data="payment"
            ),
            InlineKeyboardButton(
                text="📞 Biz bilan aloqa", callback_data="contact"
            ),
        ],
    ]
)

order_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛍 Buyurtma berish", url="https://t.me/Ali_tex1"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Asosiy menyu", callback_data="back_to_menu"
            )
        ],
    ]
)

back_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Asosiy menyu", callback_data="back_to_menu"
            )
        ]
    ]
)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
  # Foydalanuvchini bazaga qo'shish
  user = message.from_user
  username = f"@{user.username}" if user.username else "Username yo'q"
  add_user(user.id, user.full_name, username)

  await message.answer(
      f"Assalomu alaykum, {html.bold(user.full_name)}! "
      f"<b>Alex Home & Wear</b> rasmiy botiga xush kelibsiz.\n\n"
      f"Botimiz sizga 24/7 rejimida xizmat ko'rsatadi. Kerakli bo'limni tanlang:",
      reply_markup=main_menu,
      parse_mode=ParseMode.HTML,
  )


# --- ADMIN UCHUN STATISTIKA BUYRUG'I ---
@dp.message(Command("stat"))
async def stats_handler(message: Message):
  conn = sqlite3.connect("bot_users.db")
  cursor = conn.cursor()
  cursor.execute("SELECT COUNT(*) FROM users")
  total_users = cursor.fetchone()[0]

  cursor.execute("SELECT full_name, username FROM users")
  users = cursor.fetchall()
  conn.close()
  user_list_text = "<b>👥 Botga kirgan mijozlar ro'yxati:</b>\n\n"
  for idx, (name, uname) in enumerate(users, 1):
    user_list_text += f"{idx}. {name} ({uname})\n"

  stat_message = (
      f"📊 <b>Bot statistikasi:</b>\n\n"
      f"Jami foydalanuvchilar: <b>{total_users} ta</b>\n\n"
      f"{user_list_text}"
  )
  await message.answer(stat_message, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery):
  await callback.message.answer(
      "Asosiy menyu:", reply_markup=main_menu, parse_mode=ParseMode.HTML
  )
  await callback.answer()


@dp.callback_query(F.data == "catalog")
async def catalog_handler(callback: CallbackQuery):
  product_text = (
      "👗 <b>Yashil rangli libos va kardi-to'plam</b>\n\n"
      "<b>Matosi:</b> Yuqori sifatli shifon va viskoza aralashmasi\n"
      "<b>Narxi:</b> 250,000 so'm\n\n"
      "✨ <b>Individual buyurtma:</b> Siz xohlagan rang va o'lchamlarda "
      "sizning shaxsiy o'lchamlaringiz bo'yicha maxsus tikib beramiz!\n\n"
      "– Juda yengil va havo o'tkazuvchan\n"
      "– Yuvilganda rangi o'zgarmaydi\n\n"
      "<i>Buyurtma berish uchun quyidagi tugmani bosing:</i>"
  )

  media = [
      InputMediaPhoto(
          media=(
              "AgACAgIAAxkBAAIBoFrgj16XuHM6GekmvS2v1Kr9MMAavMZaxsitGlIPuc4u39tBcBAAMCAAN5AAM9BA"
          ),
          caption=product_text,
          parse_mode=ParseMode.HTML,
      ),
      InputMediaPhoto(
          media=(
              "AgACAgIAAxkBAAIBoFrgmUF2qn0a4mCPVhux1JWDg4AAvkZaxsitGlIH8iHqZZBdVwBAAMCAAN5AAM9BA"
          )
      ),
      InputMediaPhoto(
          media=(
              "AgACAgIAAxkBAAIBoFrgqwMyEEOYqcdFn8yV3QLCSYAAvUZaxsitGlIBzAn2YBYISsBAAMCAAN5AAM9BA"
          )
      ),
      InputMediaPhoto(
          media=(
              "AgACAgIAAxkBAAIBoFrgktJEpaTe2El6AIEYMSXWPsAAvYZaxsitGlIN0uEWFH3csBAAMCAAN5AAM9BA"
          )
      ),
  ]

  await callback.message.answer_media_group(media=media)
  await callback.message.answer(
      "Buyurtma berish uchun tugmani bosing:", reply_markup=order_markup
  )
  await callback.answer()


@dp.callback_query(F.data == "size_guide")
async def size_guide_handler(callback: CallbackQuery):
  guide_text = (
      "<b>📏 O'lchamlar jadvali va yo'riqnoma:</b>\n\n"
      "Buyurtma berishda adashmasligingiz uchun o'lchamlarni quyidagicha"
      " aniqlab olasiz:\n\n"
      "• <b>S (Standart 42-44)</b> — Ko'krak aylanasi: 84-88 sm | Bel: 66-70 sm |"
      " Son: 90-94 sm\n"
      "• <b>M (Standart 46)</b> — Ko'krak aylanasi: 92-96 sm | Bel: 74-78 sm |"
      " Son: 98-102 sm\n"
      "• <b>L (Standart 48)</b> — Ko'krak aylanasi: 100-104 sm | Bel: 82-86 sm |"
      " Son: 106-110 sm\n"
      "• <b>XL (Standart 50-52)</b> — Ko'krak aylanasi: 108-112 sm | Bel: 90-94"
      " sm | Son: 114-118 sm\n\n"
      "👖 <b>Shim va liboslar uchun:</b>\n"
      "Siz odatda kiyadigan razmeringizni (masalan: <b>S, M, L, XL</b> yoki"
      " <b>34, 36, 38</b>) va bo'yingiz uzunligini aytsangiz, shaxsiy"
      " o'lchamlaringizga moslab maxsus tikib beramiz!\n\n"
      "<i>Aniq o'lcham olishda qiynalsangiz, adminga yozing, yordam beramiz:</i>"
      " @Ali_tex1"
  )
  await callback.message.edit_text(
      guide_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
  )
  await callback.answer()


@dp.callback_query(F.data == "faq")
async def faq_handler(callback: CallbackQuery):
  faq_text = (
      "<b>❓ Ko'p beriladigan savollar va javoblar:</b>\n\n"
      "<b>1. Buyurtmani qanday beraman?</b>\n"
      "– Tegishli guruhlarga o'tib yoki adminga yozib buyurtma berasiz.\n\n"
      "<b>2. O'lchamni qanday tanlaymiz?</b>\n"
      "– O'lchamlaringizni adminga yuborsangiz, sizga moslab tayyorlab beramiz."
  )
  await callback.message.edit_text(
      faq_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
  )
  await callback.answer()


@dp.callback_query(F.data == "delivery")
async def delivery_handler(callback: CallbackQuery):
  delivery_text = (
      "<b>🚚 Yetkazib berish shartlari:</b>\n\n"
      "🪟 <b>Pardalar:</b> Qo'qon shahar va atrofdagi tumanlar bo'ylab o'lcham"
      " olish va o'rnatib berish xizmatlari bilan.\n"
      "👗 <b>Kiyim-kechaklar:</b> O'zbekiston Respublikasi bo'ylab barcha"
      " viloyatlarga pochta orqali yetkazib beriladi."
  )
  await callback.message.edit_text(
      delivery_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
  )
  await callback.answer()


@dp.callback_query(F.data == "worktime")
async def worktime_handler(callback: CallbackQuery):
  worktime_text = (
      "<b>⏰ Ish vaqti:</b>\n\n"
      "• <b>Telegram bot:</b> 24/7 (Kechayu kunduz avtomat ishlaydi)\n"
      "• <b>Menejer va guruhlar:</b> Har kuni 09:00 dan 20:00 gacha"
      " buyurtmalar qabul qilinadi."
  )
  await callback.message.edit_text(
      worktime_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
  )
  await callback.answer()


@dp.callback_query(F.data == "payment")
async def payment_handler(callback: CallbackQuery):
  payment_text = (
      "<b>💳 To'lov ma'lumotlari:</b>\n\n"
      "<b>Aloqa bank:</b>\n"
      "Karta raqami: <code>5614 6889 7583 2881</code>\n"
      "Karta egasi: MASTURAKHON ABDURASHIDOVA\n\n"
      "<b>Xalq banki:</b>\n"
      "Karta raqami: <code>9860 0803 8322 0482</code>\n"
      "Karta egasi: MASTURAKHON NASIROVA\n\n"
      "<i>To'lov qilib, chekni adminga yuborishni unutmang!</i>"
  )
  await callback.message.edit_text(
      payment_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
  )
  await callback.answer()


@dp.callback_query(F.data == "contact")
async def contact_handler(callback: CallbackQuery):
  contact_text = (
      "<b>📞 Biz bilan bog'lanish:</b>\n\n"
      "Menejer: @Ali_tex1\n"
      "Telefon raqam: +998 90 587-31-01"
  )
  await callback.message.edit_text(
      contact_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
  )
  await callback.answer()


async def main() -> None:
  bot = Bot(
      token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
  )
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
