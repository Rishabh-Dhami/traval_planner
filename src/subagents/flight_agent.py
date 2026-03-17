"""
Flight Agent

This agent is responsible for handling all flight-related queries.

It uses mock flight data to search, compare, and recommend flights
based on user preferences such as price, duration, and stops.

Supported capabilities:
- search_flights → find all available flights for a destination
- get_cheapest_flight → return the lowest price flight
- get_fastest_flight → return the shortest duration flight
- get_direct_flights → return flights with no stops
- compare_flights → compare available flight options

This agent understands natural language queries like:
"find flights to Tokyo"
"cheapest flight to Paris"
"direct flight to Dubai"
"fastest flight available"
"compare flights"
"""

import sys
sys.path.insert(0, '../..')

from langchain.agents import create_agent
from langchain.tools import tool
from src.mock_data.data import get_flights
from typing import Optional, List, Dict, Any
from src.prompts import FLIGHT_AGENT_PROMPT

#----search flights tool----
@tool
def search_flights(
    destination: str,
    budget_max: Optional[int] = None,
    preferred_stops: str = "any",
) -> Dict[str, Any]:
    """
    Search for available flights to a destination.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris")
        budget_max (Optional[int]): Maximum budget per person in USD.
        preferred_stops (str): "direct", "one-stop", or "any".

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "flight_count": int | None,
                "flights": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "flight_count": None,
            "flights": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    try:
        flights: List[Dict[str, Any]] = get_flights(destination.lower())

        if not flights:
            return {
                "status": "error",
                "destination": destination,
                "flight_count": None,
                "flights": None,
                "error": f"No flights found for {destination}",
                "error_details": None,
            }

        # filter by budget
        if budget_max is not None:
            flights = [
                f for f in flights
                if f.get("price", float("inf")) <= budget_max
            ]

        # filter by stops
        if preferred_stops == "direct":
            flights = [f for f in flights if f.get("stops") == 0]

        elif preferred_stops == "one-stop":
            flights = [f for f in flights if f.get("stops") == 1]

        if not flights:
            return {
                "status": "error",
                "destination": destination,
                "flight_count": None,
                "flights": None,
                "error": "No flights match your criteria",
                "error_details": None,
            }

        flight_results = []

        for flight in flights:

            layover = flight.get("layover") or "Direct"

            flight_results.append({
                "airline": flight.get("airline"),
                "flight_number": flight.get("flight_number"),
                "departure_city": flight.get("departure_city"),
                "arrival_city": flight.get("arrival_city"),
                "departure_time": flight.get("departure_time"),
                "arrival_time": flight.get("arrival_time"),
                "duration": flight.get("duration"),
                "stops": flight.get("stops"),
                "layover": layover,
                "class": flight.get("class"),
                "price": flight.get("price"),
                "currency": flight.get("currency"),
            })

        return {
            "status": "success",
            "destination": destination,
            "flight_count": len(flight_results),
            "flights": flight_results,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "flight_count": None,
            "flights": None,
            "error": "Failed to search flights",
            "error_details": str(e),
        }


#----get cheapest flight tool----
@tool
def get_cheapest_flight(
    destination: str
) -> Dict[str, Any]:
    """
    Get the cheapest available flight to the destination.

    Args:
        destination (str): Destination city (e.g., "paris", "tokyo").

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "cheapest_flight_details": Dict[str, Any] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "cheapest_flight_details": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    try:
        flights: List[Dict[str, Any]] = get_flights(destination.lower())

        if not flights:
            return {
                "status": "error",
                "destination": destination,
                "cheapest_flight_details": None,
                "error": f"No flights found for destination: {destination}",
                "error_details": None,
            }

        cheapest = min(
            flights,
            key=lambda x: x.get("price", float("inf"))
        )

        cheapest_flight_result = {
            "airline": cheapest.get("airline"),
            "flight_number": cheapest.get("flight_number"),
            "departure_city": cheapest.get("departure_city"),
            "arrival_city": cheapest.get("arrival_city"),
            "departure_time": cheapest.get("departure_time"),
            "arrival_time": cheapest.get("arrival_time"),
            "duration": cheapest.get("duration"),
            "stops": cheapest.get("stops"),
            "layover": cheapest.get("layover"),
            "class": cheapest.get("class"),
            "price": cheapest.get("price"),
            "currency": cheapest.get("currency"),
        }

        return {
            "status": "success",
            "destination": destination,
            "cheapest_flight_details": cheapest_flight_result,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "cheapest_flight_details": None,
            "error": "Failed to get cheapest flight",
            "error_details": str(e),
        }
    

