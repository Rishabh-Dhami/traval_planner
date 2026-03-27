"""
Flight Agent

Description:
This agent is responsible for handling all flight-related queries,
including searching, filtering, comparing, and recommending flights
based on user preferences such as destination, price, duration,
stops, and travel time.

The agent uses mock flight data for development and testing.
In production, this agent can be connected to real flight APIs.

Possible API integrations:
- Amadeus API
- Skyscanner API
- Kiwi API
- Google Flights API
- TravelPayouts API
- Expedia API

Capabilities:
- Search flights by destination
- Find cheapest flight
- Find fastest flight
- Find direct flights
- Compare flights

Supported Tools:

- search_flights
    Search all available flights for a destination.

- get_cheapest_flight
    Return the lowest price flight.

- get_fastest_flight
    Return the shortest duration flight.

- get_direct_flights
    Return flights with no stops.

- compare_flights
    Compare multiple flight options.

Flight Data Fields:

Each flight may contain:

id
airline
departure
arrival
duration
price
currency
stops
destination
origin

Output Format:

All tools return structured JSON responses
with the following fields:

status
destination
flights_count
flights
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

- Agent must never hallucinate flight data
- Agent must always use tools
- Agent must not modify tool output
- Agent must return structured responses only
- Agent must validate destination before search
- Agent must return error if no flight found

Examples of supported queries:

"find flights to Tokyo"
"cheapest flight to Paris"
"direct flight to Dubai"
"fastest flight available"
"compare flights to London"

Notes:

This agent is designed for multi-agent travel systems
where flights, hotels, and activities are handled
by separate agents coordinated by a supervisor.
"""

from langchain.agents import create_agent


#create a flight agent
def create_flights_agent(model):
    """Create and return flight agent"""
    agent = create_agent(
        model,
        tools=[get_cheapest_flight, get_direct_flight, search_flights, compare_flights],
        system_prompt=FLIGHT_AGENT_PROMPT
    )

    return agent    