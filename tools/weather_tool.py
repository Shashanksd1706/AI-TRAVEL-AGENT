import requests
from typing import Dict, Any
from config import OPENWEATHER_API_KEY, BASE_WEATHER_URL

def get_current_weather(city: str) -> Dict[str, Any]:
    """Fetch current weather for a city using OpenWeather."""
    if not OPENWEATHER_API_KEY:
        return {"city": city, "temp_c": None, "condition": "unknown"}

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }
    resp = requests.get(BASE_WEATHER_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    main = data.get("main", {})
    weather = (data.get("weather") or [{}])[0]

    return {
        "city": data.get("name", city),
        "temp_c": main.get("temp"),
        "feels_like_c": main.get("feels_like"),
        "condition": weather.get("description", "unknown"),
    }
