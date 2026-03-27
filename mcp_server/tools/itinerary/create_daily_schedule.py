from typing import Dict, Any, List, Literal
from mcp_server.mcp_instance import mcp

@mcp.tool(tags=["itinerary"])
def create_daily_schedule(
    destination: str | None,
    days: int | None,
    hotel_location: str | None,
    activities: List[Dict[str, Any]] | None,
    trip_pace: Literal["relaxed", "moderate", "packed"] | None
) -> Dict[str, Any]:
    """
    Create a day-by-day itinerary schedule for a destination.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        days (int):
            Number of travel days

        hotel_location (str):
            Hotel location / area where user stays

        activities (List[Dict[str, Any]]):
            List of activities selected for the trip

        trip_pace (str):
            Travel pace preference
            Allowed values:
                "relaxed"
                "moderate"
                "packed"

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "days": int | None,
            "trip_pace": str | None,
            "schedule": List[Dict[str, Any]] | None,
            "error": str | None,
            "error_details": str | None
        }
    """
    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "days": None,
            "trip_pace": None,
            "schedule": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if days is None or days <= 0:
        return {
            "status": "error",
            "destination": destination,
            "days": None,
            "trip_pace": None,
            "schedule": None,
            "error": "Days must be > 0",
            "error_details": None,
        }

    if not hotel_location:
        return {
            "status": "error",
            "destination": destination,
            "days": None,
            "trip_pace": None,
            "schedule": None,
            "error": "Hotel location required",
            "error_details": None,
        }

    if trip_pace not in ["relaxed", "moderate", "packed"]:
        return {
            "status": "error",
            "destination": destination,
            "days": None,
            "trip_pace": None,
            "schedule": None,
            "error": "Invalid trip pace e.g relaxed, moderate, packed",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:

        if activities is None:
            activities = []

        if trip_pace == "relaxed":
            per_day = 1
        elif trip_pace == "moderate":
            per_day = 2
        else:
            per_day = 3

        schedule = []
        activity_index = 0

        for day in range(1, days + 1):

            day_plan = []

            for _ in range(per_day):
                if activity_index < len(activities):
                    day_plan.append(activities[activity_index])
                    activity_index += 1

            schedule.append({
                "day": day,
                "hotel": hotel_location,
                "activities": day_plan
            })

        return {
            "status": "success",
            "destination": destination_clean,
            "days": days,
            "trip_pace": trip_pace,
            "schedule": schedule,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "days": None,
            "trip_pace": None,
            "schedule": None,
            "error": "Failed to create schedule",
            "error_details": str(e),
        }