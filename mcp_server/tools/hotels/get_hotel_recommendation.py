from typing import Dict, Any, List, Literal
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["hotel"])
def get_hotel_recommendation(
    destination: str,
    traveler_type: str,
    priority: Literal["price", "rating", "balanced"] = "balanced"
) -> Dict[str, Any]:
    """
    Get personalized hotel recommendation.

    Args:
        destination (str)
        traveler_type (str)
        priority: "price" | "rating" | "balanced"

    Returns:
        Dict[str, Any]
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": "",
            "recommendation": None,
            "runner_up": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }
    destination_clean = destination.strip().lower()

    try:

        hotels: List[Dict[str, Any]] = get_hotels(destination_clean)

        if not hotels:
            return {
                "status": "error",
                "destination": destination_clean,
                "recommendation": None,
                "runner_up": None,
                "error": f"No hotels found for {destination_clean}",
                "error_details": None,
            }

        # filter by traveler type
        traveler_type_lower = traveler_type.lower()

        matching_hotels = [
            h for h in hotels
            if traveler_type_lower in h.get("traveler_type", [])
        ]

        if not matching_hotels:
            matching_hotels = hotels


        # sorting logic
        if priority == "price":

            matching_hotels.sort(
                key=lambda x: x.get(
                    "price_per_night",
                    float("inf")
                )
            )

        elif priority == "rating":

            matching_hotels.sort(
                key=lambda x: x.get("rating", 0),
                reverse=True
            )

        else:  # balanced

            matching_hotels.sort(
                key=lambda x:
                x.get("rating", 0)
                / max(x.get("price_per_night", 1), 1),
                reverse=True
            )


        top_pick = matching_hotels[0]

        runner_up = (
            matching_hotels[1]
            if len(matching_hotels) > 1
            else None
        )


        return {
            "status": "success",
            "destination": destination_clean,

            "recommendation": {
                "id": top_pick.get("id"),
                "name": top_pick.get("name"),
                "neighborhood": top_pick.get("neighborhood"),
                "rating": top_pick.get("rating"),
                "reviews": top_pick.get("reviews"),
                "price_per_night": top_pick.get("price_per_night"),
                "currency": top_pick.get("currency"),
                "amenities": top_pick.get("amenities"),
                "description": top_pick.get("description"),
                "traveler_type": top_pick.get("traveler_type"),
            },

            "runner_up": (
                {
                    "id": runner_up.get("id"),
                    "name": runner_up.get("name"),
                    "rating": runner_up.get("rating"),
                    "price_per_night": runner_up.get("price_per_night"),
                }
                if runner_up
                else None
            ),

            "error": None,
            "error_details": None,
        }

    except Exception as e:

        return {
            "status": "error",
            "destination": destination_clean,
            "recommendation": None,
            "runner_up": None,
            "error": "Failed to get recommendation",
            "error_details": str(e),
        }
    