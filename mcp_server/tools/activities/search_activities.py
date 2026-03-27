from typing import Dict, Any, List
from mcp_server.mcp_instance import mcp

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
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Destination is required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    if not destination_clean:
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    try:
        activities: List[Dict[str, Any]] = get_activities(destination_clean)

        if not activities:
            return {
                "status": "error",
                "destination": destination_clean,
                "activities_count": 0,
                "activities": [],
                "error": f"No activities found for '{destination_clean}'",
                "error_details": None,
            }

        
        return {
            "status": "success",
            "destination": destination_clean,
            "activities_count": len(activities),
            "activities": activities,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "activities_count": None,
            "activities": None,
            "error": "Internal error while searching activities",
            "error_details": str(e),
        }