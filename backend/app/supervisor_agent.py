"""
    Supervisor Agent

    The main orchestrating agent that coordinates specialized agents to comprehensive traval plans.
    - Supervisor agent receives user requests and make routing decision. 
    - Subagents are wrapped as  tools for the supervisor to call. 
    - Result flow back to supervisor to synthesis
"""

from backend.app.core.wrapper_agents import wrap_agent_as_tool
from backend.app.prompts import SUPERVISOR_PROMPT
from langchain.agents import create_agent

async def create_supervisor_agent(agents: dict):
    "create and return supervisor agent"

    model = agents["model"]

    tools = []

    for name, agent in agents.items():
        if name == "model" or agent is None:
            continue

        tool = wrap_agent_as_tool(name=name, agent=agent)
        tools.append(tool)
    
    supervisor = create_agent(
        model=model,
        tools=tools,
        system_prompt=SUPERVISOR_PROMPT
    )

    return supervisor