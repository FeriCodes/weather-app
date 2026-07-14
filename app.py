from flask import Flask, render_template, request
from src.weather import get_weather_data
import os

app = Flask(__name__)


@app.route("/")
def home():
    user_location = request.args.get("location") or None

    weather_info = get_weather_data(user_location)

    if "Error" in weather_info:
        return render_template("index.html", error_msg=weather_info["Error"])

    return render_template(
        "index.html",
        con_name=weather_info["country"],
        city_name=weather_info["city"],
        weather_desc=weather_info["description"],
        weather_temp=weather_info["temp"],
        feels_like=weather_info["feels_like"],
        humidity=weather_info["humidity"],
        wind_speed_kmh=weather_info["speed"],
        sunrise_time=weather_info["sunrise"],
        sunset_time=weather_info["sunset"],
        aqi_status=weather_info["aqi"],
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
