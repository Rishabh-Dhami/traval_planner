from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp

@mcp.tool(tags={"restaurant"})
def search_restaurants(
    destination: str
) -> Dict[str, Any]:
    """
    Search available restaurants for a destination.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "restaurants_count": int | None,
            "restaurants": List[Dict[str, Any]] | None,
            "error": str | None,
            "error_details": str | None
        }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination is required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        restaurants: List[Dict[str, Any]] = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found for destination: {destination_clean}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurants_count": len(restaurants),
            "restaurants": restaurants,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurants_count": None,
            "restaurants": None,
            "error": f"Failed to search restaurants for destination: {destination_clean}",
            "error_details": str(e),
        }
    