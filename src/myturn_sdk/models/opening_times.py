from datetime import time


class OpeningTimes:
    def __init__(self, dayName, openTime: time, closeTime: time):
        self.dayName = dayName
        self.openTime = openTime
        self.closeTime = closeTime
