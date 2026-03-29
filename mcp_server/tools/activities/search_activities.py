from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.activities_schema import Activity, ActivityResponse
from mcp_server.utils import get_activities
import logging

logger = logging.getLogger(__name__)

@mcp.tool(tags={"activity"})
def search_activities(destination: str) -> Dict[str, Any]:
    """
    Search available activities for a destination.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris")

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

        return ActivityResponse(
            status="success",
            destination=destination_clean,
            activities=activities,
            activity_count=len(activities),
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to search activities")

        return ActivityResponse(
            status="error",
            error=f"No activities search found for this destinaton : {destination_clean}",
            error_details=str(e)
        )        