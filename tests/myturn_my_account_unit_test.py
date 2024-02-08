import unittest
from src.myturn_sdk.myturn_my_account import MyTurnMyAccount
from parameterized import parameterized


class MyTurnMyAccountUnitTests(unittest.TestCase):

    @parameterized.expand([
        (None, None),
        ('m/d/yyyy', '%m/%d/%Y'),
        ('mm/d/yyyy', '%m/%d/%Y'),
        ('m/dd/yyyy', '%m/%d/%Y'),
        ('mm/dd/yyyy', '%m/%d/%Y'),
        ('d/m/yyyy', '%d/%m/%Y'),
        ('dd/m/yyyy', '%d/%m/%Y'),
        ('d/mm/yyyy', '%d/%m/%Y'),
        ('dd/mm/yyyy', '%d/%m/%Y')
    ])
    def testMyTurnDateFormatToPythonDateformat(self, myTurnFormat, expected):
        # Arrange
        myTurnUsers = MyTurnMyAccount('', None, None)

        # Act
        pythonFormat = myTurnUsers._myTurnDateFormatTostrftimeFormat(
            myTurnFormat)

        # Assert
        self.assertEqual(pythonFormat, expected)


if __name__ == '__main__':
    unittest.main()
