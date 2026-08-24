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

if name == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
