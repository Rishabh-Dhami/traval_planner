"""
Flight Agent

Description:
This agent is responsible for handling all flight-related queries,
including searching, filtering, comparing, and recommending flights
based on user preferences such as destination, price, duration,
stops, and travel time.

The agent uses mock flight data for development and testing.
In production, this agent can be connected to real flight APIs.

Possible API integrations:
- Amadeus API
- Skyscanner API
- Kiwi API
- Google Flights API
- TravelPayouts API
- Expedia API

Capabilities:
- Search flights by destination
- Find cheapest flight
- Find fastest flight
- Find direct flights
- Compare flights

Supported Tools:

- search_flights
    Search all available flights for a destination.

- get_cheapest_flight
    Return the lowest price flight.

- get_fastest_flight
    Return the shortest duration flight.

- get_direct_flights
    Return flights with no stops.

- compare_flights
    Compare multiple flight options.

Flight Data Fields:

Each flight may contain:

id
airline
departure
arrival
duration
price
currency
stops
destination
origin

Output Format:

All tools return structured JSON responses
with the following fields:

status
destination
flights_count
flights
error
error_details

This allows the agent to be safely used in:

- LangChain agents
- LangGraph multi-agent systems
- Supervisor agents
- Tool routing systems
- Production APIs
- Backend services

Rules:

- Agent must never hallucinate flight data
- Agent must always use tools
- Agent must not modify tool output
- Agent must return structured responses only
- Agent must validate destination before search
- Agent must return error if no flight found

Examples of supported queries:

"find flights to Tokyo"
"cheapest flight to Paris"
"direct flight to Dubai"
"fastest flight available"
"compare flights to London"

Notes:

This agent is designed for multi-agent travel systems
where flights, hotels, and activities are handled
by separate agents coordinated by a supervisor.
"""

import sys
sys.path.insert(0, '../..')

from langchain.agents import create_agent
from langchain.tools import tool
from src.utils import get_flights
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
    destination_clean = destination.strip().lower()
    try:
        flights: List[Dict[str, Any]] = get_flights(destination_clean)

        if not flights:
            return {
                "status": "error",
                "destination": destination_clean,
                "flight_count": None,
                "flights": None,
                "error": f"No flights found for {destination_clean}",
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
                "destination": destination_clean,
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
            "destination": destination_clean,
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
    destination_clean = destination.strip().lower()
    try:
        flights: List[Dict[str, Any]] = get_flights(destination_clean)

        if not flights:
            return {
                "status": "error",
                "destination": destination_clean,
                "cheapest_flight_details": None,
                "error": f"No flights found for destination: {destination_clean}",
                "error_details": None,
            }

        cheapest = min(
            flights,
            key=lambda x: x.get("price", float("inf"))
        )

        

        return {
            "status": "success",
            "destination": destination_clean,
            "cheapest_flight_details": cheapest,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "cheapest_flight_details": None,
            "error": "Failed to get cheapest flight",
            "error_details": str(e),
        }
    
#return flights with no stops
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
    
    destination_clean = destination.strip().lower()
    try:
        flights: List[Dict[str, Any]] = get_flights(destination_clean)

        if not flights:
            return {
                "status": "error",
                "destination": destination_clean,
                "flight_count": None,
                "flights": None,
                "error": f"No flights found for {destination_clean}",
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
                "destination": destination_clean,
                "flight_count": None,
                "flights": None,
                "error": "No direct flights found",
                "error_details": None,
            }

    

        return {
            "status": "success",
            "destination": destination_clean,
            "flight_count": len(direct_flights),
            "flights": direct_flights,
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

#compare available flight options
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
    
    destination_clean = destination.strip().lower()
    try:
        flights: List[Dict[str, Any]] = get_flights(destination_clean)

        if not flights:
            return {
                "status": "error",
                "destination": destination_clean,
                "flight_count": None,
                "flights": None,
                "cheapest": None,
                "fastest": None,
                "error": f"No flights found for {destination_clean}",
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
            "destination": destination_clean,
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


#create a flight agent
def create_flights_agent(model):
    """Create and return flight agent"""
    agent = create_agent(
        model,
        tools=[get_cheapest_flight, get_direct_flight, search_flights, compare_flights],
        system_prompt=FLIGHT_AGENT_PROMPT
    )

    return agent    