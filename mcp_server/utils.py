import re
from mock_data.data import MOCK_ACTIVITIES, MOCK_FLIGHTS, MOCK_RESTAURANTS, MOCK_HOTELS

def parse_duration_to_hours(text: str) -> float:
    """
    Convert duration string to hours
    """

    if not text:
        return 0

    text = text.lower()

    if "full day" in text:
        return 8

    numbers = re.findall(r"\d+\.?\d*", text)

    if not numbers:
        return 0

    numbers = [float(n) for n in numbers]

    return max(numbers)

def get_flights(destination: str) -> list:
    """Get available flights for a destination"""
    return MOCK_FLIGHTS.get(destination.lower(), [])

def get_hotels(destination: str) -> list:
    """Get available hotels for a destination"""
    return MOCK_HOTELS.get(destination.lower(), [])

def get_activities(destination: str) -> list:
    """Get available activities for a destination"""
    return MOCK_ACTIVITIES.get(destination.lower(), [])

def get_restaurants(destination: str) -> list:
    """Get restaurant recommendations for a destination"""
    return MOCK_RESTAURANTS.get(destination.lower(), [])