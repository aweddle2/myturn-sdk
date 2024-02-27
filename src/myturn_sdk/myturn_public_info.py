from typing import List
from .models.address_response import AddressResponse
from .models.opening_times import OpeningTimes
from .models.opening_hours import OpeningHours
from .models.opening_hours_response import OpeningHoursResponse
from .myturn_service_base import _MyTurnServiceBase
from .browser import Browser
from datetime import datetime


class MyTurnPublicInfo(_MyTurnServiceBase):
    _userExportToCsvUrl = ''
    _userSearchUrl = ''
    _editUserUrl = ''
    _deleteUserUrl = ''

    # Default Constructor
    def __init__(self, libraryUrl: str, browser: Browser):
        self._libraryUrl = libraryUrl
        _MyTurnServiceBase.__init__(
            self, libraryUrl, browser, None)

    def GetOpeningHours(self):
        returnValue = OpeningHoursResponse()
        returnValue.success = False

        try:
            # get the MyTurn Homepage
            self.browser.get(self._libraryUrl)
            # get the opening hours table
            # TODO I think if you have multiple locations MyTurn can show all the times for all the locations on the homepage, so this may all fall apart!
            openingHoursTableContents = self.browser.getTableContents(
                'sidebar-hours-location')
            # If nothing found, assume the library has decided to not show their opening times in MyTurn
            if (len(openingHoursTableContents) == 0):
                returnValue.success = False
                returnValue.message = 'Opening Times could not be found'
                return returnValue

            # Going to assume MyTurn always starts the week on a monday
            # Python does start the week with
            openingTimes: List[OpeningTimes] = list()

            for row in openingHoursTableContents:
                # Parse the second cell to get the open and closing time
                dayTimes = self._parseTime(row[1])
                # By using the text from the first cell in the table, this code is now language independant and will get the language from whatever language MyTurn is in
                openingTimes.append(OpeningTimes(
                    row[0], dayTimes[0], dayTimes[1]))

            returnValue.openingHours = OpeningHours(openingTimes)
            returnValue.success = True
        except Exception as ex:
            returnValue.message = ex

        return returnValue

    # Parses "4:00 PM–8:00 PM" into a tuple of 24 hour time (16:00,20:00)
    # also returns null if the passed in string is 'Closed' or erors
    def _parseTime(self, openingTimeString):

        try:
            # this is a double dash character, not a normal dash
            timeArray = openingTimeString.split('–')
            # the #%I here tells the parser it's 12 hour clock rather than 24 hour
            openingTime = datetime.strptime(timeArray[0], '%I:%M %p').time()
            closingTime = datetime.strptime(timeArray[1], '%I:%M %p').time()
            return (openingTime, closingTime)
        except Exception as ex:
            return (None, None)

    def GetAddress(self):
        returnValue = AddressResponse()
        returnValue.success = False

        try:
            # get the MyTurn Homepage
            self.browser.get(self._libraryUrl)
            # get the address element
            address = self.browser.getTextByXPath('//address')

            # If nothing found, assume the library has decided to not show their address in MyTurn
            if (len(address) == 0):
                returnValue.success = False
                returnValue.message = 'Address could not be found'
                return returnValue

            returnValue.address = address
            returnValue.success = True
        except Exception as ex:
            returnValue.message = ex

        return returnValue
