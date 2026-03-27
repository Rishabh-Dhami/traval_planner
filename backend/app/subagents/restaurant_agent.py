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
from app.prompts import RESTAURANT_AGENT_PROMPT





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