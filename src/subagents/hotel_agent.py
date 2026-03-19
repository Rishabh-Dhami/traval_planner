"""
Hotel Agent

Description:
This agent is responsible for searching, filtering, and recommending
hotels based on user preferences such as destination, budget, rating,
traveler type, and amenities.

The agent uses mock hotel data for development and testing.
In production, this agent can be connected to real hotel APIs.

Possible API integrations:
- Booking.com API
- Hotels.com API
- Expedia API
- Airbnb API
- Agoda API
- Google Hotels API

Capabilities:
- Search hotels by destination
- Filter hotels by budget
- Filter hotels by rating
- Filter hotels by traveler type
- Filter hotels by amenities
- Get best hotel recommendation

Supported Tools:

- search_hotels
    Search hotels for a given destination.

- get_budget_hotels
    Return hotels under a given budget.

- get_hotels_by_rating
    Return hotels with minimum rating.

- get_hotels_by_traveler_type
    Filter hotels for:
    solo / couples / families / business / luxury / budget / groups / long-stay

- get_hotels_by_amenities
    Filter hotels by amenities such as:
    Spa / Gym / Pool / Free WiFi / Restaurant / Bar /
    Concierge / Parking / Laundry / Kids Club /
    Michelin Restaurant / Limousine Service / Kitchen

- get_hotel_recommendation
    Return best hotel based on priority:
    price / rating / balanced

Output Format:

All tools return structured JSON responses
with the following fields:

status
destination
hotels_count
hotels
error
error_details

This allows the agent to be safely used in:

- LangChain agents
- LangGraph multi-agent systems
- Supervisor agents
- Tool routing systems
- Production APIs
- Backend services

Notes:

- Agent must never hallucinate hotel data.
- Agent must always use tools.
- Agent must not modify tool output.
- Agent must return structured responses only.
"""

import sys
sys.path.insert(0, '../..')

from langchain.agents import create_agent
from langchain.tools import tool
from src.mock_data.data import get_hotels
from typing import  List, Dict, Any
from src.prompts import HOTEL_AGENT_PROMPT


# Search hotels for a given destination.
@tool
def search_hotels(
    destination: str
) -> Dict[str, Any]:
    """
    Search for available hotels in a destination.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris").

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "hotels_count": int | None,
                "hotels": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    try:
        hotels: List[Dict[str, Any]] = get_hotels(
            destination.lower().strip()
        )

        if not hotels:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found for {destination}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination,
            "hotels_count": len(hotels),
            "hotels": hotels,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to search hotels",
            "error_details": str(e),
        }
    
#Return hotels under a given budget.    
@tool
def get_budget_hotels(
    destination: str,
    budget: int
) -> Dict[str, Any]:
    """
    Filter available hotels under the given budget.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris").
        budget (int): Maximum price per night.

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "hotels_count": int | None,
                "hotels": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    if budget is None or budget <= 0:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Budget must be greater than 0",
            "error_details": None,
        }

    try:
        hotels: List[Dict[str, Any]] = get_hotels(
            destination.lower().strip()
        )

        if not hotels:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found for {destination}",
                "error_details": None,
            }

        # filter by budget
        hotels_under_budget = [
            hotel for hotel in hotels
            if hotel.get("price_per_night", float("inf")) <= budget
        ]

        if not hotels_under_budget:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found under budget {budget}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination,
            "hotels_count": len(hotels_under_budget),
            "hotels": hotels_under_budget,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to filter hotels by budget",
            "error_details": str(e),
        }
from typing import Dict, Any, List


