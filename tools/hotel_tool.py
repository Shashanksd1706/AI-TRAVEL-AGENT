import json
import os
from functools import lru_cache
from typing import List, Dict, Any, Optional

from langchain.tools import tool

# Ensure this path matches your folder structure
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "hotels.json")

@lru_cache(maxsize=1)
def _load_hotels() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def search_hotels(
    city: str,
    max_price_per_night: Optional[int] = None,
    min_rating: float = 0.0,
    trip_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    hotels = _load_hotels()
    result = []
    for h in hotels:
        # Match city (case-insensitive)
        if h.get("city", "").lower() != city.lower():
            continue
            
        # Filter by price
        if max_price_per_night is not None and h.get("price_per_night", 99999) > max_price_per_night:
            continue
            
        # FIX: The JSON has "stars", not "rating". We use stars as a proxy.
        # If the user asks for min_rating 3.5, we check if stars >= 3.5
        rating = h.get("stars", 0)
        if rating < min_rating:
            continue
            
        # FIX: Your JSON does not have "trip_types". 
        # We skip this filter to avoid filtering out all results.
        # if trip_type and ... (Removed logic)
        
        result.append(h)
    return result

@tool("search_hotels", return_direct=False)
def search_hotels_tool(
    city: str,
    max_price_per_night: int = 10000,
    min_rating: float = 3.5,
    trip_type: str = "Leisure",
) -> str:
    """
    Find hotels in a city filtered by price, rating, and trip type.
    """
    hotels = search_hotels(
        city=city,
        max_price_per_night=max_price_per_night,
        min_rating=min_rating,
        trip_type=trip_type,
    )
    if not hotels:
        return f"No hotels found in {city} under {max_price_per_night}."
        
    lines = []
    for h in hotels:
        # FIX: Access correct keys from hotels.json
        lines.append(
            f"{h.get('hotel_id')}: {h.get('name')} ({h.get('stars')}★) in {h.get('city')}, "
            f"price/night {h.get('price_per_night')}, "
            f"amenities={','.join(h.get('amenities', []))}"
        )
    return "\n".join(lines)