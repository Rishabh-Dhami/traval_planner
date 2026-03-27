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



from langchain.agents import create_agent
from backend.app.prompts import HOTEL_AGENT_PROMPT

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
