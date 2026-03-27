from typing import Dict, Any, List, Literal, Union
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["restaurant"])
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
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if not tags:
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Tags are required",
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
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found for tags: {tags_list}",
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
            "error": "Failed to filter restaurants by tags",
            "error_details": str(e),
        }