import telebot

TOKEN = "8906543011:AAE1MwSygdmOHXmPj3ELpUd502-m68ZB92M"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Bot ishlayapti.")

bot.infinity_polling()
