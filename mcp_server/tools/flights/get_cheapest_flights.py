from typing import Dict, List, Any
from mcp_server.mcp_instance import mcp

@mcp.tool(tags={"flight"})
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