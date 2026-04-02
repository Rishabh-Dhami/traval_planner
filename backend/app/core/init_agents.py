import sys
from pathlib import Path

# Add project root to path so absolute imports work
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from langchain.chat_models import init_chat_model
from backend.app.subagents.activity_agent import create_activity_agent
from backend.app.subagents.hotel_agent import create_hotel_agent
from backend.app.subagents.restaurant_agent import create_restaurant_agent
from backend.app.subagents.itinerary_agent import create_itinerary_agent
from backend.app.subagents.flight_agent import create_flights_agent
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()
import asyncio

logger = logging.getLogger(__name__)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


async def safe_init(coro, name: str, timeout: int = 30):
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        logger.error(f"{name} initialization timed out")
    except Exception as e:
        logger.error(f"{name} initialization failed: {e}")
    return None


async def initialize_agents(model=llm) -> Dict[str, Any]:
    """Intailize the model and all subagents"""

    try:
        model = model
        logger.info(f"Model intialized: {model}")
    except Exception as e:
        logger.error(f"Model intialization failed: {str(e)}")
        raise

    results = await asyncio.gather(
        safe_init(create_flights_agent(model), "flight_agent"),
        safe_init(create_activity_agent(model), "activity_agent"),
        safe_init(create_itinerary_agent(model), "itinerary_agent"),
        safe_init(create_restaurant_agent(model), "restaurant_agent"),
        safe_init(create_hotel_agent(model), "hotel_agent"),
    )

    agents = {
        "model": model,
        "flight_agent": results[0],
        "activity_agent": results[1],
        "itinerary_agent": results[2],
        "restaurant_agent": results[3],
        "hotel_agent": results[4],
    }

    failed_agents = [
        name for name, agent in agents.items() if agent is None and name != "model"
    ]

    if failed_agents:
        logger.warning(f"Some agents failed to initialize: {failed_agents}")
    else:
        logger.info("All agents initialized successfully")

    return agents


_agents = None

_lock = asyncio.Lock()


async def get_agents() -> Dict[str, Any]:
    """
    Thread-safe singleton for agents.
    """
    global _agents

    async with _lock:
        if _agents is None:
            logger.info("Initializing agents for the first time...")
            _agents = await initialize_agents()
        else:
            logger.info("Returning cached agents")

    return _agents


