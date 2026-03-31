from backend.mcp_client.client import MCPClient
from typing import Any, List
from langchain_core.tools import StructuredTool
import logging

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

                async def tool_func(input_data: dict, tool_name=tool.name):
                    return await client.call_tool(tool_name, input_data)

                tools.append(
                    StructuredTool.from_function(
                        name=tool.name,
                        description=tool.description or "No description",
                        coroutine=tool_func  
                    )
                )

        return tools

    except Exception as e:
        logger.error(f"Error loading tools: {e}", exc_info=True)
        return []