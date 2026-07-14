import os
import requests
from dotenv import load_dotenv
import datetime as dt
from urllib.parse import quote

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
HOME_LAT = os.getenv("TARGET_LAT")
HOME_LON = os.getenv("TARGET_LON")


def get_weather_data(location=None):

    lang_param = "fa"

    if not location:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={HOME_LAT}&lon={HOME_LON}&appid={API_KEY}&units=metric&lang={lang_param}"

    elif "," in location:
        try:
            lat, lon = map(str.strip, location.split(","))
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang={lang_param}"
        except ValueError:
            return {"Error": "Invalid coordinate format. Example: 33.11,46.16"}
    else:

        if location.isascii():
            lang_param = "en"
        else:
            lang_param = "fa"

        safe_location = quote(location)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={safe_location}&appid={API_KEY}&units=metric&lang={lang_param}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()

            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]

            pollution_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            pollution_response = requests.get(pollution_url, timeout=5)

            aqi_status = "Unknown" if lang_param == "en" else "نامشخص"
            if pollution_response.status_code == 200:
                pollution_data = pollution_response.json()
                aqi_code = pollution_data["list"][0]["main"]["aqi"]

            if lang_param == "en":
                aqi_mapper = {
                    1: "Good",
                    2: "Fair",
                    3: "Moderate",
                    4: "Poor",
                    5: "Very Poor",
                }
            else:
                aqi_mapper = {
                    1: "عالی",
                    2: "قابل قبول",
                    3: "متوسط",
                    4: "ناسالم",
                    5: "بسیار خطرناک",
                }

            aqi_status = aqi_mapper.get(
                aqi_code, "Unknown" if lang_param == "en" else "نامشخص"
            )

            local_offset = dt.timezone(dt.timedelta(seconds=data["timezone"]))
            sunrise_time = dt.datetime.fromtimestamp(
                data["sys"]["sunrise"], tz=local_offset
            ).strftime("%H:%M")
            sunset_time = dt.datetime.fromtimestamp(
                data["sys"]["sunset"], tz=local_offset
            ).strftime("%H:%M")

            wind_speed_kmh = round(data["wind"]["speed"] * 3.6, 1)

            weather_desc = data["weather"][0]["description"]

            weather_data = {
                "country": data["sys"]["country"],
                "city": data["name"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": weather_desc,
                "speed": wind_speed_kmh,
                "sunrise": sunrise_time,
                "sunset": sunset_time,
                "aqi": aqi_status,
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
