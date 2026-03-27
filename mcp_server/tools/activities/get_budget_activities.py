from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp

@mcp.tool(tags={"activity"})
def get_budget_activities(
    destination: str,
    budget: int
) -> Dict[str, Any]:
    """
    Get available activities under a given budget.

    Args:
        destination (str):
            Destination city (e.g., "tokyo", "paris")

        budget (int):
            Maximum budget allowed for activity

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
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if budget is None or budget < 0:
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Budget must be >= 0",
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

        

        filtered_activities = [
            activity
            for activity in activities
            if isinstance(activity.get("price"), (int, float))
            and activity.get("price") <= budget
        ]

        if not filtered_activities:
            return {
                "status": "error",
                "destination": destination_clean,
                "activities_count": None,
                "activities": None,
                "error": f"No activities under budget {budget}",
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
            "error": "Failed to filter activities by budget",
            "error_details": str(e),
        }