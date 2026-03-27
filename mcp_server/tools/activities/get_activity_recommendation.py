from typing import Dict, Any, List, Literal
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["activity"])
def get_activity_recommendation(
    destination: str,
    priority: Literal["price", "rating", "balanced"] = "balanced"
) -> Dict[str, Any]:
    """
    Return best activity based on priority:
    price / rating / balanced

    Args:
        destination (str):
            Destination city (e.g., "tokyo", "paris")

        priority (str):
            price → cheapest activity
            rating → highest rating
            balanced → good rating + low price

    Returns:
        Dict[str, Any]
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "activity": None,
            "error": "Destination is required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        activities: List[Dict[str, Any]] = get_activities(destination_clean)
        if not activities:
            return {
                "status": "error",
                "destination": destination_clean,
                "activity": None,
                "error": f"No activities found for {destination_clean}",
                "error_details": None,
            }

        

        

        # ---------- choose based on priority ----------

        if priority == "price":

            best = min(
                activities,
                key=lambda x: x["price"]
            )

        elif priority == "rating":

            best = max(
                activities,
                key=lambda x: x["rating"]
            )

        else:  # balanced

            # score = rating / price
            best = max(
                activities,
                key=lambda x: x["rating"] / (x["price"] + 1)
            )

     

        return {
            "status": "success",
            "destination": destination_clean,
            "priority": priority,
            "activity": best,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "activity": None,
            "error": "Failed to get recommendation",
            "error_details": str(e),
        }