#Return hotels with minimum rating.
@tool
def get_hotels_by_rating(
    destination: str,
    rating: int
) -> Dict[str, Any]:
    """
    Get hotels for a destination filtered by rating.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris").
        rating (int): Minimum hotel rating (e.g., 3, 4, 5).

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "hotels_count": int | None,
                "hotels": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    if rating is None or rating <= 0:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Rating cannot be empty",
            "error_details": None,
        }

    try:
        hotels: List[Dict[str, Any]] = get_hotels(
            destination.lower().strip()
        )

        if not hotels:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found for {destination}",
                "error_details": None,
            }

        # filter by rating (>= rating)
        hotels_under_rating = [
            hotel for hotel in hotels
            if hotel.get("rating", 0) >= rating
        ]

        if not hotels_under_rating:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found with rating >= {rating}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination,
            "hotels_count": len(hotels_under_rating),
            "hotels": hotels_under_rating,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to filter hotels by rating",
            "error_details": str(e),
        }
from typing import Dict, Any, List, Literal

#Filter hotels by traveler_type
@tool
def get_hotels_by_traveler_type(
    destination: str,
    traveler_type: List[
        Literal[
            "solo",
            "couples",
            "families",
            "groups",
            "business",
            "kids",
            "budget",
            "luxury",
            "long-stay"
        ]
    ]
) -> Dict[str, Any]:
    """
    Get hotels filtered by traveler type.

    Args:
        destination (str): Destination city (e.g., "tokyo", "paris")
        traveler_type (List[str]): traveler categories
            allowed:
            solo, couples, families, groups,
            business, kids, budget, luxury, long-stay

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "hotels_count": int | None,
                "hotels": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }
    """

    # ✅ validation
    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": "",
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    if not traveler_type:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "traveler_type cannot be empty",
            "error_details": None,
        }

    try:

        hotels: List[Dict[str, Any]] = get_hotels(
            destination.lower().strip()
        )

        if not hotels:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found for {destination}",
                "error_details": None,
            }

        # ✅ filter by traveler type (supports multiple)
        filtered_hotels = [
            hotel
            for hotel in hotels
            if any(
                t in hotel.get("traveler_type", [])
                for t in traveler_type
            )
        ]

        if not filtered_hotels:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": (
                    f"No hotels found for traveler type "
                    f"{traveler_type} in {destination}"
                ),
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination,
            "hotels_count": len(filtered_hotels),
            "hotels": filtered_hotels,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to filter hotels by traveler type",
            "error_details": str(e),
        }


# Filter hotels by amenities 
@tool
def get_hotels_by_amenities(
    destination: str, 
    amentities : List[
        Literal[
            "Spa",
            "Pool",
            "Gym",
            "Restaurant",
            "Bar",
            "Room Service",
            "Free WiFi",
            "Laundry",
            "Kids Club",
            "Disney Shuttle",
            "Multiple Restaurants",
            "Limousine Service",
            "Kitchen",
            "Washer",
            "Living Area",
            "Michelin Restaurant",
            "Concierge",
            "Courtyard"
        ]
    ]
)-> Dict[str, Any]:
    """
        Get availabel hotels filted by aminities

        Args: 
            destination (str): Destination city (e.g, "tokyo", "paris").
            aminities (List[str] ): Amenities category allowed:
                "Spa", "Pool",
                "Gym",
                "Restaurant",
                "Bar",
                "Room Service",
                "Free WiFi",
                "Laundry",
                "Kids Club",
                "Disney Shuttle",
                "Multiple Restaurants",
                "Limousine Service",
                "Kitchen",
                "Washer",
                "Living Area",
                "Michelin Restaurant",
                "Concierge",
                "Courtyard"

    Returns:
        Dict[str, Any]:
            {
                "status": "success" | "error",
                "destination": str,
                "hotels_count": int | None,
                "hotels": List[Dict[str, Any]] | None,
                "error": str | None,
                "error_details": str | None
            }   

    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": "",
            "hotels_count": None,
            "hotels": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    if not amentities:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Amentities cannot be empty",
            "error_details": None,
        }

    try:

        hotels: List[Dict[str, Any]] = get_hotels(
            destination.lower().strip()
        )

        if not hotels:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": f"No hotels found for {destination}",
                "error_details": None,
            }
        
        filtered_hotels = [
            hotel for hotel in hotels if any(
                t in hotel.get("amenities", []) 
                for t in amentities
            )
        ]

        if not filtered_hotels:
            return {
                "status": "error",
                "destination": destination,
                "hotels_count": None,
                "hotels": None,
                "error": (
                    f"No hotels found for amentity type "
                    f"{amentities} in {destination}"
                ),
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination,
            "hotels_count": len(filtered_hotels),
            "hotels": filtered_hotels,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination,
            "hotels_count": None,
            "hotels": None,
            "error": "Failed to filter hotels by amenities type",
            "error_details": str(e),
        }

