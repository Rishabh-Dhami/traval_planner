from typing import Dict, Any, List, Literal
from mcp_server.mcp_instance import mcp

@mcp.tool(tags={"hotel"})
def get_hotels_by_traveler_type(
    destination: str,
    traveler_type: List[
        Literal[
            "solo",
            "couples",
            "families",
            "groups",
            "business",
            "kids",
            "budget",
            "luxury",
            "long-stay"
        ]
    ]
) -> Dict[str, Any]:
    """
    Get hotels filtered by traveler type.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris")
        traveler_type (List[str]): traveler categories
            allowed:
            solo, couples, families, groups,
            business, kids, budget, luxury, long-stay

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "hotels_count": int | None,
                "hotels": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    #  validation
    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": "",
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    if not traveler_type:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "traveler_type cannot be empty",
            "error_details": None,
        }
    
    destination_clean = destination.strip().lower()

    try:

        hotels: List[Dict[str, Any]] = get_hotels(destination_clean)

        if not hotels:
            return {
                "status": "error",
                "destination": destination_clean,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found for {destination_clean}",
                "error_details": None,
            }

        #filter by traveler type (supports multiple)
        filtered_hotels = [
            hotel
            for hotel in hotels
            if any(
                t.lower() in [x.lower() for x in hotel.get("traveler_type", [])]
                for t in traveler_type
            )
        ]

        if not filtered_hotels:
            return {
                "status": "error",
                "destination": destination_clean,
                "hotels_count": None,
                "hotels": None,
                "error": (
                    f"No hotels found for traveler type "
                    f"{traveler_type} in {destination_clean}"
                ),
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "hotels_count": len(filtered_hotels),
            "hotels": filtered_hotels,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to filter hotels by traveler type",
            "error_details": str(e),
        }