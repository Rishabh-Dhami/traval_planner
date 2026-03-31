from fastmcp import Client
from typing import Dict, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

mcp_url = os.getenv("MCP_URL")

logger = logging.getLogger(__name__)


SERVERS = {
    "travel-tools": {
        "transport": "streamable_http",  # if this fails, try "sse"
        "url": mcp_url
    },
}


class MCPClient:
    def __init__(self, servers: dict):
        self.client = Client(servers)

    async def list_tools(self):
        try:
            async with self.client:
                tools = await self.client.list_tools()
                return tools
        except Exception as e:
            logger.warning(f"Error listing tools: {e}")
            return {"error": str(e)}
    
    async def call_tool(self, tool_name: str, payload: Dict[str, Any]):
        try:
            response = await self.client.call_tool(tool_name, payload)
            return response
        except Exception as e:
            logger.warning(f"Error calling tool {tool_name}: {e}")
            return {"error": str(e)}

# ✅ Run properly
async def main():
    print("URL:", mcp_url)
    client = MCPClient(servers=SERVERS)
    
    tools = await client.list_tools()
    print(tools)

asyncio.run(main())