# Return best hotel based on priority:
# price / rating / balanced
@tool
def get_hotel_recommendation(
    destination: str,
    traveler_type: str,
    priority: Literal["price", "rating", "balanced"] = "balanced"
) -> Dict[str, Any]:
    """
    Get personalized hotel recommendation.

    Args:
        destination (str)
        traveler_type (str)
        priority: "price" | "rating" | "balanced"

    Returns:
        Dict[str, Any]
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": "",
            "recommendation": None,
            "runner_up": None,
            "error": "Destination cannot be empty",
            "error_details": None,
        }

    try:

        hotels: List[Dict[str, Any]] = get_hotels(
            destination.lower().strip()
        )

        if not hotels:
            return {
                "status": "error",
                "destination": destination,
                "recommendation": None,
                "runner_up": None,
                "error": f"No hotels found for {destination}",
                "error_details": None,
            }

        # ✅ filter by traveler type
        traveler_type_lower = traveler_type.lower()

        matching_hotels = [
            h for h in hotels
            if traveler_type_lower in h.get("traveler_type", [])
        ]

        if not matching_hotels:
            matching_hotels = hotels


        # ✅ sorting logic
        if priority == "price":

            matching_hotels.sort(
                key=lambda x: x.get(
                    "price_per_night",
                    float("inf")
                )
            )

        elif priority == "rating":

            matching_hotels.sort(
                key=lambda x: x.get("rating", 0),
                reverse=True
            )

        else:  # balanced

            matching_hotels.sort(
                key=lambda x:
                x.get("rating", 0)
                / max(x.get("price_per_night", 1), 1),
                reverse=True
            )


        top_pick = matching_hotels[0]

        runner_up = (
            matching_hotels[1]
            if len(matching_hotels) > 1
            else None
        )


        return {
            "status": "success",
            "destination": destination,

            "recommendation": {
                "id": top_pick.get("id"),
                "name": top_pick.get("name"),
                "neighborhood": top_pick.get("neighborhood"),
                "rating": top_pick.get("rating"),
                "reviews": top_pick.get("reviews"),
                "price_per_night": top_pick.get("price_per_night"),
                "currency": top_pick.get("currency"),
                "amenities": top_pick.get("amenities"),
                "description": top_pick.get("description"),
                "traveler_type": top_pick.get("traveler_type"),
            },

            "runner_up": (
                {
                    "id": runner_up.get("id"),
                    "name": runner_up.get("name"),
                    "rating": runner_up.get("rating"),
                    "price_per_night": runner_up.get("price_per_night"),
                }
                if runner_up
                else None
            ),

            "error": None,
            "error_details": None,
        }

    except Exception as e:

        return {
            "status": "error",
            "destination": destination,
            "recommendation": None,
            "runner_up": None,
            "error": "Failed to get recommendation",
            "error_details": str(e),
        }
    

def create_hotel_agent(model):
    """create and return hotel agent"""
    agent = create_agent(
        model=model,
        tools=[
            search_hotels,
            get_budget_hotels,
            get_hotel_recommendation,
            get_hotels_by_amenities,
            get_hotels_by_rating,
            get_hotels_by_traveler_type
        ],
        system_prompt=HOTEL_AGENT_PROMPT
    )

    return agent
