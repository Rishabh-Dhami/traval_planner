"""
Restaurant Agent Module

This module defines the Restaurant Agent used in the travel multi-agent system.
The agent handles restaurant search, filtering, and recommendation using
tool-based execution.

Purpose
-------
Provide accurate restaurant results for a given destination by calling
registered tools instead of generating data manually.

Responsibilities
---------------
- Search restaurants by destination
- Filter restaurants by cuisine, price range, rating, or tags
- Get budget-friendly restaurants
- Recommend the best restaurant based on priority
- Return structured tool responses without modification

Tools Used
----------
search_restaurants
get_restaurants_filtered
get_budget_restaurants
get_restaurants_by_rating
get_restaurants_by_tags
get_restaurant_recommendation

Design Rules
------------
- Tool-first architecture (no hallucination)
- Always use tools for restaurant data
- Never modify tool output
- Keep prompts small for low-context models (Gemini free / small LLMs)
- Compatible with LangChain / LangGraph tool calling
- Safe for multi-agent supervisor routing

Notes
-----
This agent only handles restaurant-related queries.
Routing to this agent must be done by the Supervisor Agent.

This file defines:
- Restaurant agent system prompt
- Tool bindings
- Agent initialization logic
"""

import sys
sys.path.insert(0, '../..')

from langchain.agents import create_agent
from langchain.tools import tool
from src.utils import get_restaurants
from typing import  List, Dict, Any, Literal, Union, Optional
from src.prompts import RESTAURANT_AGENT_PROMPT


@tool
def search_restaurants(
    destination: str
) -> Dict[str, Any]:
    """
    Search available restaurants for a destination.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "restaurants_count": int | None,
            "restaurants": List[Dict[str, Any]] | None,
            "error": str | None,
            "error_details": str | None
        }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination is required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        restaurants: List[Dict[str, Any]] = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found for destination: {destination_clean}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurants_count": len(restaurants),
            "restaurants": restaurants,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurants_count": None,
            "restaurants": None,
            "error": f"Failed to search restaurants for destination: {destination_clean}",
            "error_details": str(e),
        }
    

@tool
def get_restaurants_by_rating(
    destination: str,
    rating: float
) -> Dict[str, Any]:
    """
    Get available restaurants for a destination filtered by rating.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        rating (float):
            Minimum rating required (e.g., 3.5, 4.0, 4.5)

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "restaurants_count": int | None,
            "restaurants": List[Dict[str, Any]] | None,
            "error": str | None,
            "error_details": str | None
        }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if rating is None or rating < 0:
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Rating must be >= 0",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        restaurants = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found for destination: {destination_clean}",
                "error_details": None,
            }

        filtered_restaurants = [
            res for res in restaurants
            if isinstance(res.get("rating"), (int, float))
            and res.get("rating", 0) >= rating
        ]

        if not filtered_restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found with rating >= {rating}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurants_count": len(filtered_restaurants),
            "restaurants": filtered_restaurants,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Failed to filter restaurants by rating",
            "error_details": str(e),
        }
    

@tool
def get_budget_restaurants(
    destination: str,
    budget: int
) -> Dict[str, Any]:
    """
    Get available restaurants for a destination filtered by rating.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        Budget (int):
            Maximum budget required (e.g., 3, 343, 2300)

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "restaurants_count": int | None,
            "restaurants": List[Dict[str, Any]] | None,
            "error": str | None,
            "error_details": str | None
        }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if budget is None:
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Budget must be required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        restaurants = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found for destination: {destination_clean}",
                "error_details": None,
            }

        filtered_restaurants = [
            res for res in restaurants
            if isinstance(res.get("price_range"), (int, float))
            and res.get("price_range") <= budget
        ]

        if not filtered_restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found with budget <= {budget}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurants_count": len(filtered_restaurants),
            "restaurants": filtered_restaurants,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Failed to filter restaurants by max budger",
            "error_details": str(e),
        }   
    

@tool
def get_restaurants_by_tags(
    destination: str,
    tags: Union[
        str,
        List[
            Literal[
                "special occasion",
                "sushi lovers",
                "solo dining",
                "late night",
                "budget",
                "groups",
                "atmosphere",
                "tourists",
                "lunch",
                "healthy",
                "quick meal",
                "fine dining",
                "foodies",
            ]
        ],
    ],
) -> Dict[str, Any]:
    """
    Get available restaurants for a destination filtered by tags.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        tags (str | List[str]):
            Tag or list of tags.

            Examples:
                "budget"
                ["budget", "late night"]

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "restaurants_count": int | None,
            "restaurants": List[Dict[str, Any]] | None,
            "error": str | None,
            "error_details": str | None
        }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination is required",
            "error_details": None,
        }

    if not tags:
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Tags are required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        restaurants = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found for destination: {destination_clean}",
                "error_details": None,
            }

        # normalize tags → always list
        if isinstance(tags, str):
            tags_list = [tags.lower().strip()]
        else:
            tags_list = [t.lower().strip() for t in tags]

        filtered_restaurants = [
            res
            for res in restaurants
            if any(
                tag in [x.lower() for x in res.get("best_for", [])]
                for tag in tags_list
            )
        ]

        if not filtered_restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": f"No restaurants found for tags: {tags_list}",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurants_count": len(filtered_restaurants),
            "restaurants": filtered_restaurants,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Failed to filter restaurants by tags",
            "error_details": str(e),
        }
    

