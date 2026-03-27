from typing import Dict, Any, Literal
from mcp_server.mcp_instance import mcp

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
            "restaurant": Dict | None,
            "error": str | None,
            "error_details": str | None
        }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurant": None,
            "error": "Destination is required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        restaurants = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurant": None,
                "error": f"No restaurants found for {destination_clean}",
                "error_details": None,
            }

    

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
        

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurant": best,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurant": None,
            "error": "Failed to get restaurant recommendation",
            "error_details": str(e),
        } 