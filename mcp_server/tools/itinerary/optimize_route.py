from typing import List, Dict, Any
from langchain.tools import tool
from mcp_server.mcp_instance import mcp


@mcp.tool()
def optimize_route(
    locations: List[str]
) -> Dict[str, Any]:
    """
    Suggest optimized visiting order based on mock activity locations.

    Args:
        locations (List[str]): List of locations

    Returns:
        Dict[str, Any]
    """

  
    if not locations or not isinstance(locations, list):
        return {
            "status": "error",
            "locations_provided": None,
            "optimized_route": None,
            "stops_count": None,
            "error": "Locations list is required",
            "error_details": None,
        }

    if len(locations) < 2:
        return {
            "status": "error",
            "locations_provided": locations,
            "optimized_route": None,
            "stops_count": len(locations),
            "error": "At least 2 locations required",
            "error_details": None,
        }

    try:
        # Normalize input
        cleaned = [
            loc.strip().lower()
            for loc in locations
            if isinstance(loc, str) and loc.strip()
        ]

        if len(cleaned) < 2:
            return {
                "status": "error",
                "locations_provided": locations,
                "optimized_route": None,
                "stops_count": len(cleaned),
                "error": "Invalid locations provided",
                "error_details": None,
            }

        #  Real grouping based on YOUR DATA
        location_groups = {
            1: ["marunouchi", "ginza", "tsukiji"],        # Central Tokyo
            2: ["shinjuku", "harajuku", "shibuya"],       # West Tokyo
            3: ["asakusa", "sumida"],                    # East Tokyo
            4: ["odaiba", "maihama"],                   # Far / Island / Disney
            5: ["day trip from tokyo"]                  # Outskirts
        }

        # Assign priority
        def get_priority(loc):
            for priority, group in location_groups.items():
                if loc in group:
                    return priority
            return 99  # unknown locations go last

        #  Sort based on group priority
        optimized = sorted(cleaned, key=get_priority)

        # Capitalize back
        optimized_route = [loc.title() for loc in optimized]

        return {
            "status": "success",
            "locations_provided": locations,
            "optimized_route": optimized_route,
            "stops_count": len(optimized_route),
            "error": None,
            "error_details": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "locations_provided": locations,
            "optimized_route": None,
            "stops_count": None,
            "error": "Failed to optimize route",
            "error_details": str(e),
        }