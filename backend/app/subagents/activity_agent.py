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


from langchain.agents import create_agent
from app.utils import get_activities
from backend.app.prompts import ACTIVITY_AGENT_SYSTEM_PROMPT



@tool



@tool



@tool



@tool


@tool



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
