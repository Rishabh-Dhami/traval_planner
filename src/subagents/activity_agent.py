"""
Activity Agent

Description:
This agent is responsible for searching and recommending
travel activities based on destination, category, price,
duration, rating, and user preferences.

The agent uses mock activity data for development and testing.
In production, this agent can be connected to real activity APIs.

Possible API integrations:
- GetYourGuide API
- Viator API
- TripAdvisor API
- Klook API
- Airbnb Experiences API
- Google Travel API

Capabilities:
- Search activities by destination
- Filter activities by category
- Filter activities by budget
- Filter activities by rating
- Filter activities by duration
- Filter activities by user interests
- Get best activity recommendation

Supported Tools:

- search_activities
    Search all activities for a destination.

- get_activities_by_category
    Filter activities by category:
    Culture / Food / Entertainment / Nature / Views

- get_budget_activities
    Return activities under a given price.

- get_activities_by_rating
    Return activities with minimum rating.

- get_activities_by_duration
    Filter activities by duration.

- get_activities_by_interest
    Filter activities by best_for tags:
        culture / food / photography / nightlife /
        families / kids / romantic / art / nature /
        budget / shopping / history / unique

- get_activity_recommendation
    Return best activity based on priority:
    price / rating / balanced

Activity Data Fields:

Each activity contains:

id
name
category
duration
price
currency
rating
description
best_for
location

Output Format:

All tools return structured JSON responses
with the following fields:

status
destination
activities_count
activities
error
error_details

This allows the agent to be safely used in:

- LangChain agents
- LangGraph multi-agent systems
- Supervisor agents
- Tool routing systems
- Production APIs
- Backend services

Rules:

- Agent must never hallucinate activity data
- Agent must always use tools
- Agent must not modify tool output
- Agent must return structured responses only
- Agent must validate destination before search
- Agent must return error if no activity found

Notes:

This agent is designed for multi-agent travel systems
where flights, hotels, and activities, resturents are handled
by separate agents coordinated by a supervisor.
"""


import sys
sys.path.insert(0, '../..')

from langchain.agents import create_agent
from langchain.tools import tool
from src.utils import get_activities, parse_duration_to_hours
from typing import  List, Dict, Any, Literal, Union
from src.prompts import ACTIVITY_AGENT_SYSTEM_PROMPT

@tool
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

@tool
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
@tool
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
@tool
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
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if rating is None or rating < 0:
        return {
            "status": "error",
            "destination": destination,
            "activities_count": None,
            "activities": None,
            "error": "Rating must be >= 0",
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
            if isinstance(activity.get("rating"), (int, float))
            and activity.get("rating") >= rating
        ]

        if not filtered_activities:
            return {
                "status": "error",
                "destination": destination_clean,
                "activities_count": None,
                "activities": None,
                "error": f"No activities under rating {rating}",
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
            "error": "Failed to filter activities by rating",
            "error_details": str(e),
        }
@tool
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
from typing import Dict, Any, List, Union
from langchain.tools import tool


@tool
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

@tool
def get_activity_recommendation(
    destination: str,
    priority: Literal["price", "rating", "balanced"] = "balanced"
) -> Dict[str, Any]:
    """
    Return best activity based on priority:
    price / rating / balanced

    Args:
        destination (str):
            Destination city (e.g., "tokyo", "paris")

        priority (str):
            price → cheapest activity
            rating → highest rating
            balanced → good rating + low price

    Returns:
        Dict[str, Any]
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "activity": None,
            "error": "Destination is required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:

        activities: List[Dict[str, Any]] = get_activities(destination_clean)

        if not activities:
            return {
                "status": "error",
                "destination": destination_clean,
                "activity": None,
                "error": f"No activities found for {destination_clean}",
                "error_details": None,
            }

        

        

        # ---------- choose based on priority ----------

        if priority == "price":

            best = min(
                activities,
                key=lambda x: x["price"]
            )

        elif priority == "rating":

            best = max(
                activities,
                key=lambda x: x["rating"]
            )

        else:  # balanced

            # score = rating / price
            best = max(
                activities,
                key=lambda x: x["rating"] / (x["price"] + 1)
            )

     

        return {
            "status": "success",
            "destination": destination_clean,
            "priority": priority,
            "activity": best,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "activity": None,
            "error": "Failed to get recommendation",
            "error_details": str(e),
        }
def create_activity_agent(model):
    "create and return activity agent"
    agent = create_agent(
        model=model,
        tools=[
            get_activities_by_category,
            get_activities_by_duration,
            get_activities_by_rating,
            get_activity_recommendation,
            get_activities_by_interest,
            search_activities,
            get_budget_activities
        ],
        system_prompt=ACTIVITY_AGENT_SYSTEM_PROMPT
    )

    return agent
