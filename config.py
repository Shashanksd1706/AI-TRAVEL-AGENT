import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY in your .env file")

DEFAULT_MODEL = "gpt-4o-mini"

BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
