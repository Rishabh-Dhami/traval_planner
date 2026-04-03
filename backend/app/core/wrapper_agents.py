from langchain_core.tools import StructuredTool
import inspect


def wrap_agent_as_tool(name: str, agent):
    """wrap agent as tool so that supervior can use"""

    async def tool_func(input_text: str):
        try:
            response = await agent.ainvoke({"input": input_text})
            return response
        except Exception as e:
            return f"{name} failed: {str(e)}"

    return StructuredTool.from_function(
        name=name,
        func=tool_func,
        description=f"Use this tool for {name.replace('_', ' ')} queries",
        coroutine=tool_func,  # Explicitly pass coroutine to handle async properly
    )
