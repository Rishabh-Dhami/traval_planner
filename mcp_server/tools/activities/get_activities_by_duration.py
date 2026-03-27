
from typing import Dict, Any, List
from backend.app.utils import parse_duration_to_hours
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["activity"])
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
        Dict[str, Any]
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if max_hours is None or max_hours <= 0:
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "max_hours must be > 0",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:

        activities: List[Dict[str, Any]] = get_activities(destination_clean)

        if not activities:
            return {
                "status": "error",
                "destination": destination_clean,
                "activities_count": None,
                "activities": None,
                "error": f"No activities found for {destination_clean}",
                "error_details": None,
            }

        filtered_activities = []

        for activity in activities:

            duration_text = activity.get("duration", "")

            hours = parse_duration_to_hours(duration_text)

            if hours <= max_hours:
                filtered_activities.append(activity)

        if not filtered_activities:
            return {
                "status": "error",
                "destination": destination_clean,
                "activities_count": None,
                "activities": None,
                "error": f"No activities under {max_hours} hours",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "activities_count": len(filtered_activities),
            "activities": filtered_activities,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "activities_count": None,
            "activities": None,
            "error": "Failed to filter by duration",
            "error_details": str(e),
        }