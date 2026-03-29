from typing import Dict, Any, List, Literal, Union
from mcp_server.mcp_instance import mcp
import logging

from mcp_server.schemas.restaurants_schema import Restaurant, RestaurantResponse
from mcp_server.utils import get_restaurants

logger = logging.getLogger(__name__)

@mcp.tool(tags={"restaurant"})
def get_restaurants_by_tags(
    destination: str,
    tags: Union[
        str,
        List[
            Literal[
                "special occasion",
                "sushi lovers",
                "solo dining",
                "late night",
                "budget",
                "groups",
                "atmosphere",
                "tourists",
                "lunch",
                "healthy",
                "quick meal",
                "fine dining",
                "foodies",
            ]
        ],
    ],
) -> Dict[str, Any]:
    """
    Get available restaurants for a destination filtered by tags.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        tags (str | List[str]):
            Tag or list of tags.

            Examples:
                "budget"
                ["budget", "late night"]

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

    if not tags:
        return RestaurantResponse(
            status="error",
            destination=destination,
            error="Tags are required"
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

        # normalize tags → always list
        if isinstance(tags, str):
            tags_list = [tags.lower().strip()]
        else:
            tags_list = [t.lower().strip() for t in tags]

        filtered_restaurants = [
            res
            for res in restaurants
            if any(
                tag in [x.lower() for x in res.get("best_for", [])]
                for tag in tags_list
            )
        ]

        if not filtered_restaurants:
            return RestaurantResponse(
                status="error",
                destination=destination_clean,
                error="No restaurants match by tags"
            ).model_dump(by_alias=True)

        return RestaurantResponse(
            status="success",
            destination=destination_clean,
            restaurants=filtered_restaurants,
            restaurant_count=len(filtered_restaurants)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to search restaurant by tags")
        return RestaurantResponse(
            status="error",
            destination=destination_clean,
            error=f"No restaurants found by tags for '{destination_clean}'"
        ).model_dump(by_alias=True)