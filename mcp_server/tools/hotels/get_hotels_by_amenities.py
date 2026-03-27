from typing import Dict, Any, List, Literal
from mcp_server.mcp_instance import mcp

@mcp.tool(tags={"hotel"})
def get_hotels_by_amenities(
    destination: str, 
    amentities : List[
        Literal[
            "Spa",
            "Pool",
            "Gym",
            "Restaurant",
            "Bar",
            "Room Service",
            "Free WiFi",
            "Laundry",
            "Kids Club",
            "Disney Shuttle",
            "Multiple Restaurants",
            "Limousine Service",
            "Kitchen",
            "Washer",
            "Living Area",
            "Michelin Restaurant",
            "Concierge",
            "Courtyard"
        ]
    ]
)-> Dict[str, Any]:
    """
        Get availabel hotels filted by aminities

        Args: 
            destination (str): Destination city (e.g, "tokyo", "paris").
            aminities (List[str] ): Amenities category allowed:
                "Spa", "Pool",
                "Gym",
                "Restaurant",
                "Bar",
                "Room Service",
                "Free WiFi",
                "Laundry",
                "Kids Club",
                "Disney Shuttle",
                "Multiple Restaurants",
                "Limousine Service",
                "Kitchen",
                "Washer",
                "Living Area",
                "Michelin Restaurant",
                "Concierge",
                "Courtyard"

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

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": "",
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    if not amentities:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Amentities cannot be empty",
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
        
        filtered_hotels = [
            hotel for hotel in hotels if any(
                t.lower() in [x.lower() for x in hotel.get("amenities", [])] 
                for t in amentities
            )
        ]

        if not filtered_hotels:
            return {
                "status": "error",
                "destination": destination_clean,
                "hotels_count": None,
                "hotels": None,
                "error": (
                    f"No hotels found for amentity type "
                    f"{amentities} in {destination_clean}"
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
            "error": "Failed to filter hotels by amenities type",
            "error_details": str(e),
        }