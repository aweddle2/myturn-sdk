from .response_base import ResponseBase
from .opening_hours import OpeningHours


class OpeningHoursResponse(ResponseBase):
    openingHours: OpeningHours = None
