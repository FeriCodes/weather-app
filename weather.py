import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
HOME_LAT = os.getenv("TARGET_LAT")
HOME_LON = os.getenv("TARGET_LON")


def get_weather_data(location=None):
    if not location:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={HOME_LAT}&lon={HOME_LON}&appid={API_KEY}&units=metric"

    elif "," in location:
        try:
            lat, lon = map(str.strip, location.split(","))
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        except ValueError:
            return {"Error": "Invalid coordinate format. Example: 33.11,46.16"}
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
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
            return weather_data

        elif response.status_code == 404:
            return {"Error": "City or coordinates not found. Please check your input!"}
        elif response.status_code == 401:
            return {"Error": "Invalid API Key. Please check your .env file."}
        else:
            return {"Error": f"Server returned error code: {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"Error": "Connection timed out. Please try again later."}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {e}"}
