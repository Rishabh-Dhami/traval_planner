from typing import Dict, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
import logging
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

mcp_url = os.getenv("MCP_URL")
mcp_token = os.getenv("MCP_API_KEY")

logger = logging.getLogger(__name__)

SERVERS = {
    "travel-tools": {
        "transport": "streamable-http",
        "url": mcp_url,
        "headers": {
            "Authorization": f"Bearer {mcp_token}"
        }
    },
    }

class MCPClient:
    
    def __init__(self):
        self.client = MultiServerMCPClient(SERVERS)

    async def list_tools(self):
        try:
            tools = await self.client.get_tools()
            return tools
        except Exception as e:
            traceback.print_exc()  
            logger.warning(f"Error listing tools: {e}")
            return {"error": str(e)}
    
    async def call_tool(self, tool_name: str, payload: Dict[str, Any]):
        try:
            result = await self.client.call_tool(tool_name, payload)
            return result
        except Exception as e:
            logger.warning(f"Error calling tool {tool_name}: {e}")
            return {"error": str(e)}

