from typing import Dict, Any, List, Literal
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.hotels_schema import Hotel, HotelResponse
from mcp_server.utils import get_hotels
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"hotel"})
def get_hotel_recommendation(
    destination: str,
    priority: Literal["price", "rating", "balanced"] = "balanced"
) -> Dict[str, Any]:
    """
    Get personalized hotel recommendation.

    Args:
        destination (str)
        traveler_type (str)
        priority: "price" | "rating" | "balanced"

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "recommended": List[dict] | None,
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
                logger.warning(f"Invalid Hotel skipped: {a} | Error: {e}")
        
        if not hotels:
            return HotelResponse(
                status="error",
                destination=destination_clean,
                error=f"No hotels found for '{destination_clean}'"
            ).model_dump(by_alias=True)

        
        # ---------- choose based on priority ----------

        if priority == "price":

            best = min(
                hotels,
                key=lambda x: x["price"]
            )

        elif priority == "rating":

            best = max(
                hotels,
                key=lambda x: x["rating"]
            )

        else:  # balanced

            # score = rating / price
            best = max(
                hotels,
                key=lambda x: x["rating"] / (x["price"] + 1)
            )

        return HotelResponse(
            status="success",
            destination=destination_clean,
            recommended=best
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to recommended hotels")

        return HotelResponse(
            status="error",
            error=f"No hotels recommended for this destinaton : {destination_clean}",
            error_details=str(e)
        )      