from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp

@mcp.tool(tags={"hotel"})
def get_hotels_by_rating(
    destination: str,
    rating: int
) -> Dict[str, Any]:
    """
    Get hotels for a destination filtered by rating.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris").
        rating (int): Minimum hotel rating (e.g., 3, 4, 5).

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

    if rating is None or rating <= 0:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Rating cannot be empty",
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

        # filter by rating (>= rating)
        hotels_under_rating = [
            hotel for hotel in hotels
            if hotel.get("rating", 0) >= rating
        ]

        if not hotels_under_rating:
            return {
                "status": "error",
                "destination": destination_clean,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found with rating >= {rating}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "hotels_count": len(hotels_under_rating),
            "hotels": hotels_under_rating,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to filter hotels by rating",
            "error_details": str(e),
        }