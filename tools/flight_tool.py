import json
import os
from functools import lru_cache
from typing import List, Dict, Any, Optional

from langchain.tools import tool   # you can keep this even if not used yet

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "flights.json",
)

@lru_cache(maxsize=1)
def _load_flights() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def search_flights(
    from_city: str,
    to_city: str,
    max_price: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Pure Python helper used by planner_agent."""
    flights = _load_flights()
    result = []
    for f in flights:
        if f.get("from", "").lower() != from_city.lower():
            continue
        if f.get("to", "").lower() != to_city.lower():
            continue
        price = f.get("price")
        if max_price is not None and isinstance(price, (int, float)) and price > max_price:
            continue
        result.append(f)
    return result

@tool("search_flights", return_direct=False)
def search_flights_tool(from_city: str, to_city: str, max_price: int = 999999) -> str:
    """
    (Optional) Tool wrapper for future agentic version.
    Finds flights between two cities under a maximum price.
    """
    flights = search_flights(from_city=from_city, to_city=to_city, max_price=max_price)
    if not flights:
        return f"No flights found from {from_city} to {to_city} under {max_price}."

    lines = []
    for f in flights:
        lines.append(
            f"{f.get('flight_id')}: {f.get('airline')} "
            f"{f.get('from')} -> {f.get('to')}, "
            f"{f.get('departure_time')} -> {f.get('arrival_time')}, "
            f"price {f.get('price')}"
        )
    return "\n".join(lines)
