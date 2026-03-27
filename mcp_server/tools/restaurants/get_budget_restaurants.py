from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["restaurant"])
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
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if budget is None:
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Budget must be required",
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
            if isinstance(res.get("price_range"), (int, float))
            and res.get("price_range") <= budget
        ]

        if not filtered_restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found with budget <= {budget}",
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
            "error": "Failed to filter restaurants by max budger",
            "error_details": str(e),
        }   
    