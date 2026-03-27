from fastmcp import FastMCP
from typing import Dict, Optional, Any, List


mcp = FastMCP("flights")

@mcp.tool()
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


