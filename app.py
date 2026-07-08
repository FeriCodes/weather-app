from flask import Flask, render_template
from weather import data_structure

app = Flask(__name__)


@app.route("/")
def home():
    weather_info = data_structure()
    if "error" in weather_info:
        return f"<h1>something went wrong!</h1><p>{weather_info['Error']}"

    return render_template(
        "index.html",
        city_name=weather_info["city"],
        weather_desc=weather_info["description"],
    )


if __name__ == "__main__":
    app.run(debug=True)
