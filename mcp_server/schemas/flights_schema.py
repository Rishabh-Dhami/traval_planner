from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class Flight(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",   # ignore unknown fields safely
        str_strip_whitespace=True
    )

    id: str
    airline: str
    flight_number: str
    departure_city: str
    arrival_city: str
    departure_time: str
    arrival_time: str
    duration: str
    stops: int = Field(ge=0)
    layover: Optional[str] = None
    class_: str = Field(alias="class")
    price: int = Field(gt=0)
    currency: str


class FlightResponse(BaseModel):
    status: Literal["success", "error"]
    destination: str
    flight_count: Optional[int] = None
    flights: Optional[List[Flight]] = None
    cheapest: Optional[Flight] = None
    fastest: Optional[Flight] = None
    error: Optional[str] = None
    error_details: Optional[str] = None
