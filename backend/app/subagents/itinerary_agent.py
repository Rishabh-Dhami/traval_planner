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
import logging


logger = logging.getLogger(__name__)
async def create_itinerary_agent(model):
    """
    Create and return itinerary agent.

    Args:
        model: The LLM model instance to bind to the agent.
        retries: Number of attempts to load tools before failing.

    Returns:
        A configured agent instance, or None if initialization failed.

    """
    try:
        tools = await load_tools_by_tags("itinerary")
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=ITINERARY_AGENT_PROMPT
        )    

        logger.info("Itinerary agent initialized successfully")

        return agent

    except Exception as e:
        logger.error(f"Itinerary agent failed: {e}")
        return None