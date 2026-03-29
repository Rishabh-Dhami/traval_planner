import logging
from typing import Dict, Any, List, Union
from mcp_server.mcp_instance import mcp
from mcp_server.schemas.activities_schema import Activity, ActivityResponse
from mcp_server.utils import get_activities

logger = logging.getLogger(__name__)

@mcp.tool(tags={"activity"})
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


    if not destination or not destination.strip():
         return ActivityResponse(
            status="error",
            destination=destination,
            error="Destination is required"
        ).model_dump(by_alias=True)

    if not best_for_tags:
         return ActivityResponse(
            status="error",
            destination=destination,
            error="Tags are required"
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
            return  ActivityResponse(
                status="error",
                destination=destination_clean,
                error=f"No acivity found by interest"
            ).model_dump(by_alias=True)

        return ActivityResponse(
            status="success",
            destination=destination_clean,
            activities=filtered_activities,
            activity_count=len(filtered_activities)
        ).model_dump(by_alias=True)

    except Exception as e:
        logger.warning(f"Failed to fetch activities by interest")

        return ActivityResponse(
            status="error",
            error=f"No activities found by interedt/tags for this destinaton : {destination_clean}",
            error_details=str(e)
        )   