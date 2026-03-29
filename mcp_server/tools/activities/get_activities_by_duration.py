import logging
from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.activities_schema import Activity, ActivityResponse
from mcp_server.utils import get_activities, parse_duration_to_hours

logger = logging.getLogger(__name__)

@mcp.tool(tags={"activity"})
def get_activities_by_duration(
    destination: str,
    max_hours: float
) -> Dict[str, Any]:
    """
    Get activities whose duration is less than or equal to max_hours.

    Args:
        destination (str): city name
        max_hours (float): maximum allowed duration in hours

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

    if not max_hours or max_hours < 0:
         return ActivityResponse(
            status="error",
            destination=destination,
            error="Max hour must be > 0"
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

        filtered_activities = []

        for activity in activities:

            duration_text = activity.get("duration", "")

            hours = parse_duration_to_hours(duration_text)

            if hours <= max_hours:
                filtered_activities.append(activity)

        if not filtered_activities:
            return  ActivityResponse(
                status="error",
                destination=destination_clean,
                error=f"No acivity found under {max_hours} hours"
            ).model_dump(by_alias=True)

        return ActivityResponse(
            status="success",
            destination=destination_clean,
            activities=filtered_activities,
            activity_count=len(filtered_activities)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to fetch activities by duration")

        return ActivityResponse(
            status="error",
            error=f"No activities found by duration for this destinaton : {destination_clean}",
            error_details=str(e)
        )   