
from typing import Dict, Any, List, Union
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["activity"])
def get_activities_by_interest(
    destination: str,
    best_for_tags: Union[str, List[str]]
) -> Dict[str, Any]:
    """
    Get available activities filtered by best_for tags for a destination.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        best_for_tags (str | List[str]):
            One tag or list of tags.
            Example:
                "culture"
                ["history", "shopping"]

    Returns:
        Dict[str, Any]
    """

    # ---------- validation ----------

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if not best_for_tags:
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Tags are required",
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

        

        if isinstance(best_for_tags, str):
            tags_clean = {best_for_tags.lower().strip()}
        else:
            tags_clean = {
                t.lower().strip()
                for t in best_for_tags
            }

        

        filtered_activities = [
            activity
            for activity in activities
            if any(
                tag in [
                    x.lower()
                    for x in activity.get("best_for", [])
                ]
                for tag in tags_clean
            )
        ]

        

        if not filtered_activities:
            return {
                "status": "error",
                "destination": destination_clean,
                "activities_count": None,
                "activities": None,
                "error": f"No activities found for tags: {best_for_tags}",
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
            "error": f"Failed to get activities for tags: {best_for_tags}",
            "error_details": str(e),
        }