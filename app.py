from flask import Flask, render_template, request
from weather import get_weather_data

app = Flask(__name__)


@app.route("/")
def home():
    user_location = request.args.get("location") or None

    weather_info = get_weather_data(user_location)

    if "Error" in weather_info:
        return f"<h1>something went wrong!</h1><p>{weather_info['Error']}</p>"

    return render_template(
        "index.html",
        con_name=weather_info["country"],
        city_name=weather_info["city"],
        weather_desc=weather_info["description"],
        weather_temp=weather_info["temp"],
        feels_like=weather_info["feels_like"],
        humidity=weather_info["humidity"],
        wind_speed=weather_info["speed"],
    )


if __name__ == "__main__":
    app.run(debug=True)
