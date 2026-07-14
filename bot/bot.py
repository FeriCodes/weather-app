import os
import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    welcome_text = (
        "سلام من ربات هواشناسی هستم.\n"
        "برای نحوه استفاده از من، فرمان /help رو بفرستین."
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "برای دریافت اطلاعات هواشناسی فقط کافیه بگید 'weather' یا 'هوا' و پس از اون اسم شهر یا کشور خودتون رو بنویسید مثلا:\n"
        "weather تهران\n"
        "weather Tehran"
    )
    bot.reply_to(message, help_text)


if __name__ == "__main__":
    print("Bot is running safely...")
    bot.polling(none_stop=True)
