import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
lat = os.getenv("TARGET_LAT")
lon = os.getenv("TARGET_LON")

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "country": data["sys"]["country"],
            "city": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["main"],
            "speed": data["wind"]["speed"],
        }
        print(weather_data)


except Exception as e:
    print(f"Error: {e}")
