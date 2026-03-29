from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.hotels_schema import Hotel, HotelResponse
from mcp_server.utils import get_hotels
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"hotel"})
def get_hotels_by_rating(
    destination: str,
    rating: int
) -> Dict[str, Any]:
    """
    Get hotels for a destination filtered by rating.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris").
        rating (int): Minimum hotel rating (e.g., 3, 4, 5).

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

    if rating is None or rating <= 0:
        return HotelResponse(
            status="error",
            destination=destination,
            error="Rating must be >= 0"
        ).model_dump(by_alias=True)
    
    destination_clean = destination.strip().lower()

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

        # filter by rating (>= rating)
        filtered_hotels = [
            hotel for hotel in hotels
            if hotel.get("rating", 0) >= rating
        ]

        if not filtered_hotels:
            return HotelResponse(
                status="error",
                destination=destination_clean,
                error=f"No hotels found by rating' {rating}'"
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
            error=f"No hotels found by rating:{rating} for '{destination_clean}'"
        ).model_dump(by_alias=True)