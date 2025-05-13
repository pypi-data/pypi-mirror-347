from typing import Optional
from pydantic import BaseModel, Field
from naxai.models.calendars.schedule_object import ScheduleObject

class CreateCalendarRequest(BaseModel):
    """Request object for creating a calendar"""
    name: str
    timezone: Optional[str] = "Europe/Brussels"
    schedule: list[ScheduleObject] = Field(max_length=7, min_length=7)
    exclusions: Optional[list[str]] = None
