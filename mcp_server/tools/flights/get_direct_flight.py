from typing import Dict, List, Any
from mcp_server.mcp_instance import mcp
from mcp_server.utils import get_flights
from schemas.flights_schema import Flight, FlightResponse
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"flight"})
def get_direct_flight(
    destination: str
) -> Dict[str, Any]:
    """
    Get direct flights available to the destination.

    Args:
        destination (str): Destination city (e.g., "paris", "tokyo")

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "flight_count": int | None,
                "flights": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return FlightResponse(
            status="success",
            destination=destination,
            error="Destination cannot be empty",
        ).model_dump(by_alias=True)
    
    destination_clean = destination.strip().lower()
    try:
        raw_flights: List[Dict[str, Any]] = get_flights(destination_clean)

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
                error= f"No flight found for this destination: {destination_clean}"
            )

        # filter direct flights safely
        direct_flights = [
            f for f in flights
            if f.get("stops") == 0
        ]

        if not direct_flights:
            return FlightResponse(
                status="error",
                destination=destination_clean,
                error="No direct flight found"
            )

        return FlightResponse(
            status="success",
            destination=destination_clean,
            flight_count=len(direct_flights),
            flights=direct_flights,
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to fecth direct flights")
        return FlightResponse(
            status="error",
            destination=destination_clean,
            error=f"Failed to fetch direct flights for this destination: {destination_clean}",
            error_details=str(e)
        )