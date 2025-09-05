from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# put your OpenWeather API key here
API_KEY = "5f13b804fea2353d008753f93637f717"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    alerts = []

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            print(data)  # 👈 shows in terminal for debugging

            if response.status_code == 200:
                weather_data = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "wind": round(data["wind"]["speed"] * 3.6, 1),  # m/s → km/h
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                }

                # simple alerts
                if weather_data["temp"] > 35:
                    alerts.append("🥵 Stay hydrated, it’s very hot!")
                if "rain" in weather_data["description"].lower():
                    alerts.append("🌧 Don’t forget your umbrella!")
                if weather_data["wind"] > 50:
                    alerts.append("🌪 High wind warning!")

    return render_template("index.html", weather=weather_data, alerts=alerts)

if __name__ == "__main__":
    app.run(debug=True)
