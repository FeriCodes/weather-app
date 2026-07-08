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
        weather = data["weather"]
        print("Data fetched successfully!")


except Exception as e:
    print(f"Error: {e}")
