from typing import Dict, Any, Literal, List
from mcp_server.mcp_instance import mcp
import logging

from mcp_server.schemas.restaurants_schema import Restaurant, RestaurantResponse

logger = logging.getLogger(__name__)

@mcp.tool(tags={"restaurant"})
def get_restaurant_recommendation(
    destination: str,
    priority: Literal["price", "rating", "balanced"] = "balanced",
) -> Dict[str, Any]:
    """
    Get best restaurant recommendation for a destination.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        priority (str):
            Recommendation priority:
                - "price" → cheapest
                - "rating" → highest rating
                - "balanced" → best rating with reasonable price

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "recommended": Dict | None,
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

    

        best = None

        # -------- PRICE --------
        if priority == "price":

            best = min(
                restaurants,
                key=lambda x : x.get("price_range"),
            )

        # -------- RATING --------
        elif priority == "rating":

            best = max(
                restaurants,
                key=lambda r: r.get("rating", 0),
            )

        # -------- BALANCED --------
        else:

            best = max(
                restaurants,
                key=lambda x: x.get("rating") / (x.get("price_range") + 1)
            )
        

        return RestaurantResponse(
            status="success",
            destination=destination_clean,
            recommended=best
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to recommended restaurants")

        return RestaurantResponse(
            status="error",
            error=f"No restaurants recommended for this destinaton : {destination_clean}",
            error_details=str(e)
        )     