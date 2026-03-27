from typing import Dict, Any, List, Optional
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["restaurant"])
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
        Dict[str, Any]
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination required",
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
                "error": "No restaurants found",
                "error_details": None,
            }

        filtered = restaurants

        # cuisine
        if cuisine:
            filtered = [
                r for r in filtered
                if cuisine.lower() in r.get("cuisine", "").lower()
            ]

        # price
        if price_range:
            filtered = [
                r for r in filtered
                if r.get("price_range") == price_range
            ]

        # rating
        if min_rating is not None:
            filtered = [
                r for r in filtered
                if r.get("rating", 0) >= min_rating
            ]

        # neighborhood
        if neighborhood:
            filtered = [
                r for r in filtered
                if neighborhood.lower()
                in r.get("neighborhood", "").lower()
            ]

        # tags
        if tags:
            tags_lower = [t.lower() for t in tags]

            filtered = [
                r for r in filtered
                if any(
                    t in [x.lower() for x in r.get("best_for", [])]
                    for t in tags_lower
                )
            ]

        if not filtered:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": "No restaurants match filters",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurants_count": len(filtered),
            "restaurants": filtered,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Filtering failed",
            "error_details": str(e),
        }