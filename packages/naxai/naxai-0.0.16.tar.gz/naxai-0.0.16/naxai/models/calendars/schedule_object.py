from typing import Optional
from pydantic import BaseModel, Field

HOUR_PATTERN = r'^\d{2}:\d{2}$'

class ScheduleObject(BaseModel):
    """Schedule object for creating a calendar"""
    day: int = Field(ge=1, le=7)
    open: bool
    start: Optional[str] = Field(pattern=HOUR_PATTERN, default=None)
    stop: Optional[str] = Field(pattern=HOUR_PATTERN, default=None)
    extended: Optional[bool] = Field(default=False)
    extension_start: Optional[str] = Field(alias="extensionStart", pattern=HOUR_PATTERN, default=None)
    extension_stop: Optional[str] = Field(alias="extensionStop", pattern=HOUR_PATTERN, default=None)

    model_config = {"populate_by_name": True,
                    "validate_by_name": True}