@tool
def get_direct_flight(
    destination: str
) -> Dict[str, Any]:
    """
    Get direct flights available to the destination.

    Args:
        destination (str): Destination city (e.g., "paris", "tokyo")

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "flight_count": int | None,
                "flights": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "flight_count": None,
            "flights": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    try:
        flights: List[Dict[str, Any]] = get_flights(destination.lower())

        if not flights:
            return {
                "status": "error",
                "destination": destination,
                "flight_count": None,
                "flights": None,
                "error": f"No flights found for {destination}",
                "error_details": None,
            }

        # filter direct flights safely
        direct_flights = [
            f for f in flights
            if f.get("stops") == 0
        ]

        if not direct_flights:
            return {
                "status": "error",
                "destination": destination,
                "flight_count": None,
                "flights": None,
                "error": "No direct flights found",
                "error_details": None,
            }

        direct_flight_details = []

        for flight in direct_flights:
            direct_flight_details.append({
                "airline": flight.get("airline"),
                "flight_number": flight.get("flight_number"),
                "departure_city": flight.get("departure_city"),
                "arrival_city": flight.get("arrival_city"),
                "departure_time": flight.get("departure_time"),
                "arrival_time": flight.get("arrival_time"),
                "duration": flight.get("duration"),
                "stops": flight.get("stops"),
                "class": flight.get("class"),
                "price": flight.get("price"),
                "currency": flight.get("currency"),
            })

        return {
            "status": "success",
            "destination": destination,
            "flight_count": len(direct_flight_details),
            "flights": direct_flight_details,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "flight_count": None,
            "flights": None,
            "error": "Failed to get direct flights",
            "error_details": str(e),
        }


@tool
def compare_flights(
    destination: str,
) -> Dict[str, Any]:
    """
    Compare available flights for a destination.

    Args:
        destination (str): Destination city

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "flight_count": int | None,
                "flights": List[dict] | None,
                "cheapest": dict | None,
                "fastest": dict | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "flight_count": None,
            "flights": None,
            "cheapest": None,
            "fastest": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    try:
        flights: List[Dict[str, Any]] = get_flights(destination.lower())

        if not flights:
            return {
                "status": "error",
                "destination": destination,
                "flight_count": None,
                "flights": None,
                "cheapest": None,
                "fastest": None,
                "error": f"No flights found for {destination}",
                "error_details": None,
            }

        cheapest = min(
            flights,
            key=lambda x: x.get("price", float("inf"))
        )

        fastest = min(
            flights,
            key=lambda x: x.get(
                "duration_minutes",
                float("inf")
            )
        )

        return {
            "status": "success",
            "destination": destination,
            "flight_count": len(flights),
            "flights": flights,
            "cheapest": cheapest,
            "fastest": fastest,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "flight_count": None,
            "flights": None,
            "cheapest": None,
            "fastest": None,
            "error": "Failed to compare flights",
            "error_details": str(e),
        }

def create_flights_agent(model):
    """Create and return flight agent"""
    agent = create_agent(
        model,
        tools=[get_cheapest_flight, get_direct_flight, search_flights, compare_flights],
        system_prompt=FLIGHT_AGENT_PROMPT
    )

    return agent    