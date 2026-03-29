from typing import Dict, Any, List, Union
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.activities_schema import Activity, ActivityResponse
from mcp_server.utils import get_activities
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"activity"})
def get_activities_by_category(
    destination: str,
    category: Union[str, List[str]]
) -> Dict[str, Any]:
    """
    Get available activities filtered by category for a given destination.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        category (str | List[str]):
            Activity category or list of categories.
            Allowed values:
                Culture, Food, Entertainment, Nature, Views

            Examples:
                "Food"
                ["Food", "Culture"]

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "activities_count": int | None,
            "activities": List[Dict[str, Any]] | None,
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

    if not category:
         return ActivityResponse(
            status="error",
            destination=destination,
            error="category is required"
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


        
        if isinstance(category, str):
            category = [category]

        # ---------- normalize ----------

        category_clean = {
            c.lower().strip()
            for c in category
        }

        # ---------- filter ----------

        filtered_activities = [
            activity
            for activity in activities
            if activity.get("category", "").lower()
            in category_clean
        ]

        if not filtered_activities:
            return  ActivityResponse(
                status="error",
                destination=destination_clean,
                error=f"No acivity found by category: {category_clean}"
            ).model_dump(by_alias=True)

        return ActivityResponse(
            status="success",
            destination=destination_clean,
            activities=filtered_activities,
            activity_count=len(filtered_activities)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to fetch activities by category")

        return ActivityResponse(
            status="error",
            error=f"No activities found by category for this destinaton : {destination_clean}",
            error_details=str(e)
        )   