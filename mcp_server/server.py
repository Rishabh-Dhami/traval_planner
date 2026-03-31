import sys
from pathlib import Path


_root = Path(__file__).resolve().parent.parent
_here = Path(__file__).resolve().parent
for p in (_root, _here):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

#  import SAME instance
from mcp_server.mcp_instance import mcp

#  import tools (VERY IMPORTANT)
import mcp_server.tools.flights
import mcp_server.tools.activities
import mcp_server.tools.itinerary
import mcp_server.tools.restaurants
import mcp_server.tools.hotels

#run server
if __name__ == "__main__":
    mcp.run(transport="http", port=8000)