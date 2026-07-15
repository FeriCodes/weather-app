import os
import re
import telebot
from telebot import types
from dotenv import load_dotenv
from src.weather import get_weather_data

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_LAT = os.getenv("TARGET_LAT")
TARGET_LON = os.getenv("TARGET_LON")

bot = telebot.TeleBot(BOT_TOKEN)


def send_weather_report(message, query_value, title_name, silent_on_error=False):
    """
    تابع کمکی و مشترک برای دریافت داده و ارسال گزارش آب‌وهوا.
    با استفاده از این تابع، از تکرار کد جلوگیری می‌کنیم.
    """
    try:
        weather = get_weather_data(query_value)

        if "Error" in weather:
            error_msg = weather["Error"].lower()
            if silent_on_error and ("not found" in error_msg or "404" in error_msg):
                return
            return bot.reply_to(message, f"❌ خطا: {weather['Error']}")

        bot.reply_to(message, f"🔍 در حال دریافت اطلاعات آب و هوای {title_name}...")

        weather_info = f"""
📍 *وضعیت آب و هوای {title_name}*
━━━━━━━━━━━━━━━━━━

🌍 *کشور:* {weather['country']} | 🏙️ *شهر:* {weather['city']}
☁️ *آسمان:* {weather['description']}

🌡️ *دما:* {weather['temp']}°C
🥵 *دمای احساس‌شده:* {weather['feels_like']}°C

💧 *رطوبت:* {weather['humidity']}%
💨 *سرعت باد:* {weather['speed']} km/h

🌅 *طلوع آفتاب:* {weather['sunrise']}
🌇 *غروب آفتاب:* {weather['sunset']}

🍃 *شاخص پاکی هوا:* {weather['aqi']}
"""
        bot.reply_to(message, weather_info.strip(), parse_mode="Markdown")

    except Exception as e:
        print(f"Error handling weather request: {e}")
        if not silent_on_error:
            bot.reply_to(message, "❌ خطایی در پردازش اطلاعات رخ داد.")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_my_weather = types.KeyboardButton("🏠 آب و هوای من")
    btn_help = types.KeyboardButton("📖 راهنما")

    markup.row(btn_my_weather)
    markup.row(btn_help)

    welcome_text = (
        "سلام من ربات هواشناسی هستم.\n"
        "برای دریافت راهنمایی روی دکمه '📖 راهنما' بزنید یا فرمان /help رو بفرستید."
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == "📖 راهنما")
def send_help(message):
    help_text = (
        "برای دریافت اطلاعات هواشناسی فقط کافیه بگید 'weather' یا 'هوا' و پس از اون اسم شهر یا کشور خودتون رو بنویسید مثلا:\n"
        "weather تهران\n"
        "weather Tehran"
    )
    bot.reply_to(message, help_text.strip(), parse_mode="Markdown")


@bot.message_handler(func=lambda message: message.text == "🏠 آب و هوای من")
def handle_my_weather(message):
    if not TARGET_LAT or not TARGET_LON:
        bot.reply_to(message, "خطایی غیرمنتظره رخ داد !")
        return

    send_weather_report(
        message=message,
        query_value=f"{TARGET_LAT},{TARGET_LON}",
        title_name="منطقه شما",
        silent_on_error=False,
    )


@bot.message_handler(regexp=r"^(weather|هوا)\s+(.+)")
def handle_city_weather(message):
    match = re.match(r"^(weather|هوا)\s+(.+)", message.text, re.IGNORECASE)
    if not match:
        return

    city_name = match.group(2).strip()

    send_weather_report(
        message=message,
        query_value=city_name,
        title_name=f"شهر {city_name}",
        silent_on_error=True,
    )


if __name__ == "__main__":
    print("Bot is running safely...")
    bot.polling(none_stop=True)
