from typing import Dict, Any, List, Literal
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.activities_schema import Activity, ActivityResponse
from mcp_server.utils import get_activities
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"activity"})
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
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "priority": Literal["price", "rating", "balanced"],
            "recommended": Dict[str, Any] | None,
            "error": str | None,
            "error_details": str | None
        }       
    """

    if not destination or not destination.strip():
        return ActivityResponse(
            status="error",
            destination=destination,
            error="Destination is required"
        ).model_dump(by_alias=True)

    destination_clean = destination.strip().lower()

    try:
        raw_activities: List[Dict[str, Any]] = get_activities(destination_clean)

        activities: List[Activity] = []
        for a in raw_activities:
            try:
                activities.append(Activity.model_validate(a))
            except Exception as e:
                logger.warning(f"Invalid activity skipped: {a} | Error: {e}")
        
        if not activities:
            return ActivityResponse(
                status="error",
                destination=destination_clean,
                error=f"No activities found for '{destination_clean}'"
            ).model_dump(by_alias=True)

        
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

        return ActivityResponse(
            status="success",
            destination=destination_clean,
            priority=priority,
            recommended=best
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to recommended activities")

        return ActivityResponse(
            status="error",
            error=f"No activities recommended for this destinaton : {destination_clean}",
            error_details=str(e)
        )      