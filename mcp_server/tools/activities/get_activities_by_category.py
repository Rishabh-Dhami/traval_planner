from typing import Dict, Any, List, Union
from mcp_server.mcp_instance import mcp

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
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if not category:
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Category is required",
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
            return {
                "status": "error",
                "destination": destination_clean,
                "activities_count": None,
                "activities": None,
                "error": f"No activities found for category {category}",
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
            "error": "Failed to fetch activities",
            "error_details": str(e),
        }