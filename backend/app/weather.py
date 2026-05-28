"""
Weather integration for Colibasi, Giurgiu using Open-Meteo.
"""

import json
from urllib.parse import urlencode
from urllib.request import urlopen


LOCATION = {
    "name": "Colibasi, Giurgiu",
    "latitude": 44.2022,
    "longitude": 26.1947,
    "timezone": "Europe/Bucharest",
}

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def _first(values):
    if not values:
        return None
    return values[0]


def fetch_current_weather():
    query = urlencode({
        "latitude": LOCATION["latitude"],
        "longitude": LOCATION["longitude"],
        "timezone": LOCATION["timezone"],
        "forecast_days": 1,
        "current": "temperature_2m,weather_code",
        "daily": "temperature_2m_min,temperature_2m_max,sunrise,sunset",
    })

    with urlopen(f"{OPEN_METEO_FORECAST_URL}?{query}", timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    current = data.get("current", {})
    daily = data.get("daily", {})
    current_units = data.get("current_units", {})
    daily_units = data.get("daily_units", {})
    weather_code = current.get("weather_code")

    return {
        "status": "ok",
        "location": LOCATION,
        "temperature": current.get("temperature_2m"),
        "temperature_unit": current_units.get("temperature_2m", "C"),
        "condition": WEATHER_CODES.get(weather_code, "Unknown"),
        "weather_code": weather_code,
        "today": {
            "date": _first(daily.get("time")),
            "min_temperature": _first(daily.get("temperature_2m_min")),
            "max_temperature": _first(daily.get("temperature_2m_max")),
            "temperature_unit": daily_units.get("temperature_2m_min", "C"),
            "sunrise": _first(daily.get("sunrise")),
            "sunset": _first(daily.get("sunset")),
        },
        "source": "open-meteo",
    }
