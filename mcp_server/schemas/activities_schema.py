from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal


class Activity(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True
    )

    id: str
    name: str
    category: Literal["Culture", "Food", "Entertainment", "Nature", "Views"]
    duration: str
    price: float = Field(ge=0)
    currency: str
    rating: float = Field(ge=0, le=5)
    description: str
    best_for: List[str]
    location: str


class ActivityResponse(BaseModel):
    status: Literal["success", "error"]
    destination: str
    activity_count: Optional[int] = None
    activities: Optional[List[Activity]] = None
    cheapest: Optional[Activity] = None
    best_rated: Optional[Activity] = None
    recommended: Optional[Activity] = None
    error: Optional[str] = None
    priority: Optional[Literal["price", "rating", "balanced"]] = None
    error_details: Optional[str] = None    