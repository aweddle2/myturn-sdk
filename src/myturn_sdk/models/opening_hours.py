from typing import List
from .opening_times import OpeningTimes


class OpeningHours:
    def __init__(self, openingTimes: List[OpeningTimes]):
        self._openingTimes = openingTimes

    def GetOpeningTimesForDay(self, dayIndex):
        return self._openingTimes[dayIndex]

    # Python seems to start with Monday being 0 so lets follow that convention
    @property
    def monday(self):
        return self.GetOpeningTimesForDay(0)

    @property
    def tuesday(self):
        return self.GetOpeningTimesForDay(1)

    @property
    def wednesday(self):
        return self.GetOpeningTimesForDay(2)

    @property
    def thursday(self):
        return self.GetOpeningTimesForDay(3)

    @property
    def friday(self):
        return self.GetOpeningTimesForDay(4)

    @property
    def saturday(self):
        return self.GetOpeningTimesForDay(5)

    @property
    def sunday(self):
        return self.GetOpeningTimesForDay(6)
