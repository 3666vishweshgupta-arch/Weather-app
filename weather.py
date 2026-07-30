import geocoder
import requests
from datetime import datetime


# ============================================
# Weather Description
# ============================================

def weather_description(code):
    weather_codes = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        56: "Freezing Drizzle",
        57: "Heavy Freezing Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Rain Showers",
        81: "Heavy Rain Showers",
        82: "Violent Rain Showers",
        85: "Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Severe Thunderstorm"
    }

    return weather_codes.get(code, "Unknown")


# ============================================
# Weather Icon
# ============================================

def weather_icon(code):
    icons = {
        0: "☀️",
        1: "🌤️",
        2: "⛅",
        3: "☁️",
        45: "🌫️",
        48: "🌫️",
        51: "🌦️",
        53: "🌦️",
        55: "🌧️",
        56: "🌧️",
        57: "🌧️",
        61: "🌧️",
        63: "🌧️",
        65: "⛈️",
        66: "🌧️",
        67: "🌧️",
        71: "❄️",
        73: "❄️",
        75: "❄️",
        77: "❄️",
        80: "🌦️",
        81: "🌧️",
        82: "⛈️",
        85: "🌨️",
        86: "🌨️",
        95: "⛈️",
        96: "⛈️",
        99: "⛈️"
    }

    return icons.get(code, "🌍")


# ============================================
# Time Formatting
# ============================================
# ============================================
# Weather Theme
# ============================================

def weather_theme(code, current_time=None, sunrise=None, sunset=None):

    if current_time and sunrise and sunset:

        now = datetime.fromisoformat(current_time).time()
        sunrise_time = datetime.fromisoformat(sunrise).time()
        sunset_time = datetime.fromisoformat(sunset).time()

        if now < sunrise_time or now > sunset_time:
            return "night"

    if code == 0:
        return "sunny"

    elif code in [1, 2, 3]:
        return "cloudy"

    elif code in [45, 48]:
        return "fog"

    elif code in [51, 53, 55, 56, 57, 61, 63, 66, 67, 80, 81]:
        return "rain"

    elif code in [65, 82, 95, 96, 99]:
        return "storm"

    elif code in [71, 73, 75, 77, 85, 86]:
        return "snow"

    return "sunny"


# ============================================
# Temperature Color Class
# ============================================

def temperature_class(temp):

    if temp <= 0:
        return "freezing"

    elif temp <= 10:
        return "cold"

    elif temp <= 20:
        return "cool"

    elif temp <= 30:
        return "warm"

    elif temp <= 40:
        return "hot"

    return "very-hot"

def format_time(time_string):
    dt = datetime.fromisoformat(time_string)
    return dt.strftime("%I:%M %p")


# ============================================
# Hour Formatting
# ============================================

def format_hour(time_string):
    dt = datetime.fromisoformat(time_string)
    return dt.strftime("%I %p")


# ============================================
# Day Formatting
# ============================================

def format_day(date_string):
    dt = datetime.strptime(date_string, "%Y-%m-%d")
    return dt.strftime("%A")


# ============================================
# Get Coordinates
# ============================================

def get_coordinates(city):

    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data:
        return None

    result = data["results"][0]

    return {
        "city": result["name"],
        "country": result["country"],
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }


# ============================================
# Continue in Part 2
# ============================================
# ============================================
# Current Weather + Forecast + Hourly
# ============================================

def get_current_weather(lat, lon):

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}"
        f"&longitude={lon}"
        "&current="
        "temperature_2m,"
        "relative_humidity_2m,"
        "apparent_temperature,"
        "weather_code,"
        "wind_speed_10m,"
        "surface_pressure"
        "&daily="
        "temperature_2m_max,"
        "temperature_2m_min,"
        "weather_code,"
        "sunrise,"
        "sunset"
        "&hourly="
        "temperature_2m,"
        "weather_code"
        "&forecast_days=7"
        "&timezone=auto"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    current = data["current"]
    daily = data["daily"]
    hourly = data["hourly"]

    weather = {

        "temperature": current["temperature_2m"],

        "feels_like": current["apparent_temperature"],

        "humidity": current["relative_humidity_2m"],

        "pressure": current["surface_pressure"],

        "wind": current["wind_speed_10m"],

        "condition": weather_description(
            current["weather_code"]
        ),

        "icon": weather_icon(
            current["weather_code"]
        ),
            "theme": weather_theme(
        current["weather_code"],
        daily["sunrise"][0],
        daily["sunset"][0]
    ),

    "temp_class": temperature_class(
        current["temperature_2m"]
    ),

        "min_temp": daily["temperature_2m_min"][0],

        "max_temp": daily["temperature_2m_max"][0],

        "sunrise": format_time(
            daily["sunrise"][0]
        ),

        "sunset": format_time(
            daily["sunset"][0]
        ),

        "forecast": [],

        "hourly": []

    }

    # ============================================
    # 7-Day Forecast
    # ============================================

    for i in range(7):

        weather["forecast"].append({

            "day": format_day(
                daily["time"][i]
            ),

            "icon": weather_icon(
                daily["weather_code"][i]
            ),

            "condition": weather_description(
                daily["weather_code"][i]
            ),

            "max_temp": daily["temperature_2m_max"][i],

            "min_temp": daily["temperature_2m_min"][i]

        })

    # ============================================
    # Continue in Part 3
    # ============================================
        # ============================================
    # Hourly Forecast (Next 24 Hours)
    # ============================================

    for i in range(24):

        weather["hourly"].append({

            "time": format_hour(
                hourly["time"][i]
            ),

            "temperature": hourly["temperature_2m"][i],

            "icon": weather_icon(
                hourly["weather_code"][i]
            ),

            "condition": weather_description(
                hourly["weather_code"][i]
            )

        })

    return weather
def get_current_city():
    try:
        g = geocoder.ip("me")

        if g.ok and g.city:
            return g.city

    except Exception:
        pass

    return "Jaipur"
import requests

def get_7day_forecast(latitude, longitude):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min"
        "&timezone=auto"
    )

    try:

        response = requests.get(url)
        data = response.json()

        forecast = []

        dates = data["daily"]["time"]
        max_temp = data["daily"]["temperature_2m_max"]
        min_temp = data["daily"]["temperature_2m_min"]
        codes = data["daily"]["weather_code"]

        for i in range(len(dates)):

            forecast.append({

               "day": format_day(dates[i]),
                "max": max_temp[i],
                "min": min_temp[i],
                "icon": weather_icon(codes[i]),
                "description": weather_description(codes[i])

            })

        return forecast

    except Exception:
        return []
    