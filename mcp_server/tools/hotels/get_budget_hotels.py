from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp

@mcp.tool(tags={"hotel"})
def get_budget_hotels(
    destination: str,
    budget: int
) -> Dict[str, Any]:
    """
    Filter available hotels under the given budget.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris").
        budget (int): Maximum price per night.

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
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }
    
    destination_clean = destination.strip().lower()

    if budget is None or budget <= 0:
        return {
            "status": "error",
            "destination": destination_clean,
            "hotels_count": None,
            "hotels": None,
            "error": "Budget must be greater than 0",
            "error_details": None,
        }

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

        # filter by budget
        hotels_under_budget = [
            hotel for hotel in hotels
            if hotel.get("price_per_night", float("inf")) <= budget
        ]

        if not hotels_under_budget:
            return {
                "status": "error",
                "destination": destination_clean,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found under budget {budget}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "hotels_count": len(hotels_under_budget),
            "hotels": hotels_under_budget,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to filter hotels by budget",
            "error_details": str(e),
        }