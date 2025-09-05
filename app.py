import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔑 API key (you can set it in Render Environment Variables)
API_KEY = os.environ.get("API_KEY", "your_api_key_here")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form["city"]
        url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != "404":
            weather_data = {
                "city": response["name"],
                "temp": response["main"]["temp"],
                "description": response["weather"][0]["description"].title(),
                "icon": response["weather"][0]["icon"]
            }
        else:
            error = "⚠️ City not found. Please try again."

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)
