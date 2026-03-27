from typing import Dict, List, Any
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["flight"])
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