@tool
def get_restaurant_recommendation(
    destination: str,
    priority: Literal["price", "rating", "balanced"] = "balanced",
) -> Dict[str, Any]:
    """
    Get best restaurant recommendation for a destination.

    Args:
        destination (str):
            Destination city name (e.g., "tokyo", "paris")

        priority (str):
            Recommendation priority:
                - "price" → cheapest
                - "rating" → highest rating
                - "balanced" → best rating with reasonable price

    Returns:
        Dict[str, Any]:
        {
            "status": "success" | "error",
            "destination": str,
            "restaurant": Dict | None,
            "error": str | None,
            "error_details": str | None
        }
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurant": None,
            "error": "Destination is required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:
        restaurants = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurant": None,
                "error": f"No restaurants found for {destination_clean}",
                "error_details": None,
            }

    

        best = None

        # -------- PRICE --------
        if priority == "price":

            best = min(
                restaurants,
                key=lambda x : x.get("price_range"),
            )

        # -------- RATING --------
        elif priority == "rating":

            best = max(
                restaurants,
                key=lambda r: r.get("rating", 0),
            )

        # -------- BALANCED --------
        else:

            best = max(
                restaurants,
                key=lambda x: x.get("rating") / (x.get("price_range") + 1)
            )
        

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurant": best,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurant": None,
            "error": "Failed to get restaurant recommendation",
            "error_details": str(e),
        }    


@tool
def get_restaurants_filtered(
    destination: str,
    cuisine: Optional[str] = None,
    price_range: Optional[str] = None,
    min_rating: Optional[float] = None,
    neighborhood: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Get restaurants using multiple filters.

    Args:
        destination (str):
            Destination city

        cuisine (str, optional):
            Cuisine type (e.g., "sushi", "ramen")

        price_range (str, optional):
            $, $$, $$$, $$$$

        min_rating (float, optional):
            Minimum rating

        neighborhood (str, optional):
            Area name

        tags (List[str], optional):
            best_for tags

    Returns:
        Dict[str, Any]
    """

    if not destination or not destination.strip():
        return {
            "status": "error",
            "destination": destination,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Destination required",
            "error_details": None,
        }

    destination_clean = destination.strip().lower()

    try:

        restaurants = get_restaurants(destination_clean)

        if not restaurants:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": "No restaurants found",
                "error_details": None,
            }

        filtered = restaurants

        # cuisine
        if cuisine:
            filtered = [
                r for r in filtered
                if cuisine.lower() in r.get("cuisine", "").lower()
            ]

        # price
        if price_range:
            filtered = [
                r for r in filtered
                if r.get("price_range") == price_range
            ]

        # rating
        if min_rating is not None:
            filtered = [
                r for r in filtered
                if r.get("rating", 0) >= min_rating
            ]

        # neighborhood
        if neighborhood:
            filtered = [
                r for r in filtered
                if neighborhood.lower()
                in r.get("neighborhood", "").lower()
            ]

        # tags
        if tags:
            tags_lower = [t.lower() for t in tags]

            filtered = [
                r for r in filtered
                if any(
                    t in [x.lower() for x in r.get("best_for", [])]
                    for t in tags_lower
                )
            ]

        if not filtered:
            return {
                "status": "error",
                "destination": destination_clean,
                "restaurants_count": None,
                "restaurants": None,
                "error": "No restaurants match filters",
                "error_details": None,
            }

        return {
            "status": "success",
            "destination": destination_clean,
            "restaurants_count": len(filtered),
            "restaurants": filtered,
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "destination": destination_clean,
            "restaurants_count": None,
            "restaurants": None,
            "error": "Filtering failed",
            "error_details": str(e),
        }
    


def create_restaurant_agent(model):
    """
        create and return restaurant agent
    """
    agent = create_agent(
        model=model,
        tools=[
            get_budget_restaurants,
            search_restaurants,
            get_restaurant_recommendation,
            get_restaurants_by_rating,
            get_restaurants_by_rating,
            get_restaurants_by_tags,
            get_restaurants_filtered
        ],
        system_prompt=RESTAURANT_AGENT_PROMPT
    )    

    return agent