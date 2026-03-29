from typing import Any, Dict, List

from mcp_server.mcp_instance import mcp
from mcp_server.schemas.flights_schema import Flight, FlightResponse
from mcp_server.utils import get_flights, parse_duration_to_hours
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"flight"})
def compare_flights(
    destination: str,
) -> Dict[str, Any]:
    """
    Compare available flights for a destination.

    Args:
        destination (str): Destination city

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "flight_count": int | None,
                "flights": List[dict] | None,
                "cheapest": dict | None,
                "fastest": dict | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return FlightResponse(
            status="error",
            destination=destination,
            error="Destination cannot be empty",
        ).model_dump(by_alias=True)
    
    destination_clean = destination.strip().lower()
    try:
        raw_flights: List[Dict[str, Any]] = get_flights(destination_clean)

        if not raw_flights:
            return FlightResponse(
                status="error",
                destination=destination_clean,
                error=f"No flights found for {destination_clean}",
            ).model_dump(by_alias=True)

        flights: List[Flight] = []
        for f in raw_flights:
            try:
                flights.append(Flight.model_validate(f))
            except Exception as e:
                logger.warning(f"Invalid flight skipped: {f} | Error: {e}")

        cheapest = min(flights, key=lambda f: f.price)

        fastest = min(
            flights,
            key=lambda f: parse_duration_to_hours(f.duration),
        )

        return FlightResponse(
            status="success",
            destination=destination_clean,
            flight_count=len(flights),
            flights=flights,
            cheapest=cheapest,
            fastest=fastest,
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to compare flights")    
        return FlightResponse(
            status="error",
            destination=destination_clean,
            error=f"Failed to compare flights for this destination: {destination_clean}",
            error_details=str(e),
        ).model_dump(by_alias=True)
