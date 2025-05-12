from datetime import datetime, timedelta
from typing import Literal

from pydantic import BaseModel, computed_field


class Event(BaseModel):
    id: int
    start: datetime
    end: datetime
    type: Literal["transport", "stationary"]

    @computed_field
    @property
    def duration(self) -> timedelta:
        return self.end - self.start
