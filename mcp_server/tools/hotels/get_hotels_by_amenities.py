from typing import Dict, Any, List, Literal
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.hotels_schema import Hotel, HotelResponse
from mcp_server.utils import get_hotels
import logging

logger = logging.getLogger(__name__)

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
        return HotelResponse(
            status="error",
            destination=destination,
            error="Destination is required"
        ).model_dump(by_alias=True)

    destination_clean = destination.strip().lower()

    if not amentities:
        return HotelResponse(
            status="error",
            destination=destination,
            error="Amentities are required"
        ).model_dump(by_alias=True)

    try:
        raw_hotels: List[Dict[str, Any]] = get_hotels(destination_clean)

        hotels: List[Hotel] = []
        for a in raw_hotels:
            try:
                hotels.append(Hotel.model_validate(a))
            except Exception as e:
                logger.warning(f"Invalid hotel skipped: {a} | Error: {e}")
        
        if not hotels:
            return HotelResponse(
                status="error",
                destination=destination_clean,
                error=f"No hotels found for '{destination_clean}'"
            ).model_dump(by_alias=True)
        
        filtered_hotels = [
            hotel for hotel in hotels if any(
                t.lower() in [x.lower() for x in hotel.get("amenities", [])] 
                for t in amentities
            )
        ]

        if not filtered_hotels:
            return HotelResponse(
                status="error",
                destination=destination_clean,
                error=f"No hotels found by amentities' {amentities}'"
            ).model_dump(by_alias=True)

        return HotelResponse(
            status="success",
            destination=destination_clean,
            hotels=filtered_hotels,
            hotel_count=len(filtered_hotels)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to fetch hotel by amentities")
        return HotelResponse(
            status="error",
            destination=destination_clean,
            error=f"No hotels found by amentities:{amentities} for '{destination_clean}'"
        ).model_dump(by_alias=True)