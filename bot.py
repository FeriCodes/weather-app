from email.mime import message
import os
from src.weather import get_weather_data
from telebot import telebot, types

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

TARGET_LAT = os.getenv("TARGET_LAT")
TARGET_LON = os.getenv("TARGET_LON")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_my_weather = types.KeyboardButton("🏠 آب و هوای من")
    markup.add(btn_my_weather)

    welcome_text = (
        "سلام من ربات هواشناسی هستم.\n"
        "برای نحوه استفاده از من، فرمان /help رو بفرستین."
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)


@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "برای دریافت اطلاعات هواشناسی فقط کافیه بگید 'weather' یا 'هوا' و پس از اون اسم شهر یا کشور خودتون رو بنویسید مثلا:\n"
        "weather تهران\n"
        "weather Tehran"
    )
    bot.reply_to(message, help_text)


@bot.message_handler(func=lambda message: message.text == "🏠 آب و هوای من")
def send_my_weather(message):
    if not TARGET_LAT or not TARGET_LON:
        bot.reply_to(message, "موقعیت مکانی شما تنظیم نشده است.❌")
        return

    bot.reply_to(message, "🔍 در حال دریافت اطلاعات آب و هوای خانه شما...")
    try:
        my_weather = get_weather_data(f"{TARGET_LAT},{TARGET_LON}")
        if "Error" in my_weather:
            return bot.reply_to(
                message, f"❌ خطا در دریافت اطلاعات هواشناسی: {my_weather['Error']}"
            )
        else:

            weather_info = (
                f"📍 *وضعیت آب و هوای منطقه شما*\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
                f"🌍 *کشور:* {my_weather['country']} | 🏙️ *شهر:* {my_weather['city']}\n"
                f"☁️ *آسمان:* {my_weather['description']}\n\n"
                f"🌡️ *دما:* {my_weather['temp']}°C\n"
                f"🥵 *دمای احساس‌شده:* {my_weather['feels_like']}°C\n\n"
                f"💧 *رطوبت:* {my_weather['humidity']}%\n"
                f"💨 *سرعت باد:* {my_weather['speed']} km/h\n\n"
                f"🌅 *طلوع آفتاب:* {my_weather['sunrise']}\n"
                f"🌇 *غروب آفتاب:* {my_weather['sunset']}\n\n"
                f"🍃 *شاخص پاکی هوا:* {my_weather['aqi']}"
            )
            bot.reply_to(message, weather_info, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ خطایی رخ داد: {str(e)}")


if __name__ == "__main__":
    print("Bot is running safely...")
    bot.polling(none_stop=True)
