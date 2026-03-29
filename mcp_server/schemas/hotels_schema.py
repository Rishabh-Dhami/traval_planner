from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal


class Hotel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True
    )

    id: str
    name: str
    neighborhood: str
    rating: float = Field(ge=0, le=5)
    reviews: int = Field(ge=0)
    price_per_night: float = Field(gt=0)
    currency: str
    amenities: List[str]
    description: str
    traveler_type: List[
        Literal["solo", "couples", "families", "business", "luxury", "budget", "groups", "long-stay", "kids"]
    ]

class HotelResponse(BaseModel):
    status: Literal["success", "error"]
    destination: str
    hotel_count: Optional[int] = None
    hotels: Optional[List[Hotel]] = None
    cheapest: Optional[Hotel] = None
    best_rated: Optional[Hotel] = None
    recommended: Optional[Hotel] = None
    error: Optional[str] = None
    error_details: Optional[str] = None    