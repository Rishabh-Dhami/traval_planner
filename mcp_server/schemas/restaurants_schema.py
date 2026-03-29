from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal, Optional


class Restaurant(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True
    )

    id: str
    name: str
    cuisine: str
    price_range: str   
    rating: float = Field(ge=0, le=5)
    neighborhood: str
    description: str
    best_for: List[str]

class RestaurantResponse(BaseModel):
    status: Literal["success", "error"]
    destination: str
    restaurant_count: Optional[int] = None
    restaurants: Optional[List[Restaurant]] = None
    cheapest: Optional[Restaurant] = None
    recommended: Optional[Restaurant] = None
    error: Optional[str] = None
    error_details: Optional[str] = None
