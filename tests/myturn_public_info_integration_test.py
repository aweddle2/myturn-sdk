import unittest
from src.myturn_sdk.models.user_search_request import UserSearchRequest
from src.myturn_sdk.models.user import User
from src.myturn_sdk.myturn_client import MyTurnClient
from parameterized import parameterized


# These are integration test and actually make http calls to MyTurn
class PublicInfoTests(unittest.TestCase):

    def test_brunswick_opening_hours(self):
        # Arrange
        myTurnClient = MyTurnClient(
            "brunswicktoollibrary", None, None)

        # Act
        response = myTurnClient.publicInfo.GetOpeningHours()
        result = response.openingHours
        # Assert
        self.assertTrue(response.success)
        self.assertEqual(result.monday.openTime.hour, 16)
        self.assertEqual(result.monday.closeTime.hour, 20)
        self.assertEqual(result.monday.dayName, 'Monday')
        self.assertEqual(result.tuesday.openTime, None)
        self.assertEqual(result.tuesday.closeTime, None)
        self.assertEqual(result.tuesday.dayName, 'Tuesday')
        self.assertEqual(result.wednesday.openTime.hour, 16)
        self.assertEqual(result.wednesday.closeTime.hour, 20)
        self.assertEqual(result.wednesday.dayName, 'Wednesday')
        self.assertEqual(result.thursday.openTime, None)
        self.assertEqual(result.thursday.closeTime, None)
        self.assertEqual(result.thursday.dayName, 'Thursday')
        self.assertEqual(result.friday.openTime, None)
        self.assertEqual(result.friday.closeTime, None)
        self.assertEqual(result.friday.dayName, 'Friday')
        self.assertEqual(result.saturday.openTime.hour, 10)
        self.assertEqual(result.saturday.closeTime.hour, 14)
        self.assertEqual(result.saturday.dayName, 'Saturday')
        self.assertEqual(result.sunday.openTime, None)
        self.assertEqual(result.sunday.closeTime, None)
        self.assertEqual(result.sunday.dayName, 'Sunday')

    def test_ballarat_opening_hours(self):
        # Arrange
        myTurnClient = MyTurnClient(
            "ballarattoollibrary", None, None)

        # Act
        response = myTurnClient.publicInfo.GetOpeningHours()
        result = response.openingHours
        # Assert
        self.assertTrue(response.success)
        self.assertEqual(result.monday.openTime, None)
        self.assertEqual(result.monday.closeTime, None)
        self.assertEqual(result.monday.dayName, 'Monday')
        self.assertEqual(result.tuesday.openTime.hour, 16)
        self.assertEqual(result.tuesday.closeTime.hour, 18)
        self.assertEqual(result.tuesday.dayName, 'Tuesday')
        self.assertEqual(result.wednesday.openTime, None)
        self.assertEqual(result.wednesday.closeTime, None)
        self.assertEqual(result.wednesday.dayName, 'Wednesday')
        self.assertEqual(result.thursday.openTime.hour, 17)
        self.assertEqual(result.thursday.closeTime.hour, 19)
        self.assertEqual(result.thursday.dayName, 'Thursday')
        self.assertEqual(result.friday.openTime, None)
        self.assertEqual(result.friday.closeTime, None)
        self.assertEqual(result.friday.dayName, 'Friday')
        self.assertEqual(result.saturday.openTime.hour, 10)
        self.assertEqual(result.saturday.closeTime.hour, 12)
        self.assertEqual(result.saturday.dayName, 'Saturday')
        self.assertEqual(result.sunday.openTime, None)
        self.assertEqual(result.sunday.closeTime, None)
        self.assertEqual(result.sunday.dayName, 'Sunday')

    def test_chicago_opening_hours(self):
        # Arrange
        myTurnClient = MyTurnClient(
            "chicagotoollibrary", None, None)

        # Act
        response = myTurnClient.publicInfo.GetOpeningHours()
        # Assert
        self.assertEqual(response.openingHours, None)
        self.assertFalse(response.success)
        self.assertEqual(response.message, 'Opening Times could not be found')

    @parameterized.expand([
        ('brunswicktoollibrary',
         'Basement 1, 127 Nicholson St\nBrunswick East, 3057\nAustralia\n0492807491'),
        ('ballarattoollibrary', '25-39 Barkly St\nBallarat East, 3350\nAustralia'),
        ('chicagotoollibrary', '4015 W Carroll Ave\nChicago, IL, 60624\nUSA\n773-242-0923'),
        ('fictional', None)
    ])
    def testAddress(self, subdomain, address):
        # Arrange
        myTurnClient = MyTurnClient(
            subdomain, None, None)

        # Act
        response = myTurnClient.publicInfo.GetAddress()
        # Assert
        if (address is not None):
            self.assertTrue(response.success)
        self.assertEqual(
            response.address, address)
        if (address is None):
            self.assertFalse(response.success)
            self.assertEqual(response.message, 'Address could not be found')


if __name__ == '__main__':
    unittest.main()
