from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.hotels_schema import Hotel, HotelResponse
from mcp_server.utils import get_hotels
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"hotel"})
def search_hotels(
    destination: str
) -> Dict[str, Any]:
    """
    Search for available hotels in a destination.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris").

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

        return HotelResponse(
            status="error",
            destination=destination_clean,
            hotels=hotels,
            hotel_count=len(hotels)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to search hotel")
        return HotelResponse(
            status="error",
            destination=destination_clean,
            error=f"No hotels found for '{destination_clean}'"
        ).model_dump(by_alias=True)