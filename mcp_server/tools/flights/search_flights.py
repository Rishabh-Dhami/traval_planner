from typing import Dict, List, Any, Optional
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.flights_schema import Flight, FlightResponse
from mcp_server.utils import get_flights
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"flight"})
def search_flights(
    destination: str,
    budget_max: Optional[int] = None,
    preferred_stops: str = "any",
) -> Dict[str, Any]:
    """
    Search for available flights to a destination.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris")
        budget_max (Optional[int]): Maximum budget per person in USD.
        preferred_stops (str): "direct", "one-stop", or "any".

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
            status="error",
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
                error=f"No flight found for this destination: {destination_clean}"
            ).model_dump(by_alias=True)

        # filter by budget
        if budget_max is not None:
            flights = [
                f for f in flights
                if f.price <= budget_max
            ]

        # filter by stops
        if preferred_stops == "direct":
            flights = [f for f in flights if f.stops == 0]

        elif preferred_stops == "one-stop":
            flights = [f for f in flights if f.stops == 1]

        if not flights:
            return FlightResponse(
                status="error",
                destination=destination_clean,
                error="No flights match your criteria"
            ).model_dump(by_alias=True)

        return FlightResponse(
            status="success",
            destination=destination_clean,
            flight_count=len(flights),
            flights=flights
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning("Failed to search flights")
        return FlightResponse(
            status="error",
            error=f"Failed to search flight for this destinaton: {destination_clean}",
            error_details=str(e)
        )


