AI-based Travel Planner Agent
An agentic AI travel planning assistant built with Python, LangChain, OpenAI, and Streamlit. The app generates day-wise itineraries using curated JSON datasets for flights, hotels, and places, plus live weather data, and exposes everything through an interactive web UI.
​

✨ Features
Collects trip details (origin, destination, days, budget, trip type, preferences) via Streamlit UI.
​

Loads structured flight, hotel, and place information from local JSON files for reproducible, offline-friendly recommendations.
​

Fetches real-time weather for the destination and incorporates it into itinerary design (e.g., outdoor activities in good weather slots).
​

Generates a coherent, day-wise itinerary using an OpenAI chat model, including trip summary, selected flight and hotel, activities per day, and rough cost breakdown.
​

Modular architecture: tools for data access, a planner module, and a minimal but extensible Streamlit frontend.

🏗️ Project Structure

AI_TRAVEL_AGENT/
├── app.py                 # Streamlit entry point
├── config.py              # API keys and global config
├── requirements.txt       # Python dependencies
├── .env                   # Local environment variables (NOT committed)
├── .gitignore             # Git ignore rules
├── data/
│   ├── flights.json       # Sample flight data
│   ├── hotels.json        # Sample hotel data
│   └── places.json        # Sample sightseeing/activity data
└── tools/
    ├── __init__.py
    ├── agent/
    │   └── planner_agent.py   # High-level planning logic
    ├── flight_tool.py         # Flight search helpers
    ├── hotel_tool.py          # Hotel search helpers
    ├── place_tool.py          # Place search helpers
    └── weather_tool.py        # OpenWeather integration

This layout follows common patterns for Streamlit + LLM applications with separate modules for tools and planning logic.
​

🚀 Getting Started (Local)
Clone the repo
git clone https://github.com/<your-username>/AI_TRAVEL_AGENT.git
cd AI_TRAVEL_AGENT

Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Set environment variables

Create a .env file in the project root:
OPENAI_API_KEY=your_openai_key_here
OPENWEATHER_API_KEY=your_openweather_key_here

config.py loads these values so the app can call both the OpenAI and weather APIs.
​

Run the app
streamlit run app.py

Open the URL shown in the terminal (typically http://localhost:8501) and start planning trips.

🌐 Deployment (Streamlit Cloud)
Push the project to GitHub as a public or private repository.
​

On Streamlit Cloud, create a new app and point it to this repo and app.py as the entry file.
​

In the app’s Secrets settings, add:
OPENAI_API_KEY = "your_openai_key_here"
OPENWEATHER_API_KEY = "your_openweather_key_here"

The same config.py works both locally (via .env) and in the cloud (via Streamlit secrets).
​

🔍 How It Works (High Level)
The user provides trip parameters in the sidebar and a natural-language request in the chat box.
​

The planner module:

Filters flights, hotels, and places from the JSON datasets based on city, budget, ratings, and trip type.

Retrieves current weather for the destination city.
​

Builds a structured prompt that includes all of this context and sends it to an OpenAI chat model via LangChain.
​

The model returns a formatted itinerary which the app displays within the chat interface.

📂 Data Files
The data/ directory contains small, human-readable JSON files, for example:

flights.json: records with fields such as flight_id, from, to, departure_time, arrival_time, price, and airline.
​

hotels.json: records with hotel_id, city, name, area, stars, price_per_night, rating, and amenities.

places.json: records with place_id, city, name, category, typical_stay_hours, entry_fee, and best_time_of_day.

You can extend or replace these files with your own curated datasets.

🧩 Tech Stack
Language: Python 3.10+

LLM: OpenAI chat models, accessed via LangChain.
​

Frontend: Streamlit for chat-style UI.
​

Weather API: OpenWeather current weather endpoint.
​

✅ Roadmap / Possible Extensions
Add multi-city itineraries and round-trip flight logic.
​

Introduce true tool-calling agent workflows once the LangChain agents API is stable in your environment.
​

Hook into real travel APIs (Skyscanner, Amadeus, Booking, Google Places) instead of static JSON data.
​

Add evaluation metrics and user feedback collection for itinerary quality.
