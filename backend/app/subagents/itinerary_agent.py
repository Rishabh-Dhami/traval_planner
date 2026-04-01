"""
    Itinerary Agent 

    Specialized agent for organizing travel components into cohensive day-by-day schedule.
    Handel optimization of timing, logistic and flow.

    - create_daily_schedule
    - optimize_route
    - generate_trip_summary 
"""

from langchain.agents import create_agent
from backend.mcp_client.tool_registry import load_tools_by_tags
from backend.app.prompts import ITINERARY_AGENT_PROMPT



def create_itinerary_agent(model):
    """
        create and return restaurant agent
    """
    tools = load_tools_by_tags("itinerary")
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=ITINERARY_AGENT_PROMPT
    )    

    return agent