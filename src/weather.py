import os
import requests
from dotenv import load_dotenv
import datetime as dt
from urllib.parse import quote

load_dotenv()


class Weather:
    def __init__(self):
        self.API_KEY = os.getenv("WEATHER_API_KEY")
        self.HOME_LAT = os.getenv("TARGET_LAT")
        self.HOME_LON = os.getenv("TARGET_LON")
        self.session = requests.Session()

    def get_weather_data(self, location=None):
        lang_param = "fa"

        if not location:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.HOME_LAT}&lon={self.HOME_LON}&appid={self.API_KEY}&units=metric&lang={lang_param}"
        elif "," in location:
            try:
                lat, lon = map(str.strip, location.split(","))
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}&units=metric&lang={lang_param}"
            except ValueError:
                return {"Error": "Invalid coordinate format. Example: 33.11,46.16"}
        else:
            if location.isascii():
                lang_param = "en"

            safe_location = quote(location)
            url = f"https://api.openweathermap.org/data/2.5/weather?q={safe_location}&appid={self.API_KEY}&units=metric&lang={lang_param}"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                lat = data["coord"]["lat"]
                lon = data["coord"]["lon"]

                pollution_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.API_KEY}"
                pollution_response = self.session.get(pollution_url, timeout=10)

                aqi_status = "Unknown" if lang_param == "en" else "نامشخص"

                # FIXED: Moved the mapper and assignment inside the status check
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

                    aqi_status = aqi_mapper.get(aqi_code, aqi_status)

                local_offset = dt.timezone(dt.timedelta(seconds=data["timezone"]))
                sunrise_time = dt.datetime.fromtimestamp(
                    data["sys"]["sunrise"], tz=local_offset
                ).strftime("%H:%M")
                sunset_time = dt.datetime.fromtimestamp(
                    data["sys"]["sunset"], tz=local_offset
                ).strftime("%H:%M")
                wind_speed_kmh = round(data["wind"]["speed"] * 3.6, 1)

                weather_data = {
                    "country": data["sys"]["country"],
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "speed": wind_speed_kmh,
                    "sunrise": sunrise_time,
                    "sunset": sunset_time,
                    "aqi": aqi_status,
                }
                return weather_data

            elif response.status_code == 404:
                return {
                    "Error": "City or coordinates not found. Please check your input!"
                }
            elif response.status_code == 401:
                return {"Error": "Invalid API Key. Please check your .env file."}
            else:
                return {"Error": f"Server returned error code: {response.status_code}"}

        except requests.exceptions.Timeout:
            return {
                "Error": "Connection timed out. Please check your network or try using a proxy/VPN."
            }
        except Exception as e:
            return {"Error": f"An unexpected error occurred: {e}"}


if __name__ == "__main__":
    weather = Weather()
    print(weather.get_weather_data())
