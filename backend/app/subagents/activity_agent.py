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
from pathlib import Path

# Add project root to path so absolute imports work
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from langchain.agents import create_agent
from backend.app.prompts import ACTIVITY_AGENT_PROMPT
from backend.mcp_client.tool_registry import load_tools_by_tags
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

logger = logging.getLogger(__name__)
async def create_activity_agent(model):
    "create and return activity agent"

    try:
        tools = await load_tools_by_tags("activity")
        agent = create_agent(
            model,
            tools=tools,
            system_prompt=ACTIVITY_AGENT_PROMPT
        )

        logger.info("Activity agent intiallized successfully")

        return agent
    except Exception as e:
        logger.warning(f"Activity agent failed: {str(e)}")
        return None
