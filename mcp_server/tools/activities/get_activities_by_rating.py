from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp
import logging

from mcp_server.schemas.activities_schema import Activity, ActivityResponse
from mcp_server.utils import get_activities

logger = logging.getLogger(__name__)

@mcp.tool(tags={"activity"})
def get_activities_by_rating(
    destination: str,
    rating: float
) -> Dict[str, Any]:
    """
    Get available activities under a given rating.

    Args:
        destination (str):
            Destination city (e.g., "tokyo", "paris")

        raing (float):
            Minimum rating allowed for activity

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

    if rating is None or rating < 0:
         return ActivityResponse(
            status="error",
            destination=destination,
            error="Rating must be >= 0"
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


        

        filtered_activities = [
            activity
            for activity in activities
            if isinstance(activity.get("rating"), (int, float))
            and activity.get("rating") >= rating
        ]

        if not filtered_activities:
            return  ActivityResponse(
                status="error",
                destination=destination_clean,
                error=f"No acivity found by rating {rating}"
            ).model_dump(by_alias=True)

        return ActivityResponse(
            status="success",
            destination=destination_clean,
            activities=filtered_activities,
            activity_count=len(filtered_activities)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to fetch activities by rating")

        return ActivityResponse(
            status="error",
            error=f"No activities found by raing for this destinaton : {destination_clean}",
            error_details=str(e)
        )   