from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Ensure these imports work based on your folder structure. 
# If running from root, these should work.
from config import OPENAI_API_KEY, DEFAULT_MODEL
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.place_tool import search_places
from tools.weather_tool import get_current_weather

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=DEFAULT_MODEL,
    temperature=0.4,
)

SYSTEM_PROMPT = """
You are an AI travel planner.

You receive:
- User's natural language request.
- Structured flight options, hotel options, and places (already pre-selected by Python).
- Weather info.

Task:
- Create a realistic day-wise itinerary.
- Respect budget and preferences.
- Choose one flight and one hotel from the options provided.
- Use suitable places for each day.
- Output sections: Trip Summary, Flight, Hotel, Day-wise Plan, Estimated Cost, Reasoning.
"""

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{planner_input}"),
    ]
)

def _format_options(title: str, rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return f"{title}: none found (check budget/availability).\n"
    lines = [f"{title}:"]
    for r in rows:
        lines.append(str(r))
    return "\n".join(lines) + "\n"

def plan_trip_with_agent(
    user_request: str,
    origin: str,
    destination: str,
    days: int,
    total_budget: int,
    trip_type: str,
) -> str:
    
    # 1) Call Python tools directly
    # Relaxed budget logic slightly to ensure we get results
    max_flight_price = int(total_budget * 0.50) 
    flights = search_flights(origin, destination, max_price=max_flight_price)

    # Calculate max hotel price per night. 
    # Logic: Allocating ~40% of budget to hotels, divided by nights.
    max_hotel_price = int((total_budget * 0.40) / max(days, 1))
    
    hotels = search_hotels(
        city=destination,
        max_price_per_night=max_hotel_price,
        min_rating=3.0, # Lowered slightly to capture 3-star hotels
        trip_type=trip_type,
    )

    places = search_places(destination)

    # Safe weather call
    try:
        weather = get_current_weather(destination)
        weather_text = (
            f"Weather in {weather.get('city', destination)}: "
            f"{weather.get('temp_c')}°C, {weather.get('condition')}."
            if weather.get("temp_c") is not None
            else "Weather information unavailable."
        )
    except Exception:
        weather_text = "Weather information unavailable (service error)."

    # 2) Build a single prompt with all structured data
    planner_input = (
        f"User request:\n{user_request}\n\n"
        f"Origin: {origin}\nDestination: {destination}\n"
        f"Days: {days}\nTotal budget: {total_budget} INR\n"
        f"Trip type: {trip_type}\n"
        f"{weather_text}\n\n"
        f"{_format_options('Flight options', flights)}\n"
        f"{_format_options('Hotel options', hotels)}\n"
        f"{_format_options('Place options', places)}\n"
        "Now choose the best flight, hotel, and plan each day using these options."
    )

    chain = PROMPT | llm
    resp = chain.invoke({"planner_input": planner_input})
    return resp.content