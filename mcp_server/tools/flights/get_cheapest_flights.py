from typing import Dict, List, Any
from mcp_server.mcp_instance import mcp
from mcp_server.utils import get_flights
from schemas.flights_schema import  Flight, FlightResponse
import logging


logger = logging.getLogger(__name__)

@mcp.tool(tags={"flight"})
def get_cheapest_flight(
    destination: str
) -> Dict[str, Any]:
    """
    Get the cheapest available flight to the destination.

    Args:
        destination (str): Destination city (e.g., "paris", "tokyo").

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                cheapest": Dict[str, Any] | None,
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

        if not flights:
            return FlightResponse(
                status="error",
                destination=destination_clean,
                error="No valid flights available",
            ).model_dump(by_alias=True)

        # 🔹 3. Business logic
        cheapest = min(flights, key=lambda f: f.price)

        # 🔹 4. Return SAME schema
        return FlightResponse(
            status="success",
            destination=destination_clean,
            cheapest=cheapest,
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.exception("Failed to get cheapest flight")

        return FlightResponse(
            status="error",
            destination=destination_clean,
            error="Failed to get cheapest flight",
            error_details=str(e),
        ).model_dump(by_alias=True)