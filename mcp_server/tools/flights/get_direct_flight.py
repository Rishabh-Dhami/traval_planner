from typing import Dict, List, Any
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["flight"])
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