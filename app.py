from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os

from weather import (
    get_coordinates,
    get_current_weather,
    get_current_city,
    get_7day_forecast
)

# ============================================
# Load Environment Variables
# ============================================

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# ============================================
# Initialize Session
# ============================================

def init_session():

    if "favorites" not in session:
        session["favorites"] = []

    if "history" not in session:
        session["history"] = []


# ============================================
# Home Page
# ============================================

@app.route("/", methods=["GET", "POST"])
def home():

    init_session()

    weather = None
    error = None

    # Automatically detect city on first visit
    city = get_current_city()

    if request.method == "POST":
        city = request.form.get("city", "").strip()

    if city:

        location = get_coordinates(city)

        if location:

            weather = get_current_weather(
                location["latitude"],
                location["longitude"]
            )

            if weather:

                weather["city"] = location["city"]
                weather["country"] = location["country"]

                history = session["history"]

                if city in history:
                    history.remove(city)

                history.insert(0, city)

                session["history"] = history[:10]

            else:
                error = "Unable to fetch weather data."

        else:
            error = "City not found."

    return render_template(
        "index.html",
        weather=weather,
        error=error
    )

# ============================================
# Forecast Page
# ============================================

@app.route("/forecast")
def forecast():

    city = get_current_city()

    location = get_coordinates(city)

    forecast = []

    if location:

        forecast = get_7day_forecast(
            location["latitude"],
            location["longitude"]
        )

    return render_template(
        "forecast.html",
        city=city,
        forecast=forecast
    )
# ============================================
# Hourly Forecast Page
# ============================================

@app.route("/hourly")
def hourly():

    return render_template("hourly.html")


# ============================================
# Favorites Page
# ============================================

@app.route("/favorites")
def favorites():

    init_session()

    return render_template(
        "favorites.html",
        favorites=session["favorites"]
    )


# ============================================
# Add Favorite
# ============================================

@app.route("/favorite/add/<city>")
def add_favorite(city):

    init_session()

    favorites = session["favorites"]

    if city not in favorites:
        favorites.append(city)

    session["favorites"] = favorites

    return render_template(
        "favorites.html",
        favorites=favorites
    )


# ============================================
# Remove Favorite
# ============================================

@app.route("/favorite/remove/<city>")
def remove_favorite(city):

    init_session()

    favorites = session["favorites"]

    if city in favorites:
        favorites.remove(city)

    session["favorites"] = favorites

    return render_template(
        "favorites.html",
        favorites=favorites
    )
# ============================================
# History Page
# ============================================

@app.route("/history")
def history():

    init_session()

    return render_template(
        "history.html",
        history=session["history"]
    )


# ============================================
# Clear History
# ============================================

@app.route("/history/clear")
def clear_history():

    init_session()

    session["history"] = []

    return render_template(
        "history.html",
        history=[]
    )


# ============================================
# About Page
# ============================================

@app.route("/about")
def about():

    return render_template("about.html")


# ============================================
# Settings Page
# ============================================

@app.route("/settings")
def settings():

    return render_template("settings.html")


# ============================================
# Error Page
# ============================================

@app.route("/error")
def error():

    return render_template("error.html")


# ============================================
# Run Flask App
# ============================================

if __name__ == "__main__":

    app.run(
        debug=True
    )