from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp
import logging

from mcp_server.schemas.restaurants_schema import Restaurant, RestaurantResponse
from mcp_server.utils import get_restaurants

logger = logging.getLogger(__name__)

@mcp.tool(tags={"restaurant"})
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
        return RestaurantResponse(
            status="error",
            destination=destination,
            error="Destination is required"
        ).model_dump(by_alias=True)

    if rating is None or rating < 0:
        return RestaurantResponse(
            status="error",
            destination=destination,
            error="Rating must be > 0"
        ).model_dump(by_alias=True)

    destination_clean = destination.strip().lower()

    try:
        raw_restaurants: List[Dict[str, Any]] = get_restaurants(destination_clean)

        restaurants: List[Restaurant] = []
        for a in raw_restaurants:
            try:
                restaurants.append(Restaurant.model_validate(a))
            except Exception as e:
                logger.warning(f"Invalid restaurant skipped: {a} | Error: {e}")
        
        if not restaurants:
            return RestaurantResponse(
                status="error",
                destination=destination_clean,
                error=f"No restaurants found for '{destination_clean}'"
            ).model_dump(by_alias=True)

        filtered_restaurants = [
            res for res in restaurants
            if isinstance(res.get("rating"), (int, float))
            and res.get("rating", 0) >= rating
        ]

        if not filtered_restaurants:
            return RestaurantResponse(
                status="error",
                destination=destination_clean,
                error="No restaurants match by rating"
            ).model_dump(by_alias=True)

        return RestaurantResponse(
            status="success",
            destination=destination_clean,
            restaurants=filtered_restaurants,
            restaurant_count=len(filtered_restaurants)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to search restaurant by rating critirea")
        return RestaurantResponse(
            status="error",
            destination=destination_clean,
            error=f"No restaurants found by rating for '{destination_clean}'"
        ).model_dump(by_alias=True)