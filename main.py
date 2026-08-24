import asyncio
import logging
import sys
import sqlite3
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

TOKEN = "8986085140:AAGtJBqi7cD-nbPZDzujHyBZ3QuKvi6oNC8"

# 1. Dispatcher eng birinchi e'lon qilinadi (NameError chiqmasligi uchun)
dp = Dispatcher()

# --- RENDER UCHUN FLASK SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- BAZA BILAN ISHLASH ---
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
    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES (?, ?, ?)
    """, (user_id, full_name, username))
    conn.commit()
    conn.close()

# --- Asosiy menyu ---
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛍 Mahsulotlar katalogi", callback_data="catalog"),
            InlineKeyboardButton(text="❓ Savol-javoblar (FAQ)", callback_data="faq"),
        ],
        [
            InlineKeyboardButton(text="📢 Rasmiy guruhimiz", url="https://t.me/alex_home_wear1"),
        ],
        [
            InlineKeyboardButton(text="📢 Parda zakaz guruhi", url="https://t.me/parda_tikamiz_oson_tez"),
        ],
        [
            InlineKeyboardButton(text="✍️ Kiyimlar uchun zakaz guruhi", url="https://t.me/zakazga_hamma_narsa_tikamiz"),
        ],
        [
            InlineKeyboardButton(text="⭐ Mijozlar sharhlari", callback_data="reviews"),
        ],
        [
            InlineKeyboardButton(text="📏 O'lcham olish va yetkazib berish", callback_data="size_delivery"),
        ],
        [
            InlineKeyboardButton(text="⏰ Ish vaqti va Manzil", callback_data="worktime"),
        ],
        [
            InlineKeyboardButton(text="💳 To'lov (Karta raqami)", callback_data="payment"),
        ],
        [
            InlineKeyboardButton(text="📞 Biz bilan aloqa", callback_data="contact"),
        ]
    ]
)

order_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✍️ Buyurtma berish", url="https://t.me/Ali_tex1")
        ],
        [
            InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_menu")
        ]
    ]
)

back_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_menu")
        ]
    ]
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = message.from_user
    username = f"@{user.username}" if user.username else "Username yo'q"
    add_user(user.id, user.full_name, username)
    
    await message.answer(
        f"Assalomu alaykum, {html.bold(user.full_name)}! \n"
        f"<b>Alex Home & Wear</b> rasmiy botiga xush kelibsiz.\n\n"
        f"Botimiz sizga 24/7 rejimida xizmat ko'rsatadi. Kerakli bo'limni tanlang:",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML,
    )

@dp.message(Command("stat"))
async def stats_handler(message: Message):
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT full_name, username FROM users")
    users = cursor.fetchall()
    conn.close()

    user_list_text = "<b>Botga kirgan mijozlar ro'yxati:</b>\n"
    for idx, (name, uname) in enumerate(users, 1):
        user_list_text += f"{idx}. {name} ({uname})\n"

    stat_message = (
        f"<b>📊 Bot statistikasi:</b>\n\n"
        f"<b>Jami foydalanuvchilar:</b> {total_users} ta\n\n"
        f"{user_list_text}"
    )
    await message.answer(stat_message, parse_mode=ParseMode.HTML)

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Asosiy menyu:", reply_markup=main_menu, parse_mode=ParseMode.HTML
    )

@dp.callback_query(F.data == "catalog")
async def catalog_handler(callback: CallbackQuery):
    product_text = (
        f"<b>🌿 Libos va kardi-te'placer/plato</b>\n"
        f"<b>💰Narxi:</b> 250,000 so'm\n\n"
        f"<b>Individual buyurtma:</b> Siz xohlagan rang va o'lchamlarda "
        f"sizning shaxsiy o'lcharingiz bo'yicha maxsus tikib beramiz!\n"
        f"- Juda yengil va havo o'tkazuvchan\n"
        f"- Yuvilganda rangi o'zgarmaydi\n"
        f"- Buyurtma berish uchun quyidagi tugmani bosing:"
    )
    
    # Eskirgan rasm ID'lari xato bermasligi uchun vaqtincha faqat matn va buyurtma tugmasi shaklida ko'rsatiladi
    await callback.message.edit_text(
        product_text, parse_mode=ParseMode.HTML, reply_markup=order_markup
    )
    await callback.answer()

@dp.callback_query(F.data == "reviews")
async def reviews_handler(callback: CallbackQuery):
    reviews_text = (
        f"<b>⭐ Mijozlar sharhlari va fikrlari:</b>\n\n"
        f"Bizning ishlarimizdan mamnun bo'lgan mijozlarimizning samimiy "
        f"tashakkurlari va sharhlari biz uchun eng katta mukofotdir!\n\n"
        f"Siz ham o'z fikringizni qoldirishingiz yoki boshqalarning "
        f"sharhlari bilan tanishishingiz mumkin."
    )
    await callback.message.edit_text(
        reviews_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
    )
    await callback.answer()

@dp.callback_query(F.data == "size_delivery")
async def size_delivery_handler(callback: CallbackQuery):
    sd_text = (
        f"<b>📏 O'lcham olish va yetkazib berish shartlari:</b>\n\n"
        f"<b>1. O'lcham olish:</b>\n"
        f"🔹 36 (Standart 42-44) - Ko'krak: 84-88 sm | Bel: 66-70 sm | Son: 90-94 sm\n"
        f"🔹 38 (Standart 46) - Ko'krak: 92-96 sm | Bel: 74-78 sm | Son: 98-102 sm\n"
        f"🔹 40 (Standart 48) - Ko'krak: 100-104 sm | Bel: 82-86 sm | Son: 106-110 sm\n"
        f"🔹 42 (Standart 50-52) - Ko'krak: 108-112 sm | Bel: 90-94 sm | Son: 114-118 sm\n\n"
        f"Odatdagi o'lchamingiz yoki bo'yingizni aytsangiz, shaxsiy o'lcharingizga moslab tikamiz.\n\n"
        f"<b>2. Yetkazib berish:</b>\n"
        f"<b>Pardalar:</b> Qo'qon shahar va atrofdagi tumanlar bo'ylab eltib berish va o'rnatib berish bilan.\n"
        f"<b>Kiyim-kechaklar:</b> O'zbekiston bo'ylab barcha viloyatlarga pochta orqali yuboriladi."
    )
    await callback.message.edit_text(
        sd_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
    )
    await callback.answer()

@dp.callback_query(F.data == "faq")
async def faq_handler(callback: CallbackQuery):
    faq_text = (
        f"<b>❓ Ko'p beriladigan savollar va javoblar:</b>\n\n"
        f"<b>1. Buyurtmani qanday beraman?</b>\n"
        f"- Guruhlarga o'tib yoki adminga yozib buyurtma berasiz.\n\n"
        f"<b>2. O'lchamni qanday tanlaymiz?</b>\n"
        f"- O'lchamlaringizni adminga yozib yuborsangiz, sizga moslab tayyorlab beramiz."
    )
    await callback.message.edit_text(
        faq_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
    )
    await callback.answer()

@dp.callback_query(F.data == "worktime")
async def worktime_handler(callback: CallbackQuery):
    worktime_text = (
        f"<b>⏰ Ish vaqti va Manzil:</b>\n\n"
        f"<b>Telegram guruh va kanallar:</b> 24/7 ochiq\n"
        f"<b>Menejer:</b> Har kuni 09:00 dan 20:00 gacha buyurtmalar qabul qiladi.\n\n"
        f"<b>📍 Manzil:</b> Qo'qon shahar, Avgonbog', Ansor market yonida"
    )
    await callback.message.edit_text(
        worktime_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
    )
    await callback.answer()

@dp.callback_query(F.data == "payment")
async def payment_handler(callback: CallbackQuery):
    payment_text = (
        f"<b>💳 To'lov ma'lumotlari:</b>\n\n"
        f"<b>Aloqa bank:</b>\n"
        f"<b>Karta raqami:</b> <code>9860 6889 7583 2881</code>\n"
        f"<b>Karta egasi:</b> MASTURAKHON ABDURASHIDOVA\n\n"
        f"<b>Xalq banki:</b>\n"
        f"<b>Karta raqami:</b> <code>9860 0803 0322 0482</code>\n"
        f"<b>Karta egasi:</b> MASTURAKHON NASIROVA\n\n"
        f"<i>To'lov qilib, chekni adminga yuborishni unutmang!</i>"
    )
    await callback.message.edit_text(
        payment_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
    )
    await callback.answer()

@dp.callback_query(F.data == "contact")
async def contact_handler(callback: CallbackQuery):
    contact_text = (
        f"<b>📞 Biz bilan bog'lanish:</b>\n\n"
        f"<b>Menejer:</b> @Ali_tex1\n"
        f"<b>Telefon raqam:</b> +998 90 587-31-01"
    )
    await callback.message.edit_text(
        contact_text, parse_mode=ParseMode.HTML, reply_markup=back_markup
    )
    await callback.answer()

async def main() -> None:
    keep_alive()
    bot = Bot(
        token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
