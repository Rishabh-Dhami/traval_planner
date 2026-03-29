from typing import Dict, Any, List, Optional
from mcp_server.mcp_instance import mcp
import logging

from mcp_server.schemas.restaurants_schema import Restaurant, RestaurantResponse
from mcp_server.utils import get_restaurants

logger = logging.getLogger(__name__)

@mcp.tool(tags={"restaurant"})
def get_restaurants_filtered(
    destination: str,
    cuisine: Optional[str] = None,
    price_range: Optional[str] = None,
    min_rating: Optional[float] = None,
    neighborhood: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Get restaurants using multiple filters.

    Args:
        destination (str):
            Destination city

        cuisine (str, optional):
            Cuisine type (e.g., "sushi", "ramen")

        price_range (str, optional):
            $, $$, $$$, $$$$

        min_rating (float, optional):
            Minimum rating

        neighborhood (str, optional):
            Area name

        tags (List[str], optional):
            best_for tags

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

        filtered_restaurants = restaurants

        # cuisine
        if cuisine:
            filtered_restaurants = [
                r for r in filtered_restaurants
                if cuisine.lower() in r.get("cuisine", "").lower()
            ]

        # price
        if price_range:
            filtered_restaurants = [
                r for r in filtered_restaurants
                if r.get("price_range") == price_range
            ]

        # rating
        if min_rating is not None:
            filtered_restaurants = [
                r for r in filtered_restaurants
                if r.get("rating", 0) >= min_rating
            ]

        # neighborhood
        if neighborhood:
            filtered_restaurants = [
                r for r in filtered_restaurants
                if neighborhood.lower()
                in r.get("neighborhood", "").lower()
            ]

        # tags
        if tags:
            tags_lower = [t.lower() for t in tags]

            filtered_restaurants = [
                r for r in filtered_restaurants
                if any(
                    t in [x.lower() for x in r.get("best_for", [])]
                    for t in tags_lower
                )
            ]

        if not filtered_restaurants:
            return RestaurantResponse(
                status="error",
                destination=destination_clean,
                error="No restaurants match filter"
            ).model_dump(by_alias=True)

        return RestaurantResponse(
            status="success",
            destination=destination_clean,
            restaurants=filtered_restaurants,
            restaurant_count=len(filtered_restaurants)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to search restaurant by filtering critirea")
        return RestaurantResponse(
            status="error",
            destination=destination_clean,
            error=f"No restaurants found for '{destination_clean}'"
        ).model_dump(by_alias=True)