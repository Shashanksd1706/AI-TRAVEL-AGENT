import json
import os
from functools import lru_cache
from typing import List, Dict, Any, Optional

from langchain.tools import tool

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "places.json")

@lru_cache(maxsize=1)
def _load_places() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def search_places(
    city: str,
    category: Optional[str] = None,
    max_entry_fee: Optional[int] = None,
) -> List[Dict[str, Any]]:
    places = _load_places()
    result = []
    for p in places:
        if p.get("city", "").lower() != city.lower():
            continue
            
        # FIX: JSON uses "type", tool uses "category"
        place_type = p.get("type", "").lower()
        if category and category.lower() not in place_type:
            continue
            
        # FIX: JSON is missing "entry_fee", assume 0 if missing
        entry_fee = p.get("entry_fee", 0)
        if max_entry_fee is not None and entry_fee > max_entry_fee:
            continue
            
        result.append(p)
    return result

@tool("search_places", return_direct=False)
def search_places_tool(
    city: str,
    category: str = "",
    max_entry_fee: int = 100000,
) -> str:
    """
    List sightseeing places in a city filtered by category.
    """
    kwargs = {"city": city}
    if category:
        kwargs["category"] = category
    if max_entry_fee is not None:
        kwargs["max_entry_fee"] = max_entry_fee
        
    places = search_places(**kwargs)
    if not places:
        return f"No places found in {city} with the given filters."
        
    lines = []
    for p in places:
        # FIX: Handle missing keys safely
        place_id = p.get("place_id", "N/A")
        name = p.get("name", "Unknown")
        p_type = p.get("type", "General")
        rating = p.get("rating", "N/A")
        
        # Add artificial defaults for fields missing in JSON
        lines.append(
            f"{place_id}: {name} ({p_type}), Rating: {rating}, "
            f"Entry: {p.get('entry_fee', 0)}, "
            f"Typical stay: 2h" 
        )
    return "\n".join(lines)