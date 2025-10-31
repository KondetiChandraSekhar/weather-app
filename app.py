from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "7898272576d6aa7be9edb6020682bc7a"  # Replace with your actual API key

@app.route("/", methods=["GET", "POST"])
def weather():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form["city"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            desc = data["weather"][0]["description"].capitalize()
            emoji = get_weather_emoji(desc)

            weather_data = {
                "city": data["name"],
                "temp": round(data["main"]["temp"]),
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "desc": f"{desc} {emoji}",
            }
        else:
            error = "City name is incorrect or API key invalid."
    return render_template("index.html", weather=weather_data, error=error)

def get_weather_emoji(desc):
    desc = desc.lower()
    if "rain" in desc:
        return "🌧️"
    elif "cloud" in desc:
        return "☁️"
    elif "sun" in desc or "clear" in desc:
        return "☀️"
    elif "storm" in desc:
        return "⛈️"
    elif "snow" in desc:
        return "❄️"
    elif "mist" in desc or "fog" in desc:
        return "🌫️"
    else:
        return "🌍"

if __name__ == "__main__":
    app.run(debug=True)
