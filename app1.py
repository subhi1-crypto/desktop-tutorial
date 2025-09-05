from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "5f13b804fea2353d008753f93637f717"   # 🔑 paste your real OpenWeather key here
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if data["cod"] == 200:
                weather = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                }
            else:
                weather = {"error": data["message"]}
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
