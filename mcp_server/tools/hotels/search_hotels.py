from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp

@mcp.tool(tags={"hotel"})
def search_hotels(
    destination: str
) -> Dict[str, Any]:
    """
    Search for available hotels in a destination.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris").

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "hotels_count": int | None,
                "hotels": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }
    
    destination_clean = destination.strip().lower()

    try:
        hotels: List[Dict[str, Any]] = get_hotels(destination_clean)

        if not hotels:
            return {
                "status": "error",
                "destination": destination_clean,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found for {destination_clean}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "hotels_count": len(hotels),
            "hotels": hotels,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to search hotels",
            "error_details": str(e),
        }