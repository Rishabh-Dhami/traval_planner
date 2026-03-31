from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp
import logging

from mcp_server.schemas.restaurants_schema import Restaurant, RestaurantResponse
from mcp_server.utils import get_restaurants

logger = logging.getLogger(__name__)

@mcp.tool(tags={"restaurant"})
def get_budget_restaurants(
    destination: str,
    budget: int
) -> Dict[str, Any]:
    """
    Get available restaurants for a destination filtered by rating.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        Budget (int):
            Maximum budget required (e.g., 3, 343, 2300)

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

    if not budget:
        return RestaurantResponse(
            status="error",
            destination=destination,
            error="Budget is required"
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
            if isinstance(res.get("price_range"), (int, float))
            and res.get("price_range") <= budget
        ]

        if not filtered_restaurants:
            return RestaurantResponse(
                status="error",
                destination=destination_clean,
                error="No restaurants match by budget"
            ).model_dump(by_alias=True)

        return RestaurantResponse(
            status="success",
            destination=destination_clean,
            restaurants=filtered_restaurants,
            restaurant_count=len(filtered_restaurants)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to search restaurant by budget critirea")
        return RestaurantResponse(
            status="error",
            destination=destination_clean,
            error=f"No restaurants found by budget for '{destination_clean}'"
        ).model_dump(by_alias=True) 
    