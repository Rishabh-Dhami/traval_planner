"""
    Itinerary Agent 

    Specialized agent for organizing travel components into cohensive day-by-day schedule.
    Handel optimization of timing, logistic and flow.

    - create_daily_schedule
    - optimize_route
    - generate_trip_summary 
"""

from langchain.tools import tool
from langchain.agents import create_agent
from typing import Dict, Any, List, Literal



