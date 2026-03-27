from typing import Dict, Any
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["restaurant"])
def get_restaurants_by_rating(
    destination: str,
    rating: float
) -> Dict[str, Any]:
    """
    Get available restaurants for a destination filtered by rating.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        rating (float):
            Minimum rating required (e.g., 3.5, 4.0, 4.5)

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

    if rating is None or rating < 0:
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Rating must be >= 0",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        restaurants = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found for destination: {destination_clean}",
                "error_details": None,
            }

        filtered_restaurants = [
            res for res in restaurants
            if isinstance(res.get("rating"), (int, float))
            and res.get("rating", 0) >= rating
        ]

        if not filtered_restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found with rating >= {rating}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurants_count": len(filtered_restaurants),
            "restaurants": filtered_restaurants,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Failed to filter restaurants by rating",
            "error_details": str(e),
        }