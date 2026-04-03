from backend.mcp_client.client import MCPClient
from typing import List
from langchain_core.tools import StructuredTool
import logging
import inspect

logger = logging.getLogger(__name__)


async def load_tools_by_tags(tag: str) -> List[StructuredTool]:
    """Load MCP tools filtered by tag"""

    try:
        client = MCPClient()

        mcp_tools = await client.list_tools()

        tools = []

        for tool in mcp_tools:
            tags = (
                getattr(tool, "metadata", {})
                .get("_meta", {})
                .get("_fastmcp", {})
                .get("tags", [])
            )

            if tag in tags:
                # Create a factory function to properly capture tool_name in closure
                def create_tool_func(tool_name):
                    async def tool_func(input_data: dict):
                        return await client.call_tool(tool_name, input_data)

                    return tool_func

                tool_func = create_tool_func(tool.name)

                tools.append(
                    StructuredTool.from_function(
                        name=tool.name,
                        description=tool.description or "No description",
                        func=tool_func,  # Pass as func, not coroutine - LangChain will handle async
                    )
                )

        return tools

    except Exception as e:
        logger.error(f"Error loading tools: {e}", exc_info=True)
        return []
