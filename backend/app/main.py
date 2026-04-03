import sys
from pathlib import Path

# Add project root to path so absolute imports work
# main.py is at: traval_planner/backend/app/main.py
# We need: traval_planner (go up 2 levels from app)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from typing import AsyncGenerator

from langchain_core.messages import HumanMessage

# 👉 import your agents
from backend.app.supervisor_agent import create_supervisor_agent

from backend.app.core.init_agents import get_agents


# =========================================================
# STREAM RESPONSE FUNCTION
# =========================================================


async def stream_response(user_input: str) -> AsyncGenerator[str, None]:
    """
    Stream response from supervisor agent.

    Args:
        user_input (str): User query

    Yields:
        str: streamed chunks
    """

    try:

        agents = await get_agents()
        config = {"configurable": {"thread_id": 1}}

        supervisor_agent = await create_supervisor_agent(agents=agents)
        # initial input
        messages = [HumanMessage(content=user_input)]

        # stream from agent
        async for chunk in supervisor_agent.astream(
            {"messages": messages}, config=config
        ):

            # 🔥 LangGraph / LCEL stream structure
            if "messages" in chunk:
                last_message = chunk["messages"][-1]

                if hasattr(last_message, "content") and last_message.content:
                    yield last_message.content

    except Exception as e:
        yield f"Error: {str(e)}"


# =========================================================
# SIMPLE CLI TEST (optional)
# =========================================================


async def main():
    print("🚀 Travel Planner AI (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        print("AI: ", end="", flush=True)

        async for chunk in stream_response(user_input):
            print(chunk, end="", flush=True)

        print("\n")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    asyncio.run(main())